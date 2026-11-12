using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text.Json;
using Microsoft.DiaSymReader;

internal static class Program
{
    private static readonly Guid Sha1Guid = new("ff1816ec-aa5e-4d10-87f7-6f4963833460");
    private static readonly Guid Sha256Guid = new("8829d00f-11b8-4213-878b-770e8597ac16");

    private sealed class NoMetadataSignatures : ISymReaderMetadataProvider
    {
        public unsafe bool TryGetStandaloneSignature(int token, out byte* signature, out int length)
        {
            signature = null;
            length = 0;
            return false;
        }

        public bool TryGetTypeDefinitionInfo(int token, out string namespaceName, out string typeName, out TypeAttributes attributes)
        {
            namespaceName = string.Empty;
            typeName = string.Empty;
            attributes = default;
            return false;
        }

        public bool TryGetTypeReferenceInfo(int token, out string namespaceName, out string typeName)
        {
            namespaceName = string.Empty;
            typeName = string.Empty;
            return false;
        }
    }

    private sealed record DocumentSummary(string RelativePath, string Algorithm, int ChecksumLength,
                                          bool WorkingTreeChecksumMatched, int WorkingTreeBytes);

    private static bool CheckDigest(byte[] bytes, Guid algorithm, byte[] digest)
    {
        if (digest.Length == 0)
        {
            return false;
        }

        byte[] actual;
        if (algorithm == Sha1Guid)
        {
            actual = SHA1.HashData(bytes);
        }
        else if (algorithm == Sha256Guid)
        {
            actual = SHA256.HashData(bytes);
        }
        else
        {
            return false;
        }

        return CryptographicOperations.FixedTimeEquals(actual, digest);
    }

    private static void SelfTest()
    {
        var input = System.Text.Encoding.UTF8.GetBytes("managed PDB verification fixture");
        var sha1 = SHA1.HashData(input);
        var sha256 = SHA256.HashData(input);
        Require(CheckDigest(input, Sha1Guid, sha1), "SHA1 positive");
        Require(CheckDigest(input, Sha256Guid, sha256), "SHA256 positive");
        Require(!CheckDigest(input, Sha1Guid, sha256), "SHA algorithm confusion negative");
        Require(!CheckDigest(input, Guid.Empty, sha1), "unknown algorithm negative");
        Require(!CheckDigest(input, Sha1Guid, Array.Empty<byte>()), "empty checksum negative");
        var corrupted = (byte[])input.Clone();
        corrupted[0] ^= 1;
        Require(!CheckDigest(corrupted, Sha1Guid, sha1), "wrong source bytes negative");
        var badDigest = (byte[])sha256.Clone();
        badDigest[0] ^= 1;
        Require(!CheckDigest(input, Sha256Guid, badDigest), "wrong checksum record negative");
        Console.WriteLine("PASS: 7 deterministic source checksum match/mismatch controls.");
    }

    private static void Require(bool condition, string reason)
    {
        if (!condition)
        {
            throw new InvalidOperationException(reason);
        }
    }

    private static string SafeRelativeSource(string url)
    {
        var normalized = url.Replace('\\', '/');
        const string virtualRoot = "/_/src/";
        if (!normalized.StartsWith(virtualRoot, StringComparison.Ordinal))
        {
            throw new InvalidDataException("Unsupported PDB document source root");
        }

        var relative = normalized[3..]; // drops '/_/' and retains src/...
        if (relative.Contains("..", StringComparison.Ordinal) ||
            relative.Contains("//", StringComparison.Ordinal) ||
            relative.IndexOfAny(['?', '#', '\0', ':']) >= 0)
        {
            throw new InvalidDataException("PDB document path is not a safe tracked source path");
        }

        return relative;
    }

