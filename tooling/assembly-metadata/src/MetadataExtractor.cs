using System.Collections.Immutable;
using System.Globalization;
using System.Reflection;
using System.Reflection.Metadata;
using System.Reflection.PortableExecutable;
using System.Security.Cryptography;
using System.Text.Json;

namespace AssemblyMetadata;

internal sealed record AssemblyIdentity(string name, string version, string culture, string public_key_token,
    string? file_version, string? informational_version);
internal sealed record ResourceSet(string name, string[] resources);
internal sealed record ExtractedAssembly(AssemblyIdentity Identity, ResourceSet Resources, string[] Api);

internal static class MetadataExtractor
{
    public static ExtractedAssembly Extract(string path)
    {
        using FileStream file = File.OpenRead(path);
        if (file.Length > 512L * 1024 * 1024)
            throw new InvalidDataException("Assembly exceeds the 512 MiB input limit");
        using var pe = new PEReader(file, PEStreamOptions.LeaveOpen);
        if (!pe.HasMetadata || pe.PEHeaders.CorHeader is null)
            throw new BadImageFormatException("File is not a managed PE with CLR metadata");
        MetadataReader reader = pe.GetMetadataReader();
        if (!reader.IsAssembly)
            throw new BadImageFormatException("Managed modules without an assembly definition are not supported");

        var definition = reader.GetAssemblyDefinition();
        string assemblyName = reader.GetString(definition.Name);
        string culture = definition.Culture.IsNil ? "neutral" : reader.GetString(definition.Culture);
        if (string.IsNullOrEmpty(culture)) culture = "neutral";
        byte[] publicKey = definition.PublicKey.IsNil ? [] : reader.GetBlobBytes(definition.PublicKey);
        string token = "null";
        if (publicKey.Length != 0)
        {
            byte[] hash = SHA1.HashData(publicKey);
            token = Convert.ToHexString(hash.AsSpan(hash.Length - 8).ToArray().Reverse().ToArray()).ToLowerInvariant();
        }

        string? fileVersion = null;
        string? infoVersion = null;
        foreach (CustomAttributeHandle handle in definition.GetCustomAttributes())
        {
            var attribute = reader.GetCustomAttribute(handle);
            string? typeName = AttributeType(reader, attribute.Constructor);
            if (typeName is not ("System.Reflection.AssemblyFileVersionAttribute" or
                "System.Reflection.AssemblyInformationalVersionAttribute")) continue;
            var blob = reader.GetBlobReader(attribute.Value);
            if (blob.ReadUInt16() != 1) throw new BadImageFormatException("Invalid custom attribute prolog");
            string? value = blob.ReadSerializedString();
            if (typeName == "System.Reflection.AssemblyFileVersionAttribute") fileVersion = value;
            else infoVersion = value;
        }

        var identity = new AssemblyIdentity(assemblyName, definition.Version.ToString(), culture,
            token, fileVersion, infoVersion);

        var resources = reader.ManifestResources
            .Select(h => reader.GetString(reader.GetManifestResource(h).Name))
            .OrderBy(x => x, StringComparer.Ordinal).ToArray();
        if (resources.Distinct(StringComparer.Ordinal).Count() != resources.Length)
            throw new BadImageFormatException("Duplicate manifest resource name");

        var api = new SortedSet<string>(StringComparer.Ordinal);
        var signature = new SignatureText();
        foreach (TypeDefinitionHandle handle in reader.TypeDefinitions)
        {
            var type = reader.GetTypeDefinition(handle);
            if (!VisibleType(reader, handle)) continue;
            string fullName = SignatureText.FullTypeName(reader, handle);
            ImmutableArray<string> typeNames = GenericNames(reader, type.GetGenericParameters());
            var ctx = new SignatureContext(typeNames, []);
            string kind = (type.Attributes & TypeAttributes.Interface) != 0 ? "interface" :
                (type.Attributes & TypeAttributes.Abstract) != 0 ? "abstract class" : "class";
            string baseName = signature.Resolve(reader, type.BaseType, ctx);
            string interfaces = string.Join(",", type.GetInterfaceImplementations()
                .Select(h => signature.Resolve(reader, reader.GetInterfaceImplementation(h).Interface, ctx))
                .OrderBy(x => x, StringComparer.Ordinal));
            string flags = $"{type.Attributes & (TypeAttributes.Abstract | TypeAttributes.Sealed | TypeAttributes.Interface)}";
            Add(api, $"type {fullName} visibility={type.Attributes & TypeAttributes.VisibilityMask} kind={kind} flags={flags} base={baseName} interfaces=[{interfaces}]" +
                Constraints(reader, type.GetGenericParameters(), signature, ctx));

            foreach (FieldDefinitionHandle fieldHandle in type.GetFields())
            {
                FieldDefinition field = reader.GetFieldDefinition(fieldHandle);
                string? visibility = FieldVisibility(field.Attributes);
                if (visibility is null) continue;
                var fieldType = field.DecodeSignature(signature, ctx);
                string extra = (field.Attributes & FieldAttributes.Literal) != 0 ? " const" :
                    (field.Attributes & FieldAttributes.InitOnly) != 0 ? " readonly" : "";
                string constant = field.GetDefaultValue().IsNil ? "" :
                    " value=" + ReadConstant(reader, field.GetDefaultValue());
                Add(api, $"field {fullName}.{reader.GetString(field.Name)} {visibility}{extra} type={fieldType}{constant}");
            }

            foreach (MethodDefinitionHandle methodHandle in type.GetMethods())
            {
                MethodDefinition method = reader.GetMethodDefinition(methodHandle);
                string? visibility = MethodVisibility(method.Attributes);
                if (visibility is null) continue;
                var methodNames = GenericNames(reader, method.GetGenericParameters());
                var methodCtx = new SignatureContext(typeNames, methodNames);
                var parsed = method.DecodeSignature(signature, methodCtx);
                string methodName = reader.GetString(method.Name);
                string modifiers = (method.Attributes & MethodAttributes.Static) != 0 ? " static" : "";
                if ((method.Attributes & MethodAttributes.Abstract) != 0) modifiers += " abstract";
                else if ((method.Attributes & MethodAttributes.Virtual) != 0) modifiers += " virtual";
                var parameters = method.GetParameters()
                    .Select(h => reader.GetParameter(h)).Where(p => p.SequenceNumber > 0)
                    .OrderBy(p => p.SequenceNumber)
                    .ToDictionary(p => (int)p.SequenceNumber);
                var argTypes = parsed.ParameterTypes.Select((p, i) =>
                {
                    bool hasParameter = parameters.TryGetValue(i + 1, out Parameter metadata);
                    ParameterAttributes attr = hasParameter ? metadata.Attributes : 0;
                    string flag = (attr & ParameterAttributes.Out) != 0 ? "out " :
                        (attr & ParameterAttributes.In) != 0 ? "in " : "";
                    if ((attr & ParameterAttributes.Optional) != 0) flag += "optional ";
                    string constant = hasParameter && !metadata.GetDefaultValue().IsNil ?
                        " default=" + ReadConstant(reader, metadata.GetDefaultValue()) : "";
                    return flag + p + constant;
                });
                Add(api, $"method {fullName}.{methodName} {visibility}{modifiers} " +
                    $"generic={parsed.GenericParameterCount} ({string.Join(",", argTypes)})->{parsed.ReturnType}" +
                    Constraints(reader, method.GetGenericParameters(), signature, methodCtx));
            }

            foreach (PropertyDefinitionHandle handleProperty in type.GetProperties())
            {
                PropertyDefinition prop = reader.GetPropertyDefinition(handleProperty);
                var access = prop.GetAccessors();
                string? getter = Accessor(reader, access.Getter);
                string? setter = Accessor(reader, access.Setter);
                if (getter is null && setter is null) continue;
                var parsed = prop.DecodeSignature(signature, ctx);
                Add(api, $"property {fullName}.{reader.GetString(prop.Name)} " +
                    $"type={parsed.ReturnType} index=[{string.Join(",", parsed.ParameterTypes)}] " +
                    $"getter={getter ?? "none"} setter={setter ?? "none"}");
            }

            foreach (EventDefinitionHandle eventHandle in type.GetEvents())
            {
                EventDefinition ev = reader.GetEventDefinition(eventHandle);
                var access = ev.GetAccessors();
                string? adder = Accessor(reader, access.Adder);
                string? remover = Accessor(reader, access.Remover);
                if (adder is null && remover is null) continue;
                string eventType = signature.Resolve(reader, ev.Type, ctx);
                Add(api, $"event {fullName}.{reader.GetString(ev.Name)} type={eventType} " +
                    $"add={adder ?? "none"} remove={remover ?? "none"}");
            }
        }

        foreach (ExportedTypeHandle handle in reader.ExportedTypes)
        {
            ExportedType forwarded = reader.GetExportedType(handle);
            // CLI ExportedType Forwarder flag is 0x00200000 (not exposed in System.Reflection.TypeAttributes).
            if (((int)forwarded.Attributes & 0x00200000) != 0)
                Add(api, $"forwarded type {reader.GetString(forwarded.Namespace)}.{reader.GetString(forwarded.Name)}");
        }

        return new ExtractedAssembly(identity, new ResourceSet(assemblyName, resources), api.ToArray());
    }

    private static string ReadConstant(MetadataReader reader, ConstantHandle handle)
    {
        Constant constant = reader.GetConstant(handle);
        var blob = reader.GetBlobReader(constant.Value);
        return constant.TypeCode switch
        {
            ConstantTypeCode.Boolean => blob.ReadBoolean().ToString(),
            ConstantTypeCode.Char => ((int)blob.ReadChar()).ToString(CultureInfo.InvariantCulture),
            ConstantTypeCode.SByte => blob.ReadSByte().ToString(CultureInfo.InvariantCulture),
            ConstantTypeCode.Byte => blob.ReadByte().ToString(CultureInfo.InvariantCulture),
            ConstantTypeCode.Int16 => blob.ReadInt16().ToString(CultureInfo.InvariantCulture),
            ConstantTypeCode.UInt16 => blob.ReadUInt16().ToString(CultureInfo.InvariantCulture),
            ConstantTypeCode.Int32 => blob.ReadInt32().ToString(CultureInfo.InvariantCulture),
            ConstantTypeCode.UInt32 => blob.ReadUInt32().ToString(CultureInfo.InvariantCulture),
            ConstantTypeCode.Int64 => blob.ReadInt64().ToString(CultureInfo.InvariantCulture),
            ConstantTypeCode.UInt64 => blob.ReadUInt64().ToString(CultureInfo.InvariantCulture),
            ConstantTypeCode.Single => blob.ReadSingle().ToString("R", CultureInfo.InvariantCulture),
            ConstantTypeCode.Double => blob.ReadDouble().ToString("R", CultureInfo.InvariantCulture),
            ConstantTypeCode.String => JsonSerializer.Serialize(blob.ReadUTF16(blob.Length)),
            ConstantTypeCode.NullReference => "null",
            _ => throw new BadImageFormatException("Unsupported public constant type: " + constant.TypeCode)
        };
    }

