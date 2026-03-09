# scaffold.py — w2d-scaffold
# Main CLI entrypoint. Handles project generation via Click commands.
# Uses Jinja2 to render templates from the templates/ directory.

import re
import shutil
from datetime import date
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader

# Supported project types
VALID_TYPES = [
    "data",
    "rag",
    "python",
    "wordpress-plugin",
    "wordpress-theme",
    "astro",
]

TEMPLATES_DIR = Path(__file__).parent / "templates"


def slugify(name: str) -> str:
    """
    Convert a string to a safe snake_case project name.

    Replaces spaces and hyphens with underscores, removes special characters,
    and lowercases the result.

    Args:
        name: Raw project name input by the user.

    Returns:
        A clean snake_case string suitable for use as a Python identifier.
    """
    name = name.lower().strip()
    name = re.sub(r"[\s\-]+", "_", name)
    name = re.sub(r"[^\w]", "", name)
    return name


def to_human(name: str) -> str:
    """
    Convert a snake_case or kebab-case name to Title Case.

    Args:
        name: snake_case or kebab-case string.

    Returns:
        Title Case string for display purposes.
    """
    return name.replace("_", " ").replace("-", " ").title()


def render_template(template_path: Path, context: dict) -> str:
    """
    Render a single Jinja2 template file with the given context.

    Args:
        template_path: Absolute path to the .j2 template file.
        context: Dictionary of variables to inject into the template.

    Returns:
        Rendered string content.
    """
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        keep_trailing_newline=True,
    )
    template = env.get_template(template_path.name)
    return template.render(**context)


def copy_common_templates(output_dir: Path, context: dict) -> None:
    """
    Render and copy all _common templates into the output directory.

    Args:
        output_dir: Target project directory.
        context: Jinja2 rendering context.
    """
    common_dir = TEMPLATES_DIR / "_common"
    for template_file in sorted(common_dir.glob("*.j2")):
        output_filename = template_file.stem  # removes .j2 extension
        output_path = output_dir / output_filename
        rendered = render_template(template_file, context)
        output_path.write_text(rendered, encoding="utf-8")


def copy_type_templates(output_dir: Path, project_type: str, context: dict) -> None:
    """
    Render and copy all type-specific templates into the output directory,
    preserving subdirectory structure.

    Args:
        output_dir: Target project directory.
        project_type: One of the VALID_TYPES strings.
        context: Jinja2 rendering context.
    """
    type_dir = TEMPLATES_DIR / project_type
    if not type_dir.exists():
        return

    for item in sorted(type_dir.rglob("*")):
        if item.is_dir():
            continue

        relative = item.relative_to(type_dir)

        # Remove .j2 extension from output filename if present
        parts = list(relative.parts)
        parts[-1] = parts[-1].removesuffix(".j2")
        output_path = output_dir / Path(*parts)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if item.suffix == ".j2":
            rendered = render_template(item, context)
            output_path.write_text(rendered, encoding="utf-8")
        else:
            # Non-template files (e.g. .gitkeep) are copied as-is
            shutil.copy2(item, output_path)


def generate_project(
    name: str,
    project_type: str,
    description: str,
    author: str,
    output_base: Path,
) -> Path:
    """
    Orchestrate the full project generation: render common + type-specific templates.

    Args:
        name: Raw project name (will be slugified).
        project_type: One of the VALID_TYPES strings.
        description: Short project description.
        author: Author full name.
        output_base: Directory where the new project folder will be created.

    Returns:
        Path to the generated project directory.

    Raises:
        FileExistsError: If the target directory already exists.
    """
    project_name = slugify(name)
    output_dir = output_base / project_name

    if output_dir.exists():
        raise FileExistsError(
            f"Directory '{output_dir}' already exists. "
            "Use --force to overwrite (not yet implemented)."
        )

    output_dir.mkdir(parents=True)

    context = {
        "project_name": project_name,
        "project_name_human": to_human(name),
        "description": description,
        "author": author,
        "date": date.today().isoformat(),
        "type": project_type,
    }

    copy_common_templates(output_dir, context)
    copy_type_templates(output_dir, project_type, context)

    return output_dir


@click.group()
def cli() -> None:
    """w2d-scaffold — Generate opinionated project structures for LLM-assisted workflows."""
    pass


@cli.command()
@click.option("--name", "-n", default=None, help="Project name")
@click.option(
    "--type",
    "-t",
    "project_type",
    default=None,
    type=click.Choice(VALID_TYPES, case_sensitive=False),
    help="Project type",
)
@click.option("--description", "-d", default="", help="Short project description")
@click.option("--author", "-a", default="", help="Author name")
def new(
    name: str | None,
    project_type: str | None,
    description: str,
    author: str,
) -> None:
    """
    Generate a new project structure.

    Runs interactively if --name or --type are not provided.
    """
    if name is None:
        name = click.prompt("Project name")

    if project_type is None:
        project_type = click.prompt(
            "Project type",
            type=click.Choice(VALID_TYPES, case_sensitive=False),
        )

    if not description:
        description = click.prompt("Short description", default="")

    if not author:
        author = click.prompt("Author", default="")

    output_base = Path.cwd()

    try:
        output_dir = generate_project(
            name=name,
            project_type=project_type,
            description=description,
            author=author,
            output_base=output_base,
        )
        click.echo(f"✅ Project '{output_dir.name}' created at {output_dir}")
    except FileExistsError as e:
        click.echo(f"❌ {e}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    cli()