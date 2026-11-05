# EXP-028 — Source Link maps to frozen remote Git file bytes

**Scope:** Read-only provenance verification; no application edits. Draft stacked on EXP-027/026/025/024; current evidence pending until CI completes.

After real manual Source Link candidate CSV compilation and all original acceptance gates, parse actual native Windows PDB Source Link JSON and DLL CodeView identity via EXP-025. Select one **known tracked production source** (`src/RecordSift.Infrastructure.Csv/CsvStreamImporterAdapter.cs`). Apply the single wildcard mapping to the candidate's deterministic `/_/` document path, require raw HTTPS URL on exact `raw.githubusercontent.com/infoconex/RecordSift/8358780829458854a4b0356df5ac5e685f0a34c8/` origin, fetch only this allowlisted exact file and compare remote bytes against unchanged local tracked Git checkout (SHA-256 and complete bytes). Reject redirects, wrong commits, hosts, extra path/query, untracked source, traversal and changed bytes.

Eleven synthetic path safety tests run on Windows and Ubuntu. Keep only summary JSON (relative path, size/hash/commit, verified status) in CI evidence. No source bytes, binaries, PDBs, package archives, credentials, or binlogs uploaded.

**Do not overclaim:** This proves only one selected Source Link URL's provenance and byte parity, not the PDB C13 document checksum records for all compiled documents, actual Visual Studio step-through, detached HEAD/shallow clone or nested authentic Git submodule behavior. Additional separate controls required. No main branch changes, package publish or automatic adoption.

References: [EXP-025](EXP-025-windows-pdb-identity.md), [EXP-024](EXP-024-sourcelink-windows-import.md), [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37).
