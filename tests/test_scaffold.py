# tests/test_scaffold.py — w2d-scaffold
# pytest test suite: verifies that each project type generates the expected
# files and that Jinja2 variables are correctly interpolated.

from pathlib import Path

import pytest
from click.testing import CliRunner

from scaffold import cli


# ---------------------------------------------------------------------------
# Shared test fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def runner() -> CliRunner:
    """Return a Click test runner."""
    return CliRunner()


@pytest.fixture
def base_args() -> list[str]:
    """Return common CLI arguments shared across all project type tests."""
    return [
        "--name", "test_project",
        "--description", "A test project",
        "--author", "Test Author",
    ]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def invoke_new(runner: CliRunner, args: list[str]) -> object:
    """Invoke the `new` subcommand inside a temporary isolated filesystem."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["new"] + args)
        yield result, Path("test_project")


# ---------------------------------------------------------------------------
# Common files (all types)
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

@pytest.mark.parametrize("project_type", [
    "data",
    "rag",
    "python",
    "wordpress-plugin",
    "wordpress-theme",
    "astro",
])
def test_common_files_exist(runner: CliRunner, base_args: list[str], project_type: str) -> None:
    """All common LLM pilot files must be present for every project type."""
    args = base_args + ["--type", project_type]
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["new"] + args)
        assert result.exit_code == 0, result.output
        project_dir = Path("test_project")
        for filename in COMMON_FILES:
            assert (project_dir / filename).exists(), f"Missing: {filename}"


@pytest.mark.parametrize("project_type", [
    "data",
    "rag",
    "python",
    "wordpress-plugin",
    "wordpress-theme",
    "astro",
])
def test_jinja2_interpolation(runner: CliRunner, base_args: list[str], project_type: str) -> None:
    """Jinja2 variables must be correctly rendered in CONTEXT.md."""
    args = base_args + ["--type", project_type]
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["new"] + args)
        assert result.exit_code == 0, result.output
        context_md = (Path("test_project") / "CONTEXT.md").read_text()
        assert "test_project" in context_md
        assert "Test Author" in context_md
        assert "{{" not in context_md, "Unrendered Jinja2 tag found in CONTEXT.md"


# ---------------------------------------------------------------------------
# Type: data
# ---------------------------------------------------------------------------

DATA_FILES = [
    "Makefile",
    "dbt/dbt_project.yml",
    "dbt/profiles.yml",
    "dbt/models/bronze/.gitkeep",
    "dbt/models/silver/.gitkeep",
    "dbt/models/gold/.gitkeep",
    "sources/.gitkeep",
    "pyproject.toml",
]

def test_data_files_exist(runner: CliRunner, base_args: list[str]) -> None:
    """All expected files for the `data` type must be generated."""
    args = base_args + ["--type", "data"]
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["new"] + args)
        assert result.exit_code == 0, result.output
        project_dir = Path("test_project")
        for filepath in DATA_FILES:
            assert (project_dir / filepath).exists(), f"Missing: {filepath}"


def test_data_makefile_interpolation(runner: CliRunner, base_args: list[str]) -> None:
    """The data Makefile must contain the project name after rendering."""
    args = base_args + ["--type", "data"]
    with runner.isolated_filesystem():
        runner.invoke(cli, ["new"] + args)
        makefile = (Path("test_project") / "Makefile").read_text()
        assert "test_project" in makefile or "Test Project" in makefile
        assert "{{" not in makefile


def test_data_dbt_project_yml_interpolation(runner: CliRunner, base_args: list[str]) -> None:
    """dbt_project.yml must contain the project name after rendering."""
    args = base_args + ["--type", "data"]
    with runner.isolated_filesystem():
        runner.invoke(cli, ["new"] + args)
        dbt_yml = (Path("test_project") / "dbt" / "dbt_project.yml").read_text()
        assert "test_project" in dbt_yml
        assert "{{" not in dbt_yml


# ---------------------------------------------------------------------------
# Type: rag
# ---------------------------------------------------------------------------

RAG_FILES = [
    "main.py",
    "app/ingestion.py",
    "app/retrieval.py",
    "app/api.py",
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "requirements.txt",
]

def test_rag_files_exist(runner: CliRunner, base_args: list[str]) -> None:
    """All expected files for the `rag` type must be generated."""
    args = base_args + ["--type", "rag"]
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["new"] + args)
        assert result.exit_code == 0, result.output
        project_dir = Path("test_project")
        for filepath in RAG_FILES:
            assert (project_dir / filepath).exists(), f"Missing: {filepath}"


def test_rag_main_interpolation(runner: CliRunner, base_args: list[str]) -> None:
    """main.py must contain the project name after rendering."""
    args = base_args + ["--type", "rag"]
    with runner.isolated_filesystem():
        runner.invoke(cli, ["new"] + args)
        main_py = (Path("test_project") / "main.py").read_text()
        assert "Test Project" in main_py
        assert "{{" not in main_py


def test_rag_requirements_no_template_tags(runner: CliRunner, base_args: list[str]) -> None:
    """requirements.txt must have no unrendered Jinja2 tags."""
    args = base_args + ["--type", "rag"]
    with runner.isolated_filesystem():
        runner.invoke(cli, ["new"] + args)
        reqs = (Path("test_project") / "requirements.txt").read_text()
        assert "{{" not in reqs


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_duplicate_project_name(runner: CliRunner, base_args: list[str]) -> None:
    """Generating a project with an existing name must fail with exit code 1."""
    args = base_args + ["--type", "data"]
    with runner.isolated_filesystem():
        runner.invoke(cli, ["new"] + args)
        result = runner.invoke(cli, ["new"] + args)
        assert result.exit_code == 1
        assert "already exists" in result.output