using System.Collections.Immutable;
using System.Reflection.Metadata;

namespace AssemblyMetadata;

internal sealed record SignatureContext(ImmutableArray<string> TypeParameters, ImmutableArray<string> MethodParameters)
{
    public static SignatureContext Empty { get; } = new([], []);
}

// Only decodes ECMA-335 signatures; never loads or executes dependencies.
internal sealed class SignatureText : ISignatureTypeProvider<string, SignatureContext>
{
    public string GetArrayType(string elementType, ArrayShape shape) =>
        $"{elementType}[rank={shape.Rank};sizes={string.Join(",", shape.Sizes)};lower={string.Join(",", shape.LowerBounds)}]";
    public string GetByReferenceType(string elementType) => elementType + "&";
    public string GetFunctionPointerType(MethodSignature<string> signature) =>
        $"fnptr({string.Join(",", signature.ParameterTypes)})->{signature.ReturnType}";
    public string GetGenericInstantiation(string genericType, ImmutableArray<string> typeArguments) =>
        genericType + "<" + string.Join(",", typeArguments) + ">";
    public string GetGenericMethodParameter(SignatureContext context, int index) =>
        index < context.MethodParameters.Length ? context.MethodParameters[index] : "!!" + index;
    public string GetGenericTypeParameter(SignatureContext context, int index) =>
        index < context.TypeParameters.Length ? context.TypeParameters[index] : "!" + index;
    public string GetModifiedType(string modifier, string unmodifiedType, bool isRequired) =>
        $"{unmodifiedType} mod{(isRequired ? "req" : "opt")}({modifier})";
    public string GetPinnedType(string elementType) => "pinned " + elementType;
    public string GetPointerType(string elementType) => elementType + "*";
    public string GetPrimitiveType(PrimitiveTypeCode typeCode) => typeCode switch
    {
        PrimitiveTypeCode.Void => "System.Void",
        PrimitiveTypeCode.Boolean => "System.Boolean",
        PrimitiveTypeCode.Char => "System.Char",
        PrimitiveTypeCode.SByte => "System.SByte",
        PrimitiveTypeCode.Byte => "System.Byte",
        PrimitiveTypeCode.Int16 => "System.Int16",
        PrimitiveTypeCode.UInt16 => "System.UInt16",
        PrimitiveTypeCode.Int32 => "System.Int32",
        PrimitiveTypeCode.UInt32 => "System.UInt32",
        PrimitiveTypeCode.Int64 => "System.Int64",
        PrimitiveTypeCode.UInt64 => "System.UInt64",
        PrimitiveTypeCode.Single => "System.Single",
        PrimitiveTypeCode.Double => "System.Double",
        PrimitiveTypeCode.String => "System.String",
        PrimitiveTypeCode.TypedReference => "System.TypedReference",
        PrimitiveTypeCode.IntPtr => "System.IntPtr",
        PrimitiveTypeCode.UIntPtr => "System.UIntPtr",
        PrimitiveTypeCode.Object => "System.Object",
        _ => throw new BadImageFormatException($"Unsupported primitive code: {typeCode}")
    };
    public string GetSZArrayType(string elementType) => elementType + "[]";
    public string GetTypeFromDefinition(MetadataReader reader, TypeDefinitionHandle handle, byte rawTypeKind) =>
        FullTypeName(reader, handle);
    public string GetTypeFromReference(MetadataReader reader, TypeReferenceHandle handle, byte rawTypeKind) =>
        FullReferenceName(reader, handle);
    public string GetTypeFromSpecification(MetadataReader reader, SignatureContext context,
        TypeSpecificationHandle handle, byte rawTypeKind) =>
        reader.GetTypeSpecification(handle).DecodeSignature(this, context);

    internal static string FullTypeName(MetadataReader reader, TypeDefinitionHandle handle)
    {
        TypeDefinition type = reader.GetTypeDefinition(handle);
        string name = reader.GetString(type.Name);
        TypeDefinitionHandle parent = type.GetDeclaringType();
        if (!parent.IsNil) return FullTypeName(reader, parent) + "+" + name;
        string ns = reader.GetString(type.Namespace);
        return string.IsNullOrEmpty(ns) ? name : ns + "." + name;
    }

    private static string FullReferenceName(MetadataReader reader, TypeReferenceHandle handle)
    {
        TypeReference type = reader.GetTypeReference(handle);
        string name = reader.GetString(type.Name);
        if (type.ResolutionScope.Kind == HandleKind.TypeReference)
            return FullReferenceName(reader, (TypeReferenceHandle)type.ResolutionScope) + "+" + name;
        string ns = reader.GetString(type.Namespace);
        return string.IsNullOrEmpty(ns) ? name : ns + "." + name;
    }

    public string Resolve(MetadataReader reader, EntityHandle handle, SignatureContext context) => handle.Kind switch
    {
        HandleKind.TypeDefinition => GetTypeFromDefinition(reader, (TypeDefinitionHandle)handle, 0),
        HandleKind.TypeReference => GetTypeFromReference(reader, (TypeReferenceHandle)handle, 0),
        HandleKind.TypeSpecification => GetTypeFromSpecification(reader, context, (TypeSpecificationHandle)handle, 0),
        HandleKind.Nil => "",
        _ => throw new BadImageFormatException($"Unsupported type handle: {handle.Kind}")
    };
}
