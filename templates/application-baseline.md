# `<Application>` — Discovery baseline

**Reusable blank template.** Copy this file for every application discovery. Follow the [step-by-step guide](../methodology/technical-discovery-runbook.md) and enter results **only in the copy**.

**One field = one value.** For multiple SDKs, runtimes, frameworks, projects, packages, configurations or commands, repeat the relevant group or row rather than joining values in a single cell. Each numbered field has a consistent meaning. All values below are intentionally blank. Use `Not checked`, `Not executed`, or `Not applicable` only in the completed copy when supported by evidence.

## Discovery information

| Field | Value |
|---|---|
| 1. Discovery By |  |
| 2. Discovery Date |  |
| 3. Discovery Folder |  |

## Host and prerequisite tools

| Field | Value |
|---|---|
| 4. Operating System Name |  |
| 5. Operating System Version |  |
| 6. Operating System Build |  |
| 7. Operating System Architecture |  |
| 8. PowerShell Version |  |
| 9. Git Version |  |
| 10. .NET SDK Version |  |
| 11. .NET Runtime Version |  |
| 12. MSBuild Version |  |
| 13. MSBuild Installation Source |  |
| 14. NuGet CLI Version |  |
| 15. Targeting Pack Version |  |
| 16. Targeting Pack Installed |  |
| 17. Test Runner Name |  |
| 18. Test Runner Version |  |

## Source revision and verification

| Field | Value |
|---|---|
| 19. Selected Source Branch or Tag |  |
| 20. Source Commit SHA |  |
| 21. Working Tree Clean |  |
| 22. Detached HEAD |  |
| 23. Verification Date |  |
| 24. Evidence Status |  |

## Application overview

| Field | Value |
|---|---|
| 25. Application Name |  |
| 26. Application Purpose |  |
| 27. Application Type |  |
| 28. Repository Visibility |  |
| 29. HTTPS Clone URL |  |
| 30. SSH Clone URL |  |
| 31. Repository Default Branch |  |
| 32. License |  |
| 33. Supported Operating System |  |
| 34. Published Application Version |  |
| 35. Published Package Version |  |
| 36. Published Release URL |  |
| 37. Published Package URL |  |
| 38. Source Manifest Version |  |
| 39. Assembly Version |  |
| 40. File Version |  |
| 41. Consumer Name |  |
| 42. Application Entry Point |  |

## Solutions

Repeat this group for each solution.

| Field | Value |
|---|---|
| 43. Solution Path |  |
| 44. Solution Format |  |
| 45. Solution Format Version |  |
| 46. Declared IDE Version |  |
| 47. Solution Configuration |  |
| 48. Solution Platform |  |
| 49. Member Project Path |  |
| 50. Included in Solution Build |  |

## Projects

Repeat this group for each project, including projects outside a solution.

| Field | Value |
|---|---|
| 51. Project Path |  |
| 52. Project Role |  |
| 53. Project Format |  |
| 54. Target Framework |  |
| 55. Language Version |  |
| 56. Output Type |  |
| 57. MSBuild Platform |  |
| 58. Project SDK Declaration |  |
| 59. Project ToolsVersion |  |
| 60. Referenced Project Path |  |

## Compiler settings

Repeat for each relevant project and configuration; distinguish declared values from evaluated values.

| Field | Value |
|---|---|
| 61. Project Path |  |
| 62. Configuration Name |  |
| 63. DebugType |  |
| 64. Optimize |  |
| 65. Defined Compiler Constant |  |
| 66. Other Compiler Setting Name |  |
| 67. Other Compiler Setting Value |  |
| 68. Compiler Setting Condition |  |

## Output and validation settings

Repeat for each relevant project and configuration.

| Field | Value |
|---|---|
| 69. Project Path |  |
| 70. Configuration Name |  |
| 71. Output Path |  |
| 72. Warning Level |  |
| 73. Warnings As Errors |  |
| 74. Documentation File |  |

## Project metadata

Repeat for each project where applicable.

| Field | Value |
|---|---|
| 75. Project Path |  |
| 76. Default Configuration |  |
| 77. Is Test Project |  |
| 78. File Alignment |  |
| 79. Application Designer Folder |  |
| 80. Imported File Path |  |
| 81. Shared Property Name |  |
| 82. Shared Property Value |  |

## Evaluated MSBuild properties

Include relevant project, configuration, framework, property, result, and evidence.

| Field | Value |
|---|---|
| 83. Project Path |  |
| 84. Configuration Name |  |
| 85. Target Framework |  |
| 86. Evaluated Property Name |  |
| 87. Evaluated Property Value |  |
| 88. Declared Property Value |  |
| 89. Evaluation Evidence URL |  |

## Repository directories