    private static void Add(SortedSet<string> result, string text)
    {
        if (!result.Add(text)) throw new BadImageFormatException("Duplicate public API signature: " + text);
    }

    private static string? AttributeType(MetadataReader reader, EntityHandle constructor)
    {
        EntityHandle declaring = constructor.Kind switch
        {
            HandleKind.MethodDefinition => reader.GetMethodDefinition((MethodDefinitionHandle)constructor).GetDeclaringType(),
            HandleKind.MemberReference => reader.GetMemberReference((MemberReferenceHandle)constructor).Parent,
            _ => default
        };
        return declaring.Kind switch
        {
            HandleKind.TypeDefinition => SignatureText.FullTypeName(reader, (TypeDefinitionHandle)declaring),
            HandleKind.TypeReference => new SignatureText().GetTypeFromReference(reader, (TypeReferenceHandle)declaring, 0),
            _ => null
        };
    }

    private static bool VisibleType(MetadataReader reader, TypeDefinitionHandle handle)
    {
        var def = reader.GetTypeDefinition(handle);
        var parent = def.GetDeclaringType();
        TypeAttributes visibility = def.Attributes & TypeAttributes.VisibilityMask;
        if (parent.IsNil) return visibility == TypeAttributes.Public;
        return visibility is TypeAttributes.NestedPublic or TypeAttributes.NestedFamily or TypeAttributes.NestedFamORAssem &&
               VisibleType(reader, parent);
    }

    private static string? MethodVisibility(MethodAttributes attributes) => (attributes & MethodAttributes.MemberAccessMask) switch
    {
        MethodAttributes.Public => "public",
        MethodAttributes.Family => "protected",
        MethodAttributes.FamORAssem => "protected_internal",
        _ => null
    };

    private static string? FieldVisibility(FieldAttributes attributes) => (attributes & FieldAttributes.FieldAccessMask) switch
    {
        FieldAttributes.Public => "public",
        FieldAttributes.Family => "protected",
        FieldAttributes.FamORAssem => "protected_internal",
        _ => null
    };

    private static string? Accessor(MetadataReader reader, MethodDefinitionHandle handle) => handle.IsNil ? null :
        MethodVisibility(reader.GetMethodDefinition(handle).Attributes);

    private static ImmutableArray<string> GenericNames(MetadataReader reader, GenericParameterHandleCollection handles) =>
        handles.Select(h => reader.GetString(reader.GetGenericParameter(h).Name)).ToImmutableArray();

    private static string Constraints(MetadataReader reader, GenericParameterHandleCollection parameters,
        SignatureText signature, SignatureContext context)
    {
        var items = new List<string>();
        foreach (GenericParameterHandle handle in parameters)
        {
            GenericParameter parameter = reader.GetGenericParameter(handle);
            string name = reader.GetString(parameter.Name);
            string constraints = string.Join(",", parameter.GetConstraints()
                .Select(h => signature.Resolve(reader, reader.GetGenericParameterConstraint(h).Type, context))
                .OrderBy(x => x, StringComparer.Ordinal));
            items.Add($"{name}:{parameter.Attributes}:[{constraints}]");
        }
        return items.Count == 0 ? "" : " constraints=[" + string.Join(";", items) + "]";
    }
}
