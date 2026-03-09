# NEXT_STEPS.md — w2d-scaffold

_Last updated: 2026-03-09_

## ✅ Done

| Task                                                       | Date       |
| ---------------------------------------------------------- | ---------- |
| Rédaction du cahier des charges (CDC v0.2)                 | 2026-03-09 |
| **Phase 1 — Fondations**                                   |            |
| scaffold.py — CLI Click avec commande `new`                | 2026-03-09 |
| Makefile — `make new`, `make test`, `make lint`            | 2026-03-09 |
| requirements.txt + pyproject.toml                          | 2026-03-09 |
| templates/\_common — 7 templates Jinja2                    | 2026-03-09 |
| tests/test_scaffold.py — tests pytest phase 1              | 2026-03-09 |
| **Phase 2 — Templates data & rag**                         |            |
| Template `data` — Makefile, dbt, medallion                 | 2026-03-09 |
| Template `rag` — FastAPI, LlamaIndex, ChromaDB             | 2026-03-09 |
| Tests pytest phase 2 (data + rag)                          | 2026-03-09 |
| **Phase 3 — Templates WordPress**                          |            |
| Template `wordpress-plugin` — plugin.php, includes, assets | 2026-03-09 |
| Template `wordpress-theme` — Timber, Twig, SCSS, acf-json  | 2026-03-09 |
| Tests pytest phase 3 (wordpress-plugin + wordpress-theme)  | 2026-03-09 |
| **Phase 4 — Templates python & astro**                     |            |
| Template `python` — src/ layout, pyproject.toml, tests/    | 2026-03-09 |
| Tests pytest phase 4a (python)                             | 2026-03-09 |

## 🔜 To do

| #   | Task                                           | Priority | Notes                                                 |
| --- | ---------------------------------------------- | -------- | ----------------------------------------------------- |
| 1   | Phase 4 — Template `astro`                     | High     | Astro v5 + Tailwind v4 + SolidJS + Giscus + astro-seo |
| 2   | Tests pytest phase 4b (astro)                  | High     |                                                       |
| 3   | Phase 5 — README.md final + démo gif/asciinema | Low      |                                                       |
| 4   | Phase 5 — GitHub Actions (ruff + pytest)       | Low      | .github/workflows/ci.yml                              |
