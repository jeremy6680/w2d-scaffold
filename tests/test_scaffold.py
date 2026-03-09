"""
Tests for w2d-scaffold — Phase 1: common scaffold generation.

Validates that the _common templates are correctly rendered for every
supported project type.
"""

import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from scaffold import cli, to_snake_case, to_title_case

# ---------------------------------------------------------------------------
# Unit tests — helper functions
# ---------------------------------------------------------------------------


def test_to_snake_case_basic() -> None:
    """Hyphenated names are converted to snake_case."""
    assert to_snake_case("my-blog") == "my_blog"


def test_to_snake_case_spaces() -> None:
    """Names with spaces are converted to snake_case."""
    assert to_snake_case("My Blog Project") == "my_blog_project"


def test_to_snake_case_already_snake() -> None:
    """Already snake_case names are returned unchanged."""
    assert to_snake_case("my_blog") == "my_blog"


def test_to_title_case_snake() -> None:
    """snake_case names are converted to Title Case."""
    assert to_title_case("my_blog") == "My Blog"


def test_to_title_case_hyphen() -> None:
    """Hyphenated names are converted to Title Case."""
    assert to_title_case("my-blog") == "My Blog"


# ---------------------------------------------------------------------------
# Common files — generated for every project type
# ---------------------------------------------------------------------------

COMMON_FILES = [
    "CONTEXT.md",
    "NEXT_STEPS.md",
    "STRUCTURE.md",
    "DECISIONS.md",
    "README.md",
    ".gitignore",
    ".env.example",
]

VALID_TYPES = [
    "data",
    "rag",
    "python",
    "wordpress-plugin",
    "wordpress-theme",
    "astro",
]


@pytest.fixture()
def runner() -> CliRunner:
    """Return a Click test runner."""
    return CliRunner()


@pytest.mark.parametrize("project_type", VALID_TYPES)
def test_common_files_exist(
    runner: CliRunner,
    tmp_path: Path,
    project_type: str,
) -> None:
    """All _common files are generated for every project type."""
    result = runner.invoke(
        cli,
        [
            "new",
            "--name", "test_project",
            "--type", project_type,
            "--description", "A test project",
            "--author", "Test Author",
            "--output", str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output

    project_dir = tmp_path / "test_project"
    for filename in COMMON_FILES:
        assert (project_dir / filename).exists(), (
            f"Missing '{filename}' for type '{project_type}'"
        )


@pytest.mark.parametrize("project_type", VALID_TYPES)
def test_jinja2_variables_interpolated(
    runner: CliRunner,
    tmp_path: Path,
    project_type: str,
) -> None:
    """Jinja2 variables are correctly interpolated in CONTEXT.md."""
    result = runner.invoke(
        cli,
        [
            "new",
            "--name", "my_project",
            "--type", project_type,
            "--description", "Test description",
            "--author", "Jeremy Marchandeau",
            "--output", str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output

    context_md = (tmp_path / "my_project" / "CONTEXT.md").read_text()

    assert "My Project" in context_md        # project_name_human
    assert "Test description" in context_md  # description
    assert "Jeremy Marchandeau" in context_md  # author
    assert "{{" not in context_md            # no unrendered tags


def test_force_flag_overwrites_existing(
    runner: CliRunner,
    tmp_path: Path,
) -> None:
    """--force overwrites an existing project directory."""
    # First run
    runner.invoke(
        cli,
        ["new", "--name", "my_project", "--type", "python",
         "--description", "x", "--author", "x", "--output", str(tmp_path)],
    )
    # Second run without --force should fail
    result = runner.invoke(
        cli,
        ["new", "--name", "my_project", "--type", "python",
         "--description", "x", "--author", "x", "--output", str(tmp_path)],
    )
    assert result.exit_code != 0

    # Third run with --force should succeed
    result = runner.invoke(
        cli,
        ["new", "--name", "my_project", "--type", "python",
         "--description", "x", "--author", "x",
         "--output", str(tmp_path), "--force"],
    )
    assert result.exit_code == 0


def test_invalid_type_rejected(runner: CliRunner, tmp_path: Path) -> None:
    """An invalid project type returns a non-zero exit code."""
    result = runner.invoke(
        cli,
        ["new", "--name", "x", "--type", "invalid_type",
         "--description", "x", "--author", "x", "--output", str(tmp_path)],
    )
    assert result.exit_code != 0