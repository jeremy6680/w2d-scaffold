# w2d-scaffold — Makefile
# Unified interface for common development tasks.
# Compatible with macOS and Linux.

.PHONY: new test lint help

# Default target
help:
	@echo ""
	@echo "  w2d-scaffold — available commands"
	@echo ""
	@echo "  make new                          Interactive project wizard"
	@echo "  make new name=X type=Y [desc=Z]   Direct mode (no prompts)"
	@echo "  make test                          Run pytest suite"
	@echo "  make lint                          Run ruff linter"
	@echo ""

# ── Scaffolding ────────────────────────────────────────────────────────────

# Build the CLI arguments string from optional Make variables.
# Supported: name, type, desc (description), author, output, force
_ARGS :=
ifdef name
  _ARGS += --name "$(name)"
endif
ifdef type
  _ARGS += --type "$(type)"
endif
ifdef desc
  _ARGS += --description "$(desc)"
endif
ifdef author
  _ARGS += --author "$(author)"
endif
ifdef output
  _ARGS += --output "$(output)"
endif
ifdef force
  _ARGS += --force
endif

new:
	python scaffold.py new $(_ARGS)

# ── Quality ────────────────────────────────────────────────────────────────

test:
	python -m pytest tests/ -v

lint:
	python -m ruff check scaffold.py
```

---

### 📄 `requirements.txt`
```
w2d-scaffold/requirements.txt
```
```
click>=8.1
jinja2>=3.1
```

---

### 📄 `pyproject.toml`
```
w2d-scaffold/pyproject.toml