using System.Text.Json;

namespace AssemblyMetadata;

internal static class Program
{
    private static int Main(string[] args)
    {
        try
        {
            var inputs = new List<string>();
            string? output = null;
            for (int index = 0; index < args.Length; index++)
            {
                if (args[index] == "--assembly" && ++index < args.Length) inputs.Add(args[index]);
                else if (args[index] == "--output-dir" && ++index < args.Length) output = args[index];
                else throw new ArgumentException("Usage: --assembly <DLL-or-EXE> [--assembly ...] --output-dir <directory>");
            }
            if (inputs.Count == 0 || output is null)
                throw new ArgumentException("Supply one or more --assembly paths and --output-dir");
            if (inputs.Count > 100) throw new ArgumentException("At most 100 assemblies may be processed");

            var sources = inputs.Select(Path.GetFullPath).ToArray();
            if (sources.Distinct(StringComparer.OrdinalIgnoreCase).Count() != sources.Length)
                throw new ArgumentException("Assembly input paths must be unique");
            string outDir = Path.GetFullPath(output);
            foreach (string assemblyPath in sources)
            {
                if (!File.Exists(assemblyPath)) throw new FileNotFoundException("Assembly input missing", assemblyPath);
                if (string.Equals(outDir, Path.GetDirectoryName(assemblyPath), StringComparison.OrdinalIgnoreCase))
                    throw new ArgumentException("Output directory must differ from assembly input directory");
            }
            // No assembly is loaded; PEReader only inspects ECMA-335 tables in the files.
            ExtractedAssembly[] extracted = sources.Select(MetadataExtractor.Extract).ToArray();
            string[] names = extracted.Select(x => x.Identity.name).ToArray();
            if (names.Distinct(StringComparer.Ordinal).Count() != names.Length)
                throw new ArgumentException("Duplicate assembly names across inputs");
            var sorted = extracted.OrderBy(x => x.Identity.name, StringComparer.Ordinal).ToArray();
            var options = new JsonSerializerOptions { WriteIndented = true };
            string identityJson = JsonSerializer.Serialize(new { schema_version = 1, assemblies = sorted.Select(x => x.Identity) }, options) + "\n";
            string resourcesJson = JsonSerializer.Serialize(new { schema_version = 1, assemblies = sorted.Select(x => x.Resources) }, options) + "\n";
            string apiText = string.Join("\n", sorted.SelectMany(x => x.Api.Select(line => "assembly " + x.Identity.name + " :: " + line))
                .OrderBy(x => x, StringComparer.Ordinal)) + "\n";
            if (Directory.Exists(outDir) && Directory.EnumerateFileSystemEntries(outDir).Any())
                throw new InvalidOperationException("Output directory must be empty to prevent stale or mixed evidence");
            Directory.CreateDirectory(outDir);
            File.WriteAllText(Path.Combine(outDir, "assembly-identities.json"), identityJson);
            File.WriteAllText(Path.Combine(outDir, "resources.json"), resourcesJson);
            File.WriteAllText(Path.Combine(outDir, "public-api.txt"), apiText);
            Console.WriteLine($"Extracted {sorted.Length} assembly/assemblies, {sorted.Sum(x => x.Api.Length)} API records");
            return 0;
        }
        catch (Exception exception) when (exception is IOException or ArgumentException or BadImageFormatException or InvalidOperationException)
        {
            Console.Error.WriteLine($"Metadata extraction failed: {exception.GetType().Name}: {exception.Message}");
            return 2;
        }
    }
}
