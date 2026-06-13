# GitHub Pages

This page explains how to publish the Fonky MkDocs site to GitHub Pages after the local
documentation build is clean.

The expected deployment path is:

```text
Local source files
    -> MkDocs build
    -> Git commit
    -> mkdocs gh-deploy
    -> GitHub Pages
```

## Purpose

GitHub Pages allows the generated Fonky documentation site to be hosted directly from the GitHub
repository.

Use this workflow only after the local documentation site builds successfully.

Required local validation:

```powershell
python -m compileall .
mkdocs build
```

Do not deploy until source compilation and documentation generation are clean.

## Prerequisites

Confirm the following are available:

| Requirement                | Purpose                                                    |
| -------------------------- | ---------------------------------------------------------- |
| GitHub repository          | Hosts the Fonky source and documentation.                  |
| Git                        | Pushes source commits and deployment branch changes.       |
| Python virtual environment | Runs the MkDocs toolchain.                                 |
| MkDocs                     | Builds the static documentation site.                      |
| Material for MkDocs        | Provides the documentation theme.                          |
| mkdocstrings               | Renders Python API documentation from source docstrings.   |
| Clean local build          | Confirms documentation can be generated before deployment. |

## Repository Settings

The repository should contain:

```text
Fonky/
|-- mkdocs.yml
|-- README.md
|-- requirements.txt
|-- docs/
|   |-- index.md
|   |-- getting-started.md
|   |-- configuration.md
|   |-- architecture.md
|   |-- logging.md
|   |-- usage.md
|   |-- user-guide.md
|   |-- development.md
|   |-- github-pages.md
|   |-- api/
|   |-- stylesheets/
|   +-- javascripts/
|-- loaders.py
|-- fetchers.py
|-- processors.py
|-- models.py
+-- ...
```

The `site/` directory is generated output. It does not need to be committed when deploying with
`mkdocs gh-deploy`.

## MkDocs Site Configuration

The top of `mkdocs.yml` should identify the project and repository.

Example:

```yaml
site_name: Fonky Documentation
site_description: Documentation for the Fonky Python framework.
site_author: Terry D. Eppler
site_url: https://YOUR-GITHUB-USERNAME.github.io/Fonky/

repo_url: https://github.com/YOUR-GITHUB-USERNAME/Fonky
repo_name: YOUR-GITHUB-USERNAME/Fonky
```

Replace `YOUR-GITHUB-USERNAME` with the actual GitHub account or organization name.

The `site_url` value should match the GitHub Pages URL.

## Required Theme Assets

If the project uses custom styling and JavaScript, `mkdocs.yml` should include:

```yaml
extra_css:
  - stylesheets/extra.css

extra_javascript:
  - javascripts/extra.js
```

Expected files:

```text
docs/stylesheets/extra.css
docs/javascripts/extra.js
```

If either file is referenced in `mkdocs.yml`, the file must exist.

## Required Plugin Configuration

The documentation build must include mkdocstrings.

For the current flat source layout, the handler path should include the repository root:

```yaml
plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths:
            - .
          options:
            docstring_style: google
            show_source: true
            show_root_heading: true
            show_root_full_path: false
            show_signature: true
            show_signature_annotations: true
            separate_signature: true
            merge_init_into_class: false
            members_order: source
            filters:
              - "!^_"
            heading_level: 2
```

This allows API pages such as `docs/api/loaders.md` to render:

```text
::: loaders
```

Because the current source layout is flat, do not use:

```text
::: fonky.loaders
```

unless the project is moved into a real package directory named `fonky`.

## Navigation Configuration

The `nav` section should include all manual and API pages you expect users to see.

Example:

```yaml
nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Configuration: configuration.md
  - Architecture: architecture.md
  - Logging: logging.md
  - Usage: usage.md
  - User Guide: user-guide.md
  - Development: development.md
  - GitHub Pages: github-pages.md
  - API Reference:
      - Overview: api/index.md
      - Archives: api/archives.md
      - Astronomical: api/astronomical.md
      - Boogr: api/boogr.md
      - Cloud: api/cloud.md
      - Configuration: api/config.md
      - Core: api/core.md
      - Demographic: api/demographic.md
      - Documents: api/documents.md
      - Environmental: api/environmental.md
      - Fetchers: api/fetchers.md
      - Geospatial: api/geospatial.md
      - Health: api/health.md
      - Loaders: api/loaders.md
      - Models: api/models.md
      - Processors: api/processors.md
      - Scrapers: api/scrapers.md
      - Web: api/web.md
```

If MkDocs warns that pages exist but are not included in `nav`, either add them to `nav` or remove
the unused files.

## Local Validation Before Deployment

Run these commands from the repository root.

Compile Python source:

```powershell
python -m compileall .
```

Confirm API pages contain live mkdocstrings directives:

```powershell
Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Confirm manual pages do not contain live mkdocstrings directives:

```powershell
Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Expected result for manual pages:

```text
No output.
```

Build the site:

```powershell
mkdocs build
```

Serve locally:

```powershell
mkdocs serve
```

Open the local site:

```text
http://127.0.0.1:8000/
```

Review the rendered site before deployment.

## Clean Generated Output

MkDocs generates the local static site in:

```text
site/
```

It is safe to remove and rebuild:

```powershell
Remove-Item -Recurse -Force .\site -ErrorAction SilentlyContinue
mkdocs build
```

The `site/` directory should normally stay out of normal source commits when using
`mkdocs gh-deploy`.

## Commit Source Changes

Before deployment, review changes:

```powershell
git status
```

Stage documentation and source updates:

```powershell
git add .
```

Commit the changes:

```powershell
git commit -m "Update Fonky documentation"
```

Push the source branch:

```powershell
git push
```

This preserves the source documentation files in the repository before publishing the generated
site.

## Deploy with MkDocs

Deploy to GitHub Pages using:

```powershell
mkdocs gh-deploy --force
```

This command builds the documentation and pushes the generated static site to the `gh-pages` branch.

Expected result:

```text
The gh-pages branch is created or updated.
The generated documentation site is published from that branch.
```

## Configure GitHub Pages

In the GitHub repository:

```text
Settings
    -> Pages
    -> Build and deployment
```

Use these settings:

| Setting | Value                |
| ------- | -------------------- |
| Source  | Deploy from a branch |
| Branch  | `gh-pages`           |
| Folder  | `/ (root)`           |

Save the settings.

GitHub may take a few minutes to publish the updated site.

## Confirm the Published Site

The published site should normally be available at:

```text
https://YOUR-GITHUB-USERNAME.github.io/Fonky/
```

If `site_url` is configured correctly in `mkdocs.yml`, links, canonical URLs, and repository
metadata should align with the GitHub Pages URL.

## Add a Documentation Badge

A README badge can point users to the hosted documentation.

Example:

```markdown
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-024FA3)](https://YOUR-GITHUB-USERNAME.github.io/Fonky/)
```

Place the badge near the top of `README.md`, close to the project title and other project badges.

## README Documentation Link

Add a clear documentation link near the top of the README:

```markdown
[Open the Fonky Documentation](https://YOUR-GITHUB-USERNAME.github.io/Fonky/)
```

If the link routes back to the README instead of the MkDocs site, check the GitHub Pages settings
and confirm that the Pages source is the `gh-pages` branch, not the default branch.

## Common Deployment Problems

### GitHub Pages opens the README instead of the MkDocs site

Likely cause:

```text
GitHub Pages is set to deploy from the default branch instead of the gh-pages branch.
```

Fix:

```text
Settings
    -> Pages
    -> Source: Deploy from a branch
    -> Branch: gh-pages
    -> Folder: / (root)
```

Then redeploy:

```powershell
mkdocs gh-deploy --force
```

### CSS or JavaScript does not load

Likely causes:

```text
- docs/stylesheets/extra.css does not exist.
- docs/javascripts/extra.js does not exist.
- mkdocs.yml references the wrong path.
- The browser is showing cached assets.
```

Confirm the files exist:

```powershell
Test-Path .\docs\stylesheets\extra.css
Test-Path .\docs\javascripts\extra.js
```

Expected output:

```text
True
True
```

### API pages are blank

Likely causes:

```text
- The API page lacks a live mkdocstrings directive.
- The directive uses the wrong import path.
- The source module cannot be imported.
- A required dependency is missing at import time.
```

For the current flat source layout, an API page should use:

```text
::: loaders
```

not:

```text
::: fonky.loaders
```

### Duplicate API target warnings appear

Likely cause:

```text
A top-level manual page contains a live mkdocstrings directive.
```

Find accidental directives:

```powershell
Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"
```

Manual pages should return no output.

### Build fails with Griffe docstring warnings

Common causes:

```text
- Untyped Returns section.
- Returns: None included.
- Args section contains prose instead of name-type-description entries.
- Attributes section contains prose instead of name-type-description entries.
```

Correct return format:

```text
Returns:
    list[str]: Supported option values.
```

Correct argument format:

```text
Args:
    path (str): Path to the file.
```

For procedures that do not return a value, omit `Returns:`.

## Deployment Checklist

Before running `mkdocs gh-deploy --force`, confirm:

| Check                                   | Command                                                           |
| --------------------------------------- | ----------------------------------------------------------------- |
| Source compiles                         | `python -m compileall .`                                          |
| Manual pages contain no live directives | `Select-String -Path .\docs\*.md -Pattern "^:::\s+[A-Za-z_]"`     |
| API pages contain live directives       | `Select-String -Path .\docs\api\*.md -Pattern "^:::\s+[A-Za-z_]"` |
| Documentation builds                    | `mkdocs build`                                                    |
| Documentation serves locally            | `mkdocs serve`                                                    |
| Git working tree reviewed               | `git status`                                                      |
| Source changes committed                | `git add .; git commit -m "Update Fonky documentation"`           |
| Source branch pushed                    | `git push`                                                        |
| Site deployed                           | `mkdocs gh-deploy --force`                                        |
| GitHub Pages source set                 | `gh-pages` branch, root folder                                    |
| Published URL tested                    | Open GitHub Pages URL                                             |

## Recommended Deployment Sequence

Use this exact sequence:

```powershell
python -m compileall . 
mkdocs build
mkdocs serve
```

After reviewing the local site:

```powershell
git status
git add .
git commit -m "Update Fonky documentation"
git push
mkdocs gh-deploy --force
```

Then verify GitHub Pages settings and open the published documentation URL.

## Final State

A successful GitHub Pages deployment means:

```text
- Source files are committed on the default branch.
- The generated static site is published on the gh-pages branch.
- GitHub Pages is configured to serve from gh-pages.
- The README points users to the documentation site.
- The documentation URL opens the MkDocs site, not the README.
- API reference pages render source docstrings through mkdocstrings.
```
