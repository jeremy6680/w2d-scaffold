# W2D Scaffold

> Generate a complete, LLM-ready project structure in one command.

[![CI](https://github.com/jeremy6680/w2d-scaffold/actions/workflows/ci.yml/badge.svg)](https://github.com/jeremy6680/w2d-scaffold/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)

W2D Scaffold is an opinionated CLI tool that scaffolds new projects with a
consistent structure tailored for **LLM-assisted workflows** (Claude Desktop,
Claude Code). Every generated project includes the four LLM pilot files
(`CONTEXT.md`, `NEXT_STEPS.md`, `STRUCTURE.md`, `DECISIONS.md`), a
type-specific file tree, and sane Git defaults — ready in under a second.

---

## Features

- **6 project types** out of the box: `data`, `rag`, `python`,
  `wordpress-plugin`, `wordpress-theme`, `astro`
- **Interactive wizard** (`make new`) or **direct mode** (`make new name=X type=Y`)
- **Jinja2 templates** — readable, well-commented, easy to fork and adapt
- **Zero boilerplate at runtime** — only Click and Jinja2 as dependencies
- **pytest suite** covering all 6 types + GitHub Actions CI

---

## Requirements

- Python 3.12+
- `make` (available by default on macOS and Linux)

---

## Installation

```bash
git clone https://github.com/jeremy6680/w2d-scaffold.git
cd w2d-scaffold
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
pip install -r requirements.txt
```

---

## Usage

### Interactive wizard

```bash
make new
```

```
> Project name? my-blog
> Project type? [data/rag/python/wordpress-plugin/wordpress-theme/astro] astro
> Short description? Personal dev blog built with Astro
> Author? Jeremy Marchandeau
> Create ./my-blog/? [Y/n] Y

✅ Project 'my-blog' created at ./my-blog/
```

### Direct mode

```bash
make new name=my-blog type=astro description="Personal dev blog" author="Jeremy Marchandeau"
```

### Via Python directly

```bash
python scaffold.py new --name my-blog --type astro --description "Personal dev blog" --author "Jeremy Marchandeau"
```

### Output to a specific directory

```bash
python scaffold.py new --name my-blog --type astro --output-dir ~/projects
```

---

## Project types

| Type               | Stack                                  | Key generated files                                                   |
| ------------------ | -------------------------------------- | --------------------------------------------------------------------- |
| `data`             | DuckDB, dbt, medallion                 | `Makefile`, `dbt/dbt_project.yml`, `dbt/models/bronze\|silver\|gold/` |
| `rag`              | LlamaIndex, ChromaDB, FastAPI          | `main.py`, `app/ingestion.py`, `app/retrieval.py`, `app/api.py`       |
| `python`           | Typed Python, hatchling                | `src/<name>/`, `pyproject.toml`, `tests/test_main.py`                 |
| `wordpress-plugin` | PHP, optional ACF                      | `<name>.php`, `includes/`, `templates/`, `assets/`                    |
| `wordpress-theme`  | PHP, Timber, ACF, SCSS                 | `functions.php`, `templates/*.twig`, `src/scss/`, `acf-json/`         |
| `astro`            | Astro v5, Tailwind v4, SolidJS, Giscus | `src/content/`, `src/layouts/`, `astro.config.mjs`, `src/consts.ts`   |

Every type also generates the **common scaffold**:

| File            | Purpose                                             |
| --------------- | --------------------------------------------------- |
| `CONTEXT.md`    | Project overview, goals, stack — LLM context anchor |
| `NEXT_STEPS.md` | Task dashboard (done / todo)                        |
| `STRUCTURE.md`  | Annotated file tree                                 |
| `DECISIONS.md`  | Architectural decisions log                         |
| `.gitignore`    | Type-specific ignore rules                          |
| `.env.example`  | Commented environment variables (no secrets)        |
| `README.md`     | Skeleton to complete                                |

---

## Jinja2 variables

All templates have access to these variables at render time:

| Variable                   | Description             | Example                              |
| -------------------------- | ----------------------- | ------------------------------------ |
| `{{ project_name }}`       | snake_case project name | `my_blog`                            |
| `{{ project_name_human }}` | Title Case project name | `My Blog`                            |
| `{{ description }}`        | Short description       | `Personal dev blog built with Astro` |
| `{{ author }}`             | Author full name        | `Jeremy Marchandeau`                 |
| `{{ date }}`               | ISO date of generation  | `2026-03-09`                         |
| `{{ type }}`               | Project type            | `astro`                              |

---

## Development

### Run tests

```bash
make test
# or
python -m pytest tests/ -v
```

### Lint

```bash
make lint
# or
ruff check scaffold.py tests/
```

### Add a new project type

1. Create `templates/<type>/` with your `.j2` template files.
2. Add the type string to `VALID_TYPES` in `scaffold.py`.
3. Add a test class in `tests/test_scaffold.py`.
4. Update this README.

Use `PROJECT_NAME` in a template filename to have it resolved to the
snake_case project name at generation time (e.g. `PROJECT_NAME.php.j2` →
`my_plugin.php`). Use `PROJECT_SLUG` for the kebab-case equivalent.

---

## Repository structure

```
w2d-scaffold/
├── scaffold.py              # CLI entrypoint (Click)
├── Makefile                 # make new / make test / make lint
├── requirements.txt         # Click, Jinja2
├── pyproject.toml           # Python packaging config
├── templates/
│   ├── _common/             # Shared templates (all types)
│   ├── data/
│   ├── rag/
│   ├── python/
│   ├── wordpress-plugin/
│   ├── wordpress-theme/
│   └── astro/
├── tests/
│   └── test_scaffold.py
├── CONTEXT.md
├── NEXT_STEPS.md
├── STRUCTURE.md
└── DECISIONS.md
```

---

## Licence

MIT — see [LICENSE](LICENSE).

Built by [Jeremy Marchandeau](https://web2data.fr) · [Web2Data](https://web2data.fr)
