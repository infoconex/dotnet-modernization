using System.Globalization;
using System.Reflection.Metadata;
using System.Reflection.Metadata.Ecma335;
using System.Reflection.PortableExecutable;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace PeProvenance;

internal static class Program
{
    private const long MaxInputBytes = 512L * 1024 * 1024;

    private static int Main(string[] args)
    {
        try
        {
            var input = new List<string>();
            string? output = null;
            for (int index = 0; index < args.Length; index++)
            {
                if (args[index] == "--assembly" && ++index < args.Length) input.Add(args[index]);
                else if (args[index] == "--output" && ++index < args.Length) output = args[index];
                else throw new ArgumentException("Usage: --assembly <managed-dll> [--assembly ...] --output <new-json-file>");
            }
            if (input.Count == 0 || input.Count > 100 || string.IsNullOrWhiteSpace(output))
                throw new ArgumentException("Expected 1-100 assembly paths and a JSON output file");
            var sources = input.Select(Path.GetFullPath).ToArray();
            if (sources.Distinct(StringComparer.OrdinalIgnoreCase).Count() != sources.Length)
                throw new ArgumentException("Assembly paths must be unique");
            string destination = Path.GetFullPath(output);
            if (File.Exists(destination)) throw new ArgumentException("Refusing to overwrite existing evidence");
            if (sources.Contains(destination, StringComparer.OrdinalIgnoreCase))
                throw new ArgumentException("Output must not overwrite an input DLL");
            foreach (string path in sources)
            {
                if (string.Equals(Path.GetDirectoryName(path), Path.GetDirectoryName(destination),
                    StringComparison.OrdinalIgnoreCase))
                    throw new ArgumentException("Evidence must not be written next to an assembly");
            }
            var records = sources.Select(Inspect).OrderBy(x => x.assembly, StringComparer.Ordinal).ToArray();
            if (records.Select(x => x.assembly).Distinct(StringComparer.Ordinal).Count() != records.Length)
                throw new ArgumentException("Duplicate CLR assembly names in input");
            Directory.CreateDirectory(Path.GetDirectoryName(destination)!);
            File.WriteAllText(destination, JsonSerializer.Serialize(new
            {
                schema_version = 1,
                kind = "managed-pe-provenance",
                source_policy = "hash and CLR metadata only; never load or execute assembly",
                assemblies = records
            }, new JsonSerializerOptions { WriteIndented = true, DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull }) + "\n",
                new UTF8Encoding(false));
            Console.WriteLine($"Captured {records.Length} managed PE files with MVID, COFF, debug/PDB pointers and raw method IL hashes.");
            return 0;
        }
        catch (Exception e) when (e is IOException or ArgumentException or InvalidOperationException or
                                      BadImageFormatException or NotSupportedException)
        {
            Console.Error.WriteLine($"PE evidence failed: {e.GetType().Name}: {e.Message}");
            return 2;
        }
    }

    private static object Inspect(string path)
    {
        using FileStream stream = File.OpenRead(path);
        if (stream.Length > MaxInputBytes) throw new InvalidDataException("Managed PE exceeds 512 MiB");
        long length = stream.Length;
        string fileHash = Convert.ToHexString(SHA256.HashData(stream)).ToLowerInvariant();
        stream.Position = 0;
        using var pe = new PEReader(stream, PEStreamOptions.LeaveOpen);
        if (!pe.HasMetadata || pe.PEHeaders.CorHeader is null)
            throw new BadImageFormatException("Expected a managed assembly, not a native PE");
        MetadataReader reader = pe.GetMetadataReader();
        if (!reader.IsAssembly) throw new BadImageFormatException("Module without assembly metadata");
        string name = reader.GetString(reader.GetAssemblyDefinition().Name);
        Guid moduleId = reader.GetGuid(reader.GetModuleDefinition().Mvid);
        var debug = new List<object>();
        foreach (DebugDirectoryEntry entry in pe.ReadDebugDirectory())
        {
            string? codeViewGuid = null;
            int? codeViewAge = null;
            string? pdbFileName = null;
            string? pdbPathHash = null;
            if (entry.Type == DebugDirectoryEntryType.CodeView)
            {
                CodeViewDebugDirectoryData value = pe.ReadCodeViewDebugDirectoryData(entry);
                codeViewGuid = value.Guid.ToString("D");
                codeViewAge = value.Age;
                // Never upload an absolute source or PDB path; hash the complete path,
                // expose only the basename for reproducibility diagnosis.
                pdbFileName = Path.GetFileName(value.Path.Replace('\\', '/'));
                pdbPathHash = Convert.ToHexString(
                    SHA256.HashData(Encoding.UTF8.GetBytes(value.Path))).ToLowerInvariant();
            }
            debug.Add(new
            {
                type = entry.Type.ToString(),
                stamp = entry.Stamp.ToString("X8", CultureInfo.InvariantCulture),
                major = entry.MajorVersion,
                minor = entry.MinorVersion,
                data_size = entry.DataSize,
                codeview_guid = codeViewGuid,
                codeview_age = codeViewAge,
                pdb_filename = pdbFileName,
                pdb_path_sha256 = pdbPathHash
            });
        }
        var methodBodies = new SortedDictionary<string, object>(StringComparer.Ordinal);
        long ilBytes = 0;
        foreach (MethodDefinitionHandle handle in reader.MethodDefinitions)
        {
            MethodDefinition method = reader.GetMethodDefinition(handle);
            if (method.RelativeVirtualAddress == 0) continue;
            byte[] bytes = pe.GetMethodBody(method.RelativeVirtualAddress).GetILBytes().ToArray();
            ilBytes += bytes.Length;
            string token = MetadataTokens.GetToken(handle).ToString("X8", CultureInfo.InvariantCulture);
            methodBodies.Add(token, new
            {
                name = reader.GetString(method.Name),
                size = bytes.Length,
                sha256 = Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant()
            });
        }
        return new
        {
            assembly = name,
            filename = Path.GetFileName(path),
            bytes = length,
            file_sha256 = fileHash,
            assembly_version = reader.GetAssemblyDefinition().Version.ToString(),
            mvid = moduleId.ToString("D"),
            coff_timestamp_hex = pe.PEHeaders.CoffHeader.TimeDateStamp.ToString("X8", CultureInfo.InvariantCulture),
            pe_kind = pe.PEHeaders.PEHeader?.Magic.ToString(),
            method_body_count = methodBodies.Count,
            method_il_total_bytes = ilBytes,
            method_bodies = methodBodies,
            debug_directory = debug
        };
    }
}
