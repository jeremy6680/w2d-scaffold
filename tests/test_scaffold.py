# tests/test_scaffold.py — w2d-scaffold
# pytest test suite: verifies that each project type generates the expected
# files and that Jinja2 variables are correctly interpolated.

from pathlib import Path

import pytest
from click.testing import CliRunner

from scaffold import cli

import re
JINJA2_TAG_RE = re.compile(r"\{\{\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\}\}")

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


# ─── Phase 3 — WordPress templates ───────────────────────────────

class TestWordpressPluginTemplate:
    """Tests for the wordpress-plugin project type."""

    def test_generates_expected_files(self, tmp_path: Path) -> None:
        """All expected files are created for a wordpress-plugin project."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "new",
                "--name", "my_plugin",
                "--type", "wordpress-plugin",
                "--description", "A test WP plugin",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )
        assert result.exit_code == 0, result.output

        project_dir = tmp_path / "my_plugin"
        expected_files = [
            "CONTEXT.md",
            "NEXT_STEPS.md",
            "STRUCTURE.md",
            "DECISIONS.md",
            "README.md",
            ".gitignore",
            ".env.example",
            "my_plugin.php",
            "includes/class-my-plugin.php",
            "includes/helpers.php",
            "templates/archive.php",
            "assets/css/main.css",
            "assets/js/main.js",
        ]
        for f in expected_files:
            assert (project_dir / f).exists(), f"Missing: {f}"

    def test_plugin_header_contains_project_name(self, tmp_path: Path) -> None:
        """The main plugin file contains the correct Plugin Name header."""
        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "new",
                "--name", "my_plugin",
                "--type", "wordpress-plugin",
                "--description", "A test WP plugin",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )
        plugin_file = tmp_path / "my_plugin" / "my_plugin.php"
        content = plugin_file.read_text()
        assert "Plugin Name: My Plugin" in content
        assert "MY_PLUGIN_VERSION" in content


class TestWordpressThemeTemplate:
    """Tests for the wordpress-theme project type."""

    def test_generates_expected_files(self, tmp_path: Path) -> None:
        """All expected files are created for a wordpress-theme project."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "new",
                "--name", "my_theme",
                "--type", "wordpress-theme",
                "--description", "A test WP theme",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )
        assert result.exit_code == 0, result.output

        project_dir = tmp_path / "my_theme"
        expected_files = [
            "CONTEXT.md",
            "NEXT_STEPS.md",
            "STRUCTURE.md",
            "DECISIONS.md",
            "README.md",
            ".gitignore",
            ".env.example",
            "style.css",
            "functions.php",
            "index.php",
            "templates/base.twig",
            "templates/index.twig",
            "templates/single.twig",
            "src/scss/_variables.scss",
            "src/scss/_mixins.scss",
            "src/scss/main.scss",
            "src/js/main.js",
            "acf-json/.gitkeep",
        ]
        for f in expected_files:
            assert (project_dir / f).exists(), f"Missing: {f}"

    def test_style_css_contains_theme_header(self, tmp_path: Path) -> None:
        """style.css contains the WordPress theme header with correct name."""
        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "new",
                "--name", "my_theme",
                "--type", "wordpress-theme",
                "--description", "A test WP theme",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )
        style_css = tmp_path / "my_theme" / "style.css"
        content = style_css.read_text()
        assert "Theme Name: My Theme" in content
        assert "Test Author" in content

    def test_functions_php_contains_timber_bootstrap(self, tmp_path: Path) -> None:
        """functions.php contains the Timber initialisation call."""
        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "new",
                "--name", "my_theme",
                "--type", "wordpress-theme",
                "--description", "A test WP theme",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )
        functions_php = tmp_path / "my_theme" / "functions.php"
        content = functions_php.read_text()
        assert "Timber\\Timber::init()" in content
        assert "acf-json" in content


# =============================================================================
# Phase 4a: python template
# =============================================================================

class TestPythonTemplate:
    """Tests for the `python` project type."""

    def test_python_expected_files(self, tmp_path: Path) -> None:
        """All expected files are generated for a python project."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "new",
                "--name", "my_lib",
                "--type", "python",
                "--description", "A typed Python library",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )
        assert result.exit_code == 0, result.output

        project_dir = tmp_path / "my_lib"

        expected = [
            # Common scaffold
            "CONTEXT.md",
            "NEXT_STEPS.md",
            "STRUCTURE.md",
            "DECISIONS.md",
            "README.md",
            ".gitignore",
            ".env.example",
            # Python-specific
            "src/my_lib/__init__.py",
            "src/my_lib/main.py",
            "tests/test_main.py",
            "pyproject.toml",
        ]

        for relative_path in expected:
            target = project_dir / relative_path
            assert target.exists(), f"Missing: {relative_path}"

    def test_python_jinja2_interpolation(self, tmp_path: Path) -> None:
        """Jinja2 variables are correctly rendered in Python-specific files."""
        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "new",
                "--name", "my_lib",
                "--type", "python",
                "--description", "A typed Python library",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )

        project_dir = tmp_path / "my_lib"

        # pyproject.toml must contain the project name and description
        pyproject = (project_dir / "pyproject.toml").read_text()
        assert "my_lib" in pyproject
        assert "A typed Python library" in pyproject

        # main.py must reference the human name
        main_py = (project_dir / "src/my_lib/main.py").read_text()
        assert "My Lib" in main_py

        # test file must import from the package
        test_py = (project_dir / "tests/test_main.py").read_text()
        assert "from my_lib.main import main" in test_py

    def test_python_no_jinja2_tags_remaining(self, tmp_path: Path) -> None:
        """No unrendered Jinja2 tags remain in any generated file."""
        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "new",
                "--name", "my_lib",
                "--type", "python",
                "--description", "A typed Python library",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )

        project_dir = tmp_path / "my_lib"

        for file_path in project_dir.rglob("*"):
            if file_path.is_file():
                content = file_path.read_text(errors="ignore")
                assert "{{" not in content, (
                    f"Unrendered Jinja2 tag in: {file_path.relative_to(project_dir)}"
                )

# =============================================================================
# Phase 4b: astro template
# =============================================================================

class TestAstroTemplate:
    """Tests for the `astro` project type."""

    def test_astro_expected_files(self, tmp_path: Path) -> None:
        """All expected files are generated for an astro project."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "new",
                "--name", "my_blog",
                "--type", "astro",
                "--description", "Test blog",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )
        assert result.exit_code == 0, result.output

        project_dir = tmp_path / "my_blog"

        expected = [
            # Common scaffold
            "CONTEXT.md",
            "NEXT_STEPS.md",
            "STRUCTURE.md",
            "DECISIONS.md",
            "README.md",
            ".gitignore",
            ".env.example",
            # Astro-specific
            "astro.config.mjs",
            "package.json",
            "tsconfig.json",
            "src/consts.ts",
            "src/styles/global.css",
            "src/layouts/BaseLayout.astro",
            "src/layouts/PostLayout.astro",
            "src/layouts/ListLayout.astro",
            "src/pages/index.astro",
            "src/pages/blog/[...slug].astro",
            "src/components/solidjs/ThemeToggle.tsx",
            "src/components/solidjs/MobileNav.tsx",
            "src/components/solidjs/GiscusComments.tsx",
            "src/content/blog/hello-world.mdx",
            "src/content/authors/my_blog.mdx",
            "src/content/tags/general.mdx",
        ]

        for relative_path in expected:
            target = project_dir / relative_path
            assert target.exists(), f"Missing: {relative_path}"

    def test_astro_jinja2_interpolation(self, tmp_path: Path) -> None:
        """Jinja2 variables are correctly rendered in Astro-specific files."""
        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "new",
                "--name", "my_blog",
                "--type", "astro",
                "--description", "Test blog",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )

        project_dir = tmp_path / "my_blog"

        # consts.ts must contain human name, description and author
        consts = (project_dir / "src/consts.ts").read_text()
        assert "My Blog" in consts
        assert "Test blog" in consts
        assert "Test Author" in consts

        # package.json must contain the snake_case project name
        package_json = (project_dir / "package.json").read_text()
        assert "my_blog" in package_json

class TestAstroTemplate:
    """Tests for the `astro` project type."""

    def test_astro_expected_files(self, tmp_path: Path) -> None:
        """All expected files are generated for an astro project."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "new",
                "--name", "my_blog",
                "--type", "astro",
                "--description", "Test blog",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )
        assert result.exit_code == 0, result.output

        project_dir = tmp_path / "my_blog"

        expected = [
            "CONTEXT.md",
            "NEXT_STEPS.md",
            "STRUCTURE.md",
            "DECISIONS.md",
            "README.md",
            ".gitignore",
            ".env.example",
            "astro.config.mjs",
            "package.json",
            "tsconfig.json",
            "src/consts.ts",
            "src/styles/global.css",
            "src/layouts/BaseLayout.astro",
            "src/layouts/PostLayout.astro",
            "src/layouts/ListLayout.astro",
            "src/pages/index.astro",
            "src/pages/blog/[...slug].astro",
            "src/components/solidjs/ThemeToggle.tsx",
            "src/components/solidjs/MobileNav.tsx",
            "src/components/solidjs/GiscusComments.tsx",
            "src/content/blog/hello-world.mdx",
            "src/content/authors/my_blog.mdx",
            "src/content/tags/general.mdx",
        ]

        for relative_path in expected:
            target = project_dir / relative_path
            assert target.exists(), f"Missing: {relative_path}"

    def test_astro_jinja2_interpolation(self, tmp_path: Path) -> None:
        """Jinja2 variables are correctly rendered in Astro-specific files."""
        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "new",
                "--name", "my_blog",
                "--type", "astro",
                "--description", "Test blog",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )

        project_dir = tmp_path / "my_blog"

        consts = (project_dir / "src/consts.ts").read_text()
        assert "My Blog" in consts
        assert "Test blog" in consts
        assert "Test Author" in consts

        package_json = (project_dir / "package.json").read_text()
        assert "my_blog" in package_json

    def test_astro_no_jinja2_tags_remaining(self, tmp_path: Path) -> None:
        """No unrendered Jinja2 tags remain in any generated file.

        Note: {{ }} in .astro/.tsx/.ts files is valid JSX/Astro syntax
        (e.g. openGraph={{ basic: {...} }}). We only flag {{ identifier }}
        patterns that look like unrendered Jinja2 variables.
        """
        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "new",
                "--name", "my_blog",
                "--type", "astro",
                "--description", "Test blog",
                "--author", "Test Author",
                "--output-dir", str(tmp_path),
            ],
        )

        project_dir = tmp_path / "my_blog"

        for file_path in project_dir.rglob("*"):
            if file_path.is_file():
                content = file_path.read_text(errors="ignore")
                match = JINJA2_TAG_RE.search(content)
                assert match is None, (
                    f"Unrendered Jinja2 tag '{match.group()}' in: "
                    f"{file_path.relative_to(project_dir)}"
                )