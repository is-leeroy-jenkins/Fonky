# ðŸš€ GitHub Pages

This page explains how to publish the Fonky MkDocs site to GitHub Pages after the documentation
builds cleanly on the local machine.

Do not deploy until `mkdocs build` succeeds without unresolved page, import, mkdocstrings, Griffe,
or broken-link warnings that affect the rendered site.



## ðŸŽ¯ Deployment Goal

The goal is to publish the MkDocs-generated documentation site so users can access Fonky
documentation from the repositoryâ€™s GitHub Pages URL.

Expected documentation URL:

```text id="github_pages_url"
https://is-leeroy-jenkins.github.io/Fonky/
```

The exact URL depends on the GitHub username or organization and repository name.



## âœ… Prerequisites

Before deploying, confirm:

| Requirement                                           | Why it matters                                       |
| ----------------------------------------------------- | ---------------------------------------------------- |
| Git repository exists on GitHub                       | GitHub Pages deploys from the remote repository.     |
| Local repository is clean enough to deploy            | Avoid deploying stale or broken documentation.       |
| `mkdocs.yml` exists at repo root                      | MkDocs needs the site configuration.                 |
| `docs/` exists                                        | MkDocs needs Markdown source pages.                  |
| `docs/api/*.md` pages contain mkdocstrings directives | API docstrings render only through `:::` directives. |
| MkDocs dependencies are installed                     | `mkdocs gh-deploy` must be available.                |
| Local `mkdocs build` passes                           | Deploy only a known-good build.                      |



## ðŸ“¦ Install Documentation Dependencies

Install the documentation toolchain in the active virtual environment:

```powershell id="install_docs_dependencies"
python -m pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions
```

Recommended `requirements.txt` section:

```text id="requirements_docs_section"
# Documentation
mkdocs
mkdocs-material
mkdocstrings
mkdocstrings-python
pymdown-extensions
```

Install from `requirements.txt` when the dependencies are recorded there:

```powershell id="install_requirements"
python -m pip install -r requirements.txt
```



## ðŸ§ª Validate Source Before Building Docs

Run a Python compile check from the repository root:

```powershell id="compile_source"
python -m compileall .
```

For targeted checks:

```powershell id="targeted_compile"
python -m py_compile .\boogr.py
python -m py_compile .\config.py
python -m py_compile .\core.py
python -m py_compile .\archives.py
python -m py_compile .\fetchers.py
python -m py_compile .\loaders.py
python -m py_compile .\models.py
python -m py_compile .\processors.py
python -m py_compile .\scrapers.py
```

A clean compile confirms syntax validity. It does not confirm every optional API provider or
credential is configured.



## ðŸ”Œ Confirm API Pages Render Source Docstrings

The API pages must contain mkdocstrings directives.

Check all API pages:

```powershell id="check_api_directives"
Select-String -Path .\docs\api\*.md -Pattern "^:::"
```

Expected output should include entries similar to:

```text id="api_directive_expected_output"
docs\api\loaders.md:3:::: loaders
docs\api\fetchers.md:3:::: fetchers
docs\api\processors.md:3:::: processors
docs\api\models.md:3:::: models
```

If no directives are found, the API pages will not render Python docstrings.

For flat source layout, API pages should use:

```markdown id="flat_api_directive"
`::: loaders`
```

For package layout, API pages should use:

```markdown id="package_api_directive"
`::: loaders`
```



## âš™ï¸ Confirm `mkdocs.yml`

The repository root should contain:

```text id="mkdocs_file"
mkdocs.yml
```

Confirm it exists:

```powershell id="confirm_mkdocs_yml"
Test-Path .\mkdocs.yml
```

The file should include:

```yaml id="site_url_example"
site_url: https://is-leeroy-jenkins.github.io/Fonky/
```

It should also include the mkdocstrings plugin:

