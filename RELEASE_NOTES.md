# KUMIHAN Japanese 0.2.0 source candidate

Japanese typography guidance now includes source-backed writing and type context,
task-specific recipes, and an experimental evidence schema. The four standalone
Skills retain the 39 canonical rule IDs, six media profiles, seven review states,
and source-preserving review policy. Other language editions are independent.

This source version is 0.2.0. The verified published version remains 0.1.8 until
the new GitHub Release and all fifteen downloads have been verified.

New 0.2.0 packages exclude internal development reports and MCP server/configuration
files. Existing 0.1.8 downloads remain unchanged.

## Known limitations

- These packages provide guidance and bounded evidence tools, not automatic
  Japanese line breaking or a general typography compliance certificate.
- Of the original 30 acceptance scenarios, 15 were partially run and 15 were not
  run. Subsequent focused checks do not convert whole scenarios to passed.
- Historical LibreOfficeDev 26.8 alpha PDF exports with the original fonts showed
  text extraction/spacing failures, including inserted spaces in slide export.
  Exact saved presentation XML does not establish exact exported PDF text.
- Browser evidence covers the recorded Chromium viewports and CSS scaling only.
  Native browser zoom, all browsers, assistive-technology speech, native Microsoft
  Office rendering/editability, physical projection and readership remain unverified.
- Actual installation and invocation of all four Skills in each supported AI host
  have not been accepted. No Marketplace certification or MCP deployment is implied.