Repeat for meaningful directories.

| Field | Value |
|---|---|
| 90. Directory Path |  |
| 91. Directory Purpose |  |

## Repository configuration files

Repeat for each relevant configuration file or mechanism. Record inspected absence only when verified.

| Field | Value |
|---|---|
| 92. Configuration File or Mechanism |  |
| 93. Configuration Present |  |
| 94. Configuration Purpose |  |
| 95. Configuration Value |  |
| 96. Configuration Scope |  |
| 97. Importing File Path |  |
| 98. Configuration Precedence |  |

## NuGet package declarations

Repeat for each package declaration and consuming project.

| Field | Value |
|---|---|
| 99. Consuming Project |  |
| 100. Package ID |  |
| 101. Declared Package Version |  |
| 102. Package Declaration File |  |
| 103. Configured NuGet Feed |  |
| 104. Package Purpose |  |

## Other external dependencies

Repeat for each applicable non-NuGet dependency.

| Field | Value |
|---|---|
| 105. Project Path |  |
| 106. Consuming Component |  |
| 107. Dependency Name |  |
| 108. Dependency Mechanism |  |
| 109. Dependency Type |  |
| 110. Dependency Declaration File |  |
| 111. Dependency Version |  |
| 112. Dependency Identity |  |
| 113. Dependency Resolution Status |  |
| 114. Resolved Dependency Location |  |

## Build, test and delivery commands

Use the native commands or existing workflow entry points that apply to the project.

| Field | Value |
|---|---|
| 115. Restore Command |  |
| 116. Build Command |  |
| 117. Build Configuration |  |
| 118. Build Platform |  |
| 119. Test Command |  |
| 120. Compatibility Check Command |  |
| 121. Packaging Command |  |
| 122. Consumer Verification Command |  |
| 123. Deployment Command |  |
| 124. Alternate Host Name |  |
| 125. Alternate Tool Name |  |
| 126. Alternate Tool Version |  |

## Test, CI and package details

Record actual counts and outcomes; do not infer execution from source files.

| Field | Value |
|---|---|
| 127. Tests Discovered |  |
| 128. Tests Passed |  |
| 129. Tests Failed |  |
| 130. Tests Skipped |  |
| 131. Executed Test Project |  |
| 132. Executed Test Assembly |  |
| 133. Build Warning Count |  |
| 134. Build Error Count |  |
| 135. Build Output Path |  |
| 136. CI Workflow Name |  |
| 137. CI Trigger |  |
| 138. CI Command |  |
| 139. CI Run URL |  |
| 140. CI Run Source SHA |  |
| 141. CI Run Outcome |  |
| 142. Package Contents |  |
| 143. Package Metadata |  |
| 144. Release Evidence URL |  |
| 145. Runtime Requirement |  |
| 146. Deployment Requirement |  |

## Verification outcomes

Record passed, failed, blocked, not executed, or not applicable, with evidence where available.

| Field | Value |
|---|---|
| 147. Dependency Restore Outcome |  |
| 148. Build Outcome |  |
| 149. Automated Test Outcome |  |
| 150. Public API Check Outcome |  |
| 151. Assembly Identity Check Outcome |  |
| 152. Resource Check Outcome |  |
| 153. XML Documentation Check Outcome |  |
| 154. Package Contents Check Outcome |  |
| 155. Package Metadata Check Outcome |  |
| 156. Dependency Validation Outcome |  |
| 157. Vulnerability Audit Outcome |  |
| 158. Installed-Package Consumer Check Outcome |  |
| 159. Integration Check Outcome |  |

## Executed command evidence

Repeat this group for each command actually executed, including failures.

| Field | Value |
|---|---|
| 160. Discovery Step ID |  |
| 161. Exact Command |  |
| 162. Command Working Directory |  |
| 163. Command Tool |  |
| 164. Command Result |  |
| 165. Command Exit Code |  |
| 166. Command Output Excerpt |  |
| 167. Command Evidence URL |  |

## Open gaps and findings

Repeat this group for each significant gap or finding.

| Field | Value |
|---|---|
| 168. Finding |  |
| 169. Finding Impact |  |
| 170. Finding Evidence URL |  |
| 171. Next Verification Check |  |

## Discovery step status

Repeat for each relevant DISC step.

| Field | Value |
|---|---|
| 172. Discovery Step ID |  |
| 173. Step Result |  |
| 174. Step Status |  |
| 175. Step Evidence URL |  |
| 176. Missing Information |  |

## Final review

| Field | Value |
|---|---|
| 177. Overall Baseline Disposition |  |
| 178. Reviewed By |  |
| 179. Review Date |  |
| 180. Next Action |  |
| 181. Deferred Check |  |

This baseline records observed facts, not proposed modernization work.
