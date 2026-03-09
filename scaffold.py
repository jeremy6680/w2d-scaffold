"""
w2d-scaffold — CLI entry point.

Generates a complete project structure from a single command.
Usage: python scaffold.py new / make new
"""

import re
import shutil
from datetime import date
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_TYPES = [
    "data",
    "rag",
    "python",
    "wordpress-plugin",
    "wordpress-theme",
    "astro",
]

TEMPLATES_DIR = Path(__file__).parent / "templates"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def to_snake_case(name: str) -> str:
    """Convert a project name to snake_case, replacing hyphens and spaces.

    Args:
        name: Raw project name provided by the user.

    Returns:
        Normalised snake_case string.
    """
    name = name.strip().lower()
    name = re.sub(r"[\s\-]+", "_", name)
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name


def to_title_case(name: str) -> str:
    """Convert a snake_case or hyphenated name to human-readable Title Case.

    Args:
        name: snake_case or hyphenated project name.

    Returns:
        Title Case string.
    """
    return re.sub(r"[\s_\-]+", " ", name).title()


def render_template(template_path: Path, context: dict) -> str:
    """Render a single Jinja2 template file with the given context.

    Args:
        template_path: Absolute path to the .j2 template file.
        context: Dictionary of Jinja2 variables.

    Returns:
        Rendered string content.
    """
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        keep_trailing_newline=True,
    )
    template = env.get_template(template_path.name)
    return template.render(**context)


def generate_from_dir(
    template_dir: Path,
    output_dir: Path,
    context: dict,
) -> None:
    """Recursively render all .j2 templates from a directory into output_dir.

    Non-.j2 files are copied as-is (binary-safe).

    Args:
        template_dir: Source directory containing .j2 templates.
        output_dir: Destination directory for rendered files.
        context: Jinja2 template variables.
    """
    for item in sorted(template_dir.rglob("*")):
        if item.is_dir():
            continue

        relative = item.relative_to(template_dir)

        # Replace {{ project_name }} placeholder in path segments
        rendered_relative = Path(
            *[
                part.replace("__project_name__", context["project_name"])
                for part in relative.parts
            ]
        )

        dest = output_dir / rendered_relative

        dest.parent.mkdir(parents=True, exist_ok=True)

        if item.suffix == ".j2":
            # Strip the .j2 extension in the output filename
            dest = dest.with_suffix("")
            dest.write_text(render_template(item, context), encoding="utf-8")
        else:
            shutil.copy2(item, dest)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@click.group()
def cli() -> None:
    """w2d-scaffold — opinionated project scaffolding for LLM-assisted workflows."""


@cli.command("new")
@click.option("--name", "-n", default=None, help="Project name (snake_case).")
@click.option(
    "--type",
    "-t",
    "project_type",
    default=None,
    type=click.Choice(VALID_TYPES, case_sensitive=False),
    help="Project type.",
)
@click.option("--description", "-d", default=None, help="Short project description.")
@click.option("--author", "-a", default=None, help="Author name.")
@click.option(
    "--output",
    "-o",
    default=".",
    show_default=True,
    help="Parent directory where the project folder will be created.",
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Overwrite an existing directory.",
)
def new_project(
    name: str | None,
    project_type: str | None,
    description: str | None,
    author: str | None,
    output: str,
    force: bool,
) -> None:
    """Generate a new project scaffold interactively or via flags."""

    # -- Interactive prompts for missing values ----------------------------
    if not name:
        name = click.prompt("Project name")

    project_name = to_snake_case(name)

    # Warn user if normalisation changed the name
    if project_name != name:
        click.echo(
            f"  ℹ️  Name normalised to snake_case: '{project_name}'"
        )
        click.confirm("  Continue with this name?", default=True, abort=True)

    if not project_type:
        project_type = click.prompt(
            "Project type",
            type=click.Choice(VALID_TYPES, case_sensitive=False),
        )

    if not description:
        description = click.prompt("Short description", default="")

    if not author:
        author = click.prompt("Author", default="")

    # -- Resolve output directory -----------------------------------------
    output_base = Path(output).resolve()
    project_dir = output_base / project_name

    if project_dir.exists():
        if force:
            shutil.rmtree(project_dir)
            click.echo(f"  ⚠️  Existing directory removed: {project_dir}")
        else:
            raise click.ClickException(
                f"Directory '{project_dir}' already exists. "
                "Use --force to overwrite."
            )

    project_dir.mkdir(parents=True)

    # -- Build Jinja2 context ---------------------------------------------
    context: dict = {
        "project_name": project_name,
        "project_name_human": to_title_case(project_name),
        "description": description,
        "author": author,
        "date": date.today().isoformat(),
        "type": project_type,
    }

    # -- Render _common templates -----------------------------------------
    common_dir = TEMPLATES_DIR / "_common"
    generate_from_dir(common_dir, project_dir, context)

    # -- Render type-specific templates -----------------------------------
    type_dir = TEMPLATES_DIR / project_type
    if type_dir.exists():
        generate_from_dir(type_dir, project_dir, context)

    click.echo(f"\n✅  Project '{project_name}' created at {project_dir}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cli()