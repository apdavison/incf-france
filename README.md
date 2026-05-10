# Neuroinformatics in France

Static website providing a directory of neuroinformatics researchers and software projects in France, served at [www.neuroinfo.fr](https://www.neuroinfo.fr) via GitHub Pages.

## Structure

```
build.py          # Build script: renders Jinja2 templates → docs/
parse_data.py     # Loads and resolves relationships from data_all.json
data_all.json     # Source data (researchers, teams, labs, projects)
site_templates/   # Jinja2 HTML templates
static/           # CSS
media/            # Images, icons, PDFs
docs/             # Built output (served by GitHub Pages)
```

## Building the site

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py
```

The built site is written to `docs/`. Commit the `docs/` directory to deploy via GitHub Pages.

## Adding or updating content

All content comes from `data_all.json`. Edit that file and re-run `python build.py`.

To add French descriptions for a researcher or project, populate the `interests_fr` or `long_description_fr` fields in `data_all.json`. If left empty, the English text is shown in both languages.

For structural or layout changes, edit the templates in `site_templates/` and rebuild.


## History

This site was previously implemented with Django and AngularJS.
The previous implementation is available in the Git history.