    private static object Verify(string pdb, string root)
    {
        var canonicalRoot = Path.GetFullPath(root);
        Require(Directory.Exists(canonicalRoot), "Frozen source root missing");
        Require(File.Exists(pdb), "Native PDB missing");
        using var stream = File.OpenRead(pdb);
        var reader = SymUnmanagedReaderFactory.CreateReader<ISymUnmanagedReader3>(
            stream, new NoMetadataSignatures(), SymUnmanagedReaderCreationOptions.UseAlternativeLoadPath);
        try
        {
            var hr = reader.GetDocuments(0, out int docCount, null!);
            Marshal.ThrowExceptionForHR(hr);
            Require(docCount >= 1 && docCount <= 300, "Unexpected native Windows PDB document count");
            var documents = new ISymUnmanagedDocument[docCount];
            hr = reader.GetDocuments(docCount, out int returned, documents);
            Marshal.ThrowExceptionForHR(hr);
            Require(returned == docCount, "PDB document count changed during enumeration");
            var summary = new List<DocumentSummary>();
            var names = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var doc in documents)
            {
                Require(doc != null, "Null native document entry");
                var relative = SafeRelativeSource(doc.GetUrl());
                Require(names.Add(relative), "Duplicate PDB document filename");
                var sourcePath = Path.GetFullPath(Path.Combine(canonicalRoot, relative.Replace('/', Path.DirectorySeparatorChar)));
                Require(sourcePath.StartsWith(canonicalRoot + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase),
                        "PDB document path escaped frozen source checkout");
                Require(File.Exists(sourcePath), "PDB document is not a physical source file");
                var original = File.ReadAllBytes(sourcePath);
                Require(original.Length is > 0 and < 1048576, "PDB source document violates input budget");
                var guid = doc.GetChecksumAlgorithmId();
                var checksum = doc.GetChecksum();
                var algo = guid == Sha1Guid ? "SHA1" : guid == Sha256Guid ? "SHA256" : "unsupported";
                var equal = CheckDigest(original, guid, checksum);
                summary.Add(new DocumentSummary(relative, algo, checksum.Length, equal, original.Length));
            }

            Require(summary.Any(d => d.RelativePath == "src/RecordSift.Infrastructure.Csv/CsvStreamImporterAdapter.cs"),
                    "Selected Source Link document missing from native PDB");
            Require(summary.All(d => d.Algorithm != "unsupported" && d.WorkingTreeChecksumMatched),
                    "One or more source-document checksum records missing or do not match compiler input bytes");
            return new
            {
                schema_version = 1,
                experiment = "EXP-031",
                interface_used = "Microsoft.DiaSymReader ISymUnmanagedReader3/ISymUnmanagedDocument",
                document_count = summary.Count,
                sha1_document_count = summary.Count(d => d.Algorithm == "SHA1"),
                sha256_document_count = summary.Count(d => d.Algorithm == "SHA256"),
                all_physical_compiler_source_bytes_match_pdb_checksums = true,
                documents = summary,
                important_limitations = new[]
                {
                    "PDB metadata checksums are compared against actual Windows compiler input files, not Git LF blobs.",
                    "This does not prove Visual Studio debugger UI source stepping.",
                    "This standalone research-only process does not install DiaSymReader into RecordSift."
                }
            };
        }
        finally
        {
            if (reader is IDisposable disposable)
            {
                disposable.Dispose();
            }
            else if (Marshal.IsComObject(reader))
            {
                Marshal.ReleaseComObject(reader);
            }
        }
    }

    private static int Main(string[] args)
    {
        try
        {
            if (args.Length == 1 && args[0] == "--self-test")
            {
                SelfTest();
                return 0;
            }

            if (args.Length != 3)
            {
                Console.Error.WriteLine("Usage: PdbDocumentHashes <PDB> <frozen application root> <new JSON output>");
                return 3;
            }

            Require(!File.Exists(args[2]), "Refusing overwrite of evidence");
            var report = Verify(args[0], args[1]);
            var json = JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true });
            Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(args[2]))!);
            File.WriteAllText(args[2], json + Environment.NewLine);
            Console.WriteLine("Verified native managed PDB checksum records against exact Windows source bytes.");
            return 0;
        }
        catch (Exception exception)
        {
            // Do not include raw file paths or source bytes in CI output.
            Console.Error.WriteLine("PDB document checksum gate failed closed: " + exception.GetType().Name);
            return 2;
        }
    }
}
