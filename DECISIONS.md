## Dynamic template filenames

**Date:** 2026-03-09
**Status:** Accepted

**Context:**
Some generated files must be named after the project (e.g. `my_plugin.php`
for a WordPress plugin). Jinja2 cannot dynamically name files — it only
renders file _contents_.

**Decision:**
Template files whose output name depends on `project_name` use a literal
placeholder in their filename:

- `PROJECT_NAME` → `project_name` (snake_case, e.g. `my_plugin`)
- `PROJECT_SLUG` → kebab-case slug (e.g. `my-plugin`)

`scaffold.py::resolve_output_filename()` replaces these at copy time.

**Alternatives considered:**

- Naming templates with Jinja2 syntax in the filename → not supported by
  the filesystem or Jinja2's FileSystemLoader.
- A separate rename manifest file → adds indirection for minimal gain.

**Consequences:**

- Template filenames are readable and self-documenting.
- No special config needed — the convention is visible in the filename itself.

---

## Placeholder resolution applies to directory segments, not only filenames

**Date:** 2026-03-09
**Status:** Accepted

**Context:**
The `python` template requires a subdirectory named after the project:
`src/PROJECT_NAME/`. The original `resolve_output_filename()` only resolved
placeholders in the final filename segment (the last part of the path),
leaving intermediate directory names unresolved.

**Decision:**
Introduce `resolve_output_path(relative, project_name)` which applies
`resolve_output_filename()` to **every segment** of the relative path, not
just the last one. `copy_type_templates()` now strips the `.j2` suffix first,
then delegates the full path resolution to `resolve_output_path()`.

**Alternatives considered:**

- Keeping a single `resolve_output_filename()` and applying it to all parts
  inline → works, but merging the two concerns into one function reduces
  clarity.
- A manifest file mapping template paths to output paths → adds indirection
  and maintenance overhead for a problem that the naming convention already
  solves elegantly.

**Consequences:**

- Any template can now use `PROJECT_NAME` or `PROJECT_SLUG` in directory
  names at any depth — no additional configuration needed.
- The fix is backward-compatible: existing templates with no placeholders
  in directory names are unaffected.

---

## pyproject.toml as the Python template build backend

**Date:** 2026-03-09
**Status:** Accepted

**Context:**
The `python` template needs a modern, standards-compliant packaging
configuration. Several build backends are available (setuptools, flit,
hatchling, pdm-backend).

**Decision:**
Use `hatchling` as the build backend in `pyproject.toml`. It is the default
backend for Hatch, requires zero extra configuration for a standard `src/`
layout, and is fully PEP 517/518 compliant.

**Alternatives considered:**

- `setuptools` → still the most widespread, but requires more boilerplate
  (`[tool.setuptools.packages.find]`) for a `src/` layout.
- `flit` → clean, but opinionated about import-based versioning.
- `pdm-backend` → excellent, but tied to the PDM workflow.

**Consequences:**

- Generated projects are immediately publishable to PyPI with `hatch build`.
- `[tool.pytest.ini_options] pythonpath = ["src"]` allows `python -m pytest`
  without `pip install -e .`, consistent with the project constraint of
  testability without a global install.
