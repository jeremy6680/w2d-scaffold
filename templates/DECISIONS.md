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
