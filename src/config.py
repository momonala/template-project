import tomllib
from pathlib import Path

import typer

_config_file = Path(__file__).parent.parent / "pyproject.toml"
with _config_file.open("rb") as f:
    _config = tomllib.load(f)

_project_config = _config["project"]

PROJECT_NAME = _project_config["name"]
PROJECT_VERSION = _project_config["version"]
FLASK_PORT = _config["tool"]["config"]["flask_port"]


def config_cli(
    all: bool = typer.Option(False, "--all", help="Show all configuration values"),
    project_name: bool = typer.Option(False, "--project-name", help=PROJECT_NAME),
    project_version: bool = typer.Option(False, "--project-version", help=PROJECT_VERSION),
    flask_port: bool = typer.Option(False, "--flask-port", help=str(FLASK_PORT)),
) -> None:
    """Expose non-secret configuration defined in pyproject.toml's [tool.config] section."""
    if all:
        typer.echo(f"project_name={PROJECT_NAME}")
        typer.echo(f"project_version={PROJECT_VERSION}")
        typer.echo(f"flask_port={FLASK_PORT}")
        return

    param_map = {
        project_name: PROJECT_NAME,
        project_version: PROJECT_VERSION,
        flask_port: FLASK_PORT,
    }

    for is_set, value in param_map.items():
        if is_set:
            typer.echo(value)
            return

    typer.secho(
        "Error: No config key specified. Use --help to see available options.",
        fg=typer.colors.RED,
        err=True,
    )
    raise typer.Exit(1)


def main():
    typer.run(config_cli)


if __name__ == "__main__":
    main()
