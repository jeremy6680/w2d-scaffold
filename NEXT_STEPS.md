# NEXT_STEPS.md — w2d-scaffold

_Last updated: 2026-03-09_

## ✅ Done

| Task                                            | Date       |
| ----------------------------------------------- | ---------- |
| Rédaction du cahier des charges (CDC v0.2)      | 2026-03-09 |
| **Phase 1 — Fondations**                        |            |
| scaffold.py — CLI Click avec commande `new`     | 2026-03-09 |
| Makefile — `make new`, `make test`, `make lint` | 2026-03-09 |
| requirements.txt + pyproject.toml               | 2026-03-09 |
| templates/\_common — 7 templates Jinja2         | 2026-03-09 |
| tests/test_scaffold.py — tests pytest phase 1   | 2026-03-09 |

## 🔜 To do

| #   | Task                                            | Priority | Notes                                                       |
| --- | ----------------------------------------------- | -------- | ----------------------------------------------------------- |
| 1   | Phase 2 — Template `data` (dbt + medallion)     | High     | Makefile, dbt_project.yml, profiles.yml, bronze/silver/gold |
| 2   | Phase 2 — Template `rag` (LlamaIndex + FastAPI) | High     | main.py, app/, data/raw, data/processed, requirements.txt   |
| 3   | Phase 3 — Template `wordpress-plugin`           | Medium   | plugin.php, includes/, templates/, assets/                  |
| 4   | Phase 3 — Template `wordpress-theme`            | Medium   | functions.php, Twig templates, SCSS, acf-json/              |
| 5   | Phase 4 — Template `python`                     | Medium   | src/ layout, pyproject.toml, tests/                         |
| 6   | Phase 4 — Template `astro`                      | Medium   | Astro v5 + Tailwind v4 + SolidJS + Giscus + astro-seo       |
| 7   | Phase 5 — README.md final + démo gif/asciinema  | Low      |                                                             |
| 8   | Phase 5 — GitHub Actions (ruff + pytest)        | Low      | .github/workflows/ci.yml                                    |
