// EXP-036: isolated research-only managed Windows PDB reader.
// Compile TWICE with /define:DNLIB or /define:CECIL against pinned, verified DLLs.
// Never reference or activate native COM reader. Fixture files are trusted local inputs.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
#if DNLIB
using dnlib.DotNet;
using dnlib.DotNet.Pdb;
#else
using Mono.Cecil;
using Mono.Cecil.Pdb;
#endif

internal static class ReaderProbe
{
    private static readonly Dictionary<string, string> Documents =
        new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

    private static readonly HashSet<string> Missing = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

    private static void Add(string url, Guid algorithm, byte[] digest)
    {
        if (string.IsNullOrWhiteSpace(url))
            throw new InvalidDataException("Empty source document path");
        var name = Path.GetFileName(url);
        if (string.IsNullOrEmpty(name) || name == url && (url.Contains("/") || url.Contains("\\")))
            throw new InvalidDataException("Unexpected document path");
        if (digest == null || digest.Length == 0)
        {
            if (Documents.ContainsKey(name))
                throw new InvalidDataException("Conflicting missing and present digests");
            Missing.Add(name);
            return;
        }
        if (Missing.Contains(name))
            throw new InvalidDataException("Conflicting missing and present digests");
        var hex = BitConverter.ToString(digest).Replace("-", "").ToLowerInvariant();
        var record = algorithm.ToString("D") + "\t" + hex;
        if (Documents.ContainsKey(name) && Documents[name] != record)
            throw new InvalidDataException("Conflicting document checksum for same basename");
        Documents[name] = record;
    }

    private static void Inspect(string dll, string pdb)
    {
#if DNLIB
        using (var module = ModuleDefMD.Load(dll, new ModuleCreationOptions {
            TryToLoadPdbFromDisk = false, PdbOptions = PdbReaderOptions.None
        }))
        {
            module.LoadPdb(PdbReaderOptions.None, pdb);
            if (module.PdbState == null)
                throw new InvalidDataException("dnlib failed to initialize managed PDB state");
            foreach (var doc in module.PdbState.Documents)
                Add(doc.Url, doc.CheckSumAlgorithmId, doc.CheckSum);
        }
#else
        using (var module = ModuleDefinition.ReadModule(dll, new ReaderParameters {
            ReadSymbols = true,
            ThrowIfSymbolsAreNotMatching = true,
            SymbolReaderProvider = new NativePdbReaderProvider()
        }))
        {
            foreach (var type in module.Types)
                ReadType(type);
        }
#endif
    }

#if !DNLIB
    private static void ReadType(TypeDefinition type)
    {
        foreach (var method in type.Methods)
        {
            var points = method.DebugInformation.SequencePoints;
            if (points == null) continue;
            foreach (var point in points)
            {
                if (point.Document == null) continue;
                Add(point.Document.Url, point.Document.HashAlgorithmGuid, point.Document.Hash);
            }
        }
        foreach (var nested in type.NestedTypes)
            ReadType(nested);
    }
#endif

    private static int Main(string[] args)
    {
        if (args.Length != 2 || !File.Exists(args[0]) || !File.Exists(args[1]))
        {
            Console.Error.WriteLine("USAGE: ReaderProbe <dll> <pdb>");
            return 10;
        }
        try
        {
            if (new FileInfo(args[0]).Length > 10 * 1024 * 1024 ||
                new FileInfo(args[1]).Length > 16 * 1024 * 1024)
                throw new InvalidDataException("Inputs outside bounded size policy");
            Inspect(args[0], args[1]);
            if (Process.GetCurrentProcess().Modules.Cast<ProcessModule>().Any(m =>
                m.ModuleName.IndexOf("diasymreader", StringComparison.OrdinalIgnoreCase) >= 0))
                throw new InvalidDataException("Native DiaSymReader module loaded unexpectedly");
            if (Documents.Count == 0 && Missing.Count == 0)
                throw new InvalidDataException("Reader returned zero source documents");
            foreach (var pair in Documents.OrderBy(x => x.Key, StringComparer.Ordinal))
                Console.WriteLine("DOC\t" + pair.Key + "\t" + pair.Value);
            foreach (var name in Missing.OrderBy(x => x, StringComparer.Ordinal))
                Console.WriteLine("MISSING\t" + name);
            Console.WriteLine("END\t" + Documents.Count + "\t" + Missing.Count);
            return 0;
        }
        catch (Exception ex)
        {
            // Never emit absolute temporary paths or untrusted diagnostic strings.
            var detail = "OTHER";
            if (ex.Message == "Empty source document path") detail = "EMPTY_DOCUMENT_PATH";
            else if (ex.Message == "Unexpected document path") detail = "BAD_DOCUMENT_PATH";
            else if (ex.Message == "Conflicting document checksum for same basename") detail = "CONFLICTING_DIGESTS";
            else if (ex.Message == "Conflicting missing and present digests") detail = "CONFLICTING_MISSING_DIGESTS";
            else if (ex.Message == "Reader returned zero source documents") detail = "NO_DOCUMENTS";
            else if (ex.Message == "dnlib failed to initialize managed PDB state") detail = "DNLIB_NO_PDB_STATE";
            Console.Error.WriteLine("READER_ERROR\t" + ex.GetType().Name + "\t" + detail);
            return 11;
        }
    }
}