```yaml id="mkdocstrings_plugin_required"
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

Do not include:

```yaml id="invalid_custom_dir"
custom_dir: null
```

Use `custom_dir` only when there is an actual theme override directory.



## ðŸ—ï¸ Build the Site Locally

Build the documentation site:

```powershell id="mkdocs_build"
mkdocs build
```

A successful build creates:

```text id="site_directory"
site/
```

The `site/` folder is generated output. It should not usually be committed when using
`mkdocs gh-deploy`.



## ðŸ‘€ Serve and Review Locally

Start a local documentation server:

```powershell id="mkdocs_serve"
mkdocs serve
```

Open:

```text id="local_site_url"
http://127.0.0.1:8000/
```

Review at least:

| Page            | What to confirm                                                             |
| --------------- | --------------------------------------------------------------------------- |
| Home            | Landing page renders and links work.                                        |
| Getting Started | Setup steps are clear and command blocks render correctly.                  |
| Configuration   | Environment variables and logging paths are clear.                          |
| Architecture    | Module flow and responsibilities are understandable.                        |
| Logging         | Exception pattern and SQLite logging details are correct.                   |
| User Guide      | Examples render without autorefs warnings.                                  |
| API Reference   | mkdocstrings renders modules, classes, methods, signatures, and docstrings. |
| GitHub Pages    | Deployment instructions match the repository.                               |

Stop the server with:

```text id="stop_server"
Ctrl+C
```



## ðŸ§¯ Resolve Common Build Problems Before Deployment

### `custom_dir` `NoneType` error

Problem:

```text id="custom_dir_error"
TypeError: expected str, bytes or os.PathLike object, not NoneType
```

Cause:

```yaml id="bad_custom_dir_config"
custom_dir: null
```

Fix: remove the line.

Correct:

```yaml id="correct_theme_config"
theme:
  name: material
  language: en
```



### API pages are blank

Cause: API page lacks mkdocstrings directive.

Bad:

```markdown id="blank_api_page_bad"
# Loaders API

This page describes loaders.
```

Good:

```markdown id="api_page_good"
# Loaders API

`::: loaders`
```

or, for package layout:

```markdown id="api_page_package_good"
# Loaders API

`::: loaders`
```



### mkdocstrings cannot import a module

Possible causes:

```text id="import_causes"
- The directive path does not match the source layout.
- The build is not being run from the repository root.
- A dependency required at import time is missing.
- A source file has syntax errors.
```

Check imports:

```powershell id="check_imports"
python -c "import loaders; import fetchers; import processors; import models; print('imports passed')"
```

For package layout:

```powershell id="check_package_imports"
python -c "import fonky.loaders; import fonky.fetchers; import fonky.processors; import fonky.models; print('package imports passed')"
```



### Griffe warning: no type for returned value

Bad:

```text id="bad_return_docstring"
Returns:
	Supported option values.
```

Good:

```text id="good_return_docstring"
Returns:
	list[str]: Supported option values.
```

For functions that do not return a value, omit `Returns:`.



### Griffe warning: failed to get `name: description` pair

Bad:

```text id="bad_args_docstring"
Args:
	Request parameters.
```

Good:

```text id="good_args_docstring"
Args:
	params (dict[str, object]): Request parameters for the active call.
```

If there is no specific argument or attribute to document, omit the section.



### Autorefs warning for `0` or `:1000`

Cause: Markdown interprets Python bracket syntax as reference links in some contexts.

Avoid:

```python id="autorefs_bad"
print(documents[0].page_content[:1000])
```

Use:

```python id="autorefs_good"
for document in documents:
	print(document.page_content)
	break
```



## ðŸš¢ Deploy to GitHub Pages

After local build and review pass, deploy:

```powershell id="gh_deploy"
mkdocs gh-deploy --force
```

This command builds the site and pushes the generated site content to the `gh-pages` branch.

Expected behavior:

```text id="gh_deploy_behavior"
- MkDocs builds the documentation.
- The generated site is committed to the gh-pages branch.
- The gh-pages branch is pushed to GitHub.
```



## âš™ï¸ Configure GitHub Repository Settings

In GitHub:

1. Open the repository.
2. Go to **Settings**.
3. Select **Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select the branch:

```text id="pages_branch"
gh-pages
```

6. Select the folder:

```text id="pages_folder"
/
```

7. Save the settings.

GitHub may take a few minutes to publish or refresh the site.



## ðŸ”Ž Confirm the Published Site

After deployment, open:

```text id="published_site"
https://is-leeroy-jenkins.github.io/Fonky/
```

Confirm:

| Check                  | Expected result                                                             |
| ---------------------- | --------------------------------------------------------------------------- |
| Home page loads        | The documentation landing page appears.                                     |
| Navigation works       | Top-level and API pages are accessible.                                     |
| API pages render       | Source docstrings appear under classes and methods.                         |
| Theme renders          | Material for MkDocs layout, navigation, search, and code copy buttons work. |
| Links work             | No major broken internal links.                                             |
| GitHub repo link works | The repository link points to the correct GitHub repository.                |



## ðŸ§­ Confirm GitHub Pages Branch

Check branches:

```powershell id="git_branch_all"
git branch -a
```

You should see a remote branch similar to:

```text id="gh_pages_branch"
remotes/origin/gh-pages
```

Check status:

```powershell id="git_status_after_deploy"
git status
```

The working tree for your main branch should remain under your control. The generated site is
managed on `gh-pages`.



## ðŸ§¾ Commit Source Documentation Changes

`mkdocs gh-deploy` publishes the generated site, but you still need to commit source documentation
changes to the normal branch.

Check status:

```powershell id="git_status"
git status
```

Stage source documentation and configuration:

```powershell id="git_add_docs"
git add mkdocs.yml docs requirements.txt README.md
```

If source docstrings were changed:

```powershell id="git_add_source"
git add *.py
```

Commit:

```powershell id="git_commit_docs"
git commit -m "Build Fonky MkDocs documentation"
```

Push the normal branch:

```powershell id="git_push_main"
git push
```



## ðŸ” Standard Update Workflow

Use this workflow whenever documentation changes:

```text id="standard_update_workflow"
1. Edit source docstrings or Markdown pages.
2. Run python -m compileall .
3. Run mkdocs build.
4. Fix Python, Griffe, mkdocstrings, autorefs, or link warnings.
5. Run mkdocs serve.
6. Review locally.
7. Commit source documentation changes.
8. Run mkdocs gh-deploy --force.
9. Confirm the published GitHub Pages site.
```



## ðŸ§ª Full Validation Command Set

From the repository root:

```powershell id="full_validation"
python -m compileall .
Select-String -Path .\docs\api\*.md -Pattern "^:::"
mkdocs build
mkdocs serve
```

Deploy only after the local build is clean:

```powershell id="deploy_after_clean_build"
mkdocs gh-deploy --force
```



## âœ… Deployment Checklist

| Check                                | Command or location                                   |
| ------------------------------------ | ----------------------------------------------------- |
| Virtual environment active           | Prompt begins with `(.venv)`                          |
| Documentation dependencies installed | `python -m pip install -r requirements.txt`           |
| Source compiles                      | `python -m compileall .`                              |
| API pages contain directives         | `Select-String -Path .\docs\api\*.md -Pattern "^:::"` |
| MkDocs builds                        | `mkdocs build`                                        |
| Local site reviewed                  | `mkdocs serve`                                        |
| GitHub Pages deployed                | `mkdocs gh-deploy --force`                            |
| GitHub Pages branch selected         | GitHub repository Settings â†’ Pages                    |
| Published site reviewed              | `https://is-leeroy-jenkins.github.io/Fonky/`          |
| Source docs committed                | `git add ...; git commit ...; git push`               |



## âž¡ï¸ Next Step

After deployment, continue normal development by updating source docstrings and Markdown pages
together. Rebuild locally before every GitHub Pages deployment.


