# CONTEXT.md — w2d-scaffold

## Project overview

**w2d-scaffold** (W2D Scaffold) is a lightweight open-source CLI tool that generates the complete structure of a new project from a single command. It targets developers working in an LLM-assisted workflow (Claude Desktop, Claude Code) who want to enforce consistent conventions across all their projects without manual setup.

The `w2d` prefix stands for Web2Data — the author's personal brand and blog. This is an opinionated tool, not a generic scaffolding framework. It is built around a specific workflow: maintaining living documentation files that serve as context anchors for LLMs, following strict quality standards (typed Python, Conventional Commits, accessibility-first), and working in versioned phases.

## Goals

- Generate a complete, ready-to-use project structure in one command
- Enforce consistency across all projects (same LLM pilot files, same Git conventions)
- Support 6 project types out of the box: `data`, `rag`, `python`, `wordpress-plugin`, `wordpress-theme`, `astro`
- Be publishable and reusable by others (MIT licence, clean README, pytest suite)
- Serve as a reference artifact documenting the LLM-assisted project workflow

## Non-goals (v1)

- `w2d-scaffold add` — adding components to an existing project
- `w2d-scaffold doctor` — auditing an existing project
- `w2d-scaffold upgrade` — updating `_common/` files in existing projects
- Distribution via PyPI or npm
- Web UI or TUI

## Stack

| Layer           | Technology                     |
| --------------- | ------------------------------ |
| CLI             | Python + Click                 |
| Templates       | Jinja2                         |
| Command aliases | Makefile                       |
| Tests           | pytest                         |
| CI              | GitHub Actions (ruff + pytest) |
| Packaging       | pyproject.toml                 |

## Project types and their specifics

| Type               | Core stack                                          | Key generated files                                          |
| ------------------ | --------------------------------------------------- | ------------------------------------------------------------ |
| `data`             | DuckDB, dbt, medallion                              | Makefile, dbt_project.yml, profiles.yml, bronze/silver/gold/ |
| `rag`              | LlamaIndex, ChromaDB, FastAPI                       | main.py, app/ingestion.py, app/retrieval.py, app/api.py      |
| `python`           | Python typed                                        | Standard src/ layout, pyproject.toml                         |
| `wordpress-plugin` | PHP, optional ACF                                   | plugin.php, includes/, templates/, assets/                   |
| `wordpress-theme`  | PHP, Timber, ACF, SCSS                              | functions.php, templates/\*.twig, src/scss/, acf-json/       |
| `astro`            | Astro, MDX, Tailwind v4, SolidJS, Giscus, astro-seo | src/content/, src/layouts/, astro.config.mjs, src/consts.ts  |

## Common scaffold (all types)

Every generated project includes:

- `CONTEXT.md` — project description and constraints
- `NEXT_STEPS.md` — task dashboard (done / todo)
- `STRUCTURE.md` — annotated file tree
- `DECISIONS.md` — architectural decisions log
- `.gitignore` — type-specific
- `.env.example` — commented environment variables
- `README.md` — skeleton to complete

## Jinja2 variables available in all templates

| Variable                   | Description             | Example                              |
| -------------------------- | ----------------------- | ------------------------------------ |
| `{{ project_name }}`       | snake_case project name | `my_blog`                            |
| `{{ project_name_human }}` | Title Case project name | `My Blog`                            |
| `{{ description }}`        | Short description       | `Personal dev blog built with Astro` |
| `{{ author }}`             | Author name             | `Jeremy Marchandeau`                 |
| `{{ date }}`               | ISO date of generation  | `2026-03-09`                         |
| `{{ type }}`               | Project type            | `astro`                              |

## Astro template specifics

The `astro` template is derived from the battle-tested stack used on the Web2Data blog. It generates a fully wired content blog with:

- MDX + Content Collections (blog, authors, tags)
- Tailwind CSS v4 with `@theme` configuration
- SolidJS islands for interactive components (dark/light theme, mobile nav, search, Giscus comments)
- `astro.config.mjs` pre-configured with all integrations (`@astrojs/mdx`, `@astrojs/tailwind`, `@astrojs/solid-js`, `@astrojs/sitemap`, `astro-seo`)
- `src/consts.ts` as single config entry point (metadata, Giscus, navigation)

## Quality standards

- Typed Python with annotations on all functions
- Docstrings on all public functions
- English-only code, comments, and variable names
- No secrets in code (`.env.example` uses placeholders only)
- Conventional Commits format
- One branch per feature, PR for all merges

## Repository

- GitHub: `github.com/jeremy6680/w2d-scaffold`
- Package name: `w2d-scaffold`
- Main command: `w2d-scaffold new` / `make new`
- Licence: MIT
- Status: In development (v0.2 intermediate)
