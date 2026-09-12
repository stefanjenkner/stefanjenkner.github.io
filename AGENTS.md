# AGENTS.md

## Project

Static blog that powers <https://stefanjenkner.github.io>. Content lives in `content/`, the theme is the `themes/Flex` submodule, and output is generated into `output/` and deployed to GitHub Pages by `.github/workflows/github-pages.yml`.

## Build

```sh
pip install -r requirements.txt
pelican -v
```

## Dependencies

Pelican is the main dependency and drives all transitive dependencies. Pin versions in `requirements.txt` to match the Pelican release in use; do not bump transitive packages independently.

## Commits

Use semantic commit messages. Keep the summary line short. Put details as bullet points in the description.
