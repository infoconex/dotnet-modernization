# RecordSift — Discovery baseline (blank copy)

**Blank copy for RecordSift.** This copy has not been filled in. Follow the [step-by-step guide](../../../../methodology/technical-discovery-runbook.md) to evaluate each numbered field; write answers **only in your copy**.

All values are intentionally blank. Keep the numbers unchanged. For groups marked **Repeat**, add another copy of that two-column group for each solution, project, package, command, or other applicable item. Use *Not checked*, *Not executed*, or *Not applicable* when those are the actual outcomes. Link evidence and omit secrets.

## Discovery information

| Field | Value |
|---|---|
| 1. Discovery By |  |
| 2. Discovery Date |  |
| 3. Discovery Folder |  |

## Host and prerequisite tools

| Field | Value |
|---|---|
| 4. Operating System, Version, Build and Architecture |  |
| 5. PowerShell Version |  |
| 6. Git Version |  |
| 7. .NET SDK and Runtime Versions |  |
| 8. MSBuild Version and Installation |  |
| 9. NuGet CLI Version |  |
| 10. .NET Framework Targeting Packs |  |
| 11. Test Runner and Version |  |

## Source revision and verification

| Field | Value |
|---|---|
| 12. Selected Source Branch or Tag |  |
| 13. Source Commit SHA |  |
| 14. Local Checkout Status |  |
| 15. Verification Date |  |
| 16. Evidence Status |  |

## Application overview

| Field | Value |
|---|---|
| 17. Application name |  |
| 18. Application Purpose and Type |  |
| 19. Repository Visibility |  |
| 20. HTTPS clone URL |  |
| 21. SSH clone URL, if used |  |
| 22. Repository default branch |  |
| 23. License |  |
| 24. Supported Operating Systems |  |
| 25. Published Application or Package Version |  |
| 26. Published Release or Package URL |  |
| 27. Source manifest version |  |
| 28. Assembly version |  |
| 29. File version |  |
| 30. Consumers or entry points |  |

## Solutions

Repeat this group for each solution.

| Field | Value |
|---|---|
| 31. Solution path |  |
| 32. Format |  |
| 33. Format version |  |
| 34. Declared IDE version |  |
| 35. Configurations |  |
| 36. Platforms |  |
| 37. Solution membership/build exclusions |  |

## Projects

Repeat this group for each project, including projects outside a solution.

| Field | Value |
|---|---|
| 38. Project path |  |
| 39. Role |  |
| 40. Project format |  |
| 41. Target framework(s) |  |
| 42. Language version |  |
| 43. Output type |  |
| 44. MSBuild Platform |  |
| 45. SDK / ToolsVersion |  |
| 46. Direct project references |  |

## Compiler settings

Repeat for each relevant project and configuration; distinguish declared values from evaluated values.

| Field | Value |
|---|---|
| 47. Project/configuration |  |
| 48. DebugType |  |
| 49. Optimize |  |
| 50. DefineConstants |  |
| 51. Other compiler settings / conditions |  |

## Output and validation settings

Repeat for each relevant project and configuration.

| Field | Value |
|---|---|
| 52. Project/configuration |  |
| 53. OutputPath |  |
| 54. WarningLevel |  |
| 55. WarningsAsErrors |  |
| 56. DocumentationFile |  |

## Project metadata

Repeat for each project where applicable.

| Field | Value |
|---|---|
| 57. Project |  |
| 58. Default configuration |  |
| 59. IsTestProject |  |
| 60. FileAlignment |  |
| 61. AppDesignerFolder |  |
| 62. Imports / shared properties |  |

## Evaluated MSBuild properties

Include relevant project, configuration, framework, property, result, and evidence.

| Field | Value |
|---|---|
| 63. Evaluated MSBuild Properties and Differences |  |

## Repository directories

Repeat for meaningful directories.

| Field | Value |
|---|---|
| 64. Directory |  |
| 65. Purpose |  |

## Repository configuration files

Repeat for each relevant configuration file or mechanism. Record inspected absence only when verified.

| Field | Value |
|---|---|
| 66. File / mechanism |  |
| 67. Present? |  |
| 68. Current purpose / value |  |
| 69. Scope, imports or precedence |  |

## NuGet package declarations

Repeat for each package declaration and consuming project.

| Field | Value |
|---|---|
| 70. Project |  |
| 71. Package ID |  |
| 72. Version |  |
| 73. Declared in |  |
| 74. Configured feed(s) |  |
| 75. Purpose |  |

## Other external dependencies

Repeat for each applicable non-NuGet dependency.

| Field | Value |
|---|---|
| 76. Project/consumer |  |
| 77. Dependency |  |
| 78. Mechanism/type |  |
| 79. Source file |  |
| 80. Version/identity |  |
| 81. Resolution/location |  |

## Build, test and delivery commands

Use the native commands or existing workflow entry points that apply to the project.

| Field | Value |
|---|---|
| 82. Restore |  |
| 83. Build (configuration/platform) |  |
| 84. Full tests |  |
| 85. Compatibility checks |  |
| 86. Packaging |  |
| 87. Consumer/deployment |  |
| 88. Alternate host/CI toolchain details |  |

## Test, CI and package details

Record actual counts and outcomes; do not infer execution from source files.

| Field | Value |
|---|---|
| 89. Tests discovered |  |
| 90. Tests passed |  |
| 91. Tests failed |  |
| 92. Tests skipped |  |
| 93. Test projects/assemblies actually executed |  |
| 94. Build warnings/errors and important outputs |  |
| 95. CI workflow names, triggers and commands |  |
| 96. CI runs checked and their exact source SHA |  |
| 97. Package contents/metadata and release evidence |  |
| 98. Runtime / deployment requirements |  |

## Verification outcomes

Record passed, failed, blocked, not executed, or not applicable, with evidence where available.

| Field | Value |
|---|---|
| 99. Dependency restore |  |
| 100. Build |  |
| 101. Automated tests |  |
| 102. Public API |  |
| 103. Assembly identity |  |
| 104. Resources |  |
| 105. XML documentation |  |
| 106. Package contents |  |
| 107. Package metadata |  |
| 108. Dependency validation |  |
| 109. Vulnerability audit |  |
| 110. Installed-package consumer |  |
| 111. Application integration checks |  |

## Executed command evidence

Repeat this group for each command actually executed, including failures.

| Field | Value |
|---|---|
| 112. Step |  |
| 113. Exact command, scope and tool |  |
| 114. Result and exit code |  |
| 115. Output / evidence link |  |

## Open gaps and findings

Repeat this group for each significant gap or finding.

| Field | Value |
|---|---|
| 116. Gap or finding |  |
| 117. Impact |  |
| 118. Evidence / next check |  |

## Discovery step status

Repeat for each relevant DISC step.

| Field | Value |
|---|---|
| 119. Step |  |
| 120. Result/status |  |
| 121. Evidence or missing information |  |

## Final review

| Field | Value |
|---|---|
| 122. Overall Baseline Disposition |  |
| 123. Report reviewed by/date |  |
| 124. Next action or deferred checks |  |

The baseline records observed facts and execution outcomes, not proposed modernization work.
