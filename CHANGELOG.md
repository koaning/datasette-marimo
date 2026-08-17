# Changelog

This file records the notable changes for each release. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The version numbers
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Write every entry in Simplified Technical English. Apply the
`simplified-technical-english` skill before you add or edit an entry. See
[AGENTS.md](AGENTS.md) for the rule.

## [0.2.2] - 2026-08-17

### Changed

- Change the Datasette requirement to `datasette>=0.64`. The plugin now installs on
  both the Datasette 0.x line and the 1.0 line. To install on a 1.0 alpha, use
  `pip install --pre`.
- Add a Datasette version to the CI matrix. The tests now run against a 0.x release
  and the newest 1.0 alpha. This step keeps both lines supported.

## [0.2.1] - 2026-08-14

### Changed

- Change the Datasette requirement to `datasette>=0.64,<1`. The plugin now installs
  on the Datasette 0.x line. Datasette 1.0 is still an alpha release.

## [0.2.0] - 2026-08-14

### Added

- Add an **Open in marimo** link to Datasette's top-right menu. The link reads the
  page you came from and prefills the database and table.
- Connect the notebook through the moutils `DatasetteConnection`, a native marimo
  SQL connection. The connection appears in the data-sources panel and works with
  native SQL cells.
- Add a Database dropdown and a Table dropdown to the notebook. The query updates
  when you change either one.

### Changed

- Lead the notebook with the moutils connection. Hide the setup and connection
  code, so the notebook shows the result and not the plumbing.
- Point the GitHub Pages demo at `https://datasette.exe.xyz`.
- Slim the plugin dependencies to `datasette`. Each notebook declares its own
  dependencies in its inline script metadata.
- Keep the older `Datasette` helper class (`get_polars` / `sql_polars`) for
  backward compatibility. Fold its code away in the notebook.
