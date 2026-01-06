import tomllib
from pathlib import Path

import typer

# from .values import TELEGRAM_API_TOKEN
# from .values import TELEGRAM_CHAT_ID
# from .values import GOOGLE_MAPS_API_KEY
# from .values import SPOTIFY_CLIENT_ID
# from .values import SPOTIFY_CLIENT_SECRET
# from .values import MAPBOX_API_KEY
# from .values import FLASK_SECRET_KEY

_config_file = Path(__file__).parent.parent / "pyproject.toml"
with _config_file.open("rb") as f:
    _config = tomllib.load(f)

_project_config = _config["project"]
_tool_config = _config["tool"]["config"]

PROJECT_NAME = _project_config["name"]
PROJECT_VERSION = _project_config["version"]

# FLASK_PORT = _tool_config["flask_port"]
# SERVER_URL = _tool_config["server_url"]
# DATABASE_PATH = _tool_config["database_path"]
# DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
# MQTT_PORT = _tool_config["mqtt_port"]
# MQTT_TOPIC = _tool_config["mqtt_topic"]
# TUNNEL_NAME = _tool_config["tunnel_name"]
# DOMAIN_SUFFIX = _tool_config["domain_suffix"]
# UPDATE_INTERVAL_MIN = _tool_config["update_interval_min"]
# DEFAULT_LOCATION = _tool_config["default_location"]


# ============================================================================
# TYPER CLI (exposes non-secrets only)
# ============================================================================

# fmt: off
def config_cli(
    # Show all
    all: bool = typer.Option(False, "--all", help="Show all configuration values"),
    # Project keys
    project_name: bool = typer.Option(False, "--project-name", help=PROJECT_NAME),
    project_version: bool = typer.Option(False, "--project-version", help=PROJECT_VERSION),
    # Uncomment and add your config options below:
    # Server settings
    # flask_port: bool = typer.Option(False, "--flask-port", help=str(FLASK_PORT)),
    # server_url: bool = typer.Option(False, "--server-url", help=SERVER_URL),
    # Database settings
    # database_path: bool = typer.Option(False, "--database-path", help=DATABASE_PATH),
    # database_url: bool = typer.Option(False, "--database-url", help=DATABASE_URL),
    # MQTT settings
    # mqtt_port: bool = typer.Option(False, "--mqtt-port", help=str(MQTT_PORT)),
    # mqtt_topic: bool = typer.Option(False, "--mqtt-topic", help=MQTT_TOPIC),
    # Cloudflare settings
    # tunnel_name: bool = typer.Option(False, "--tunnel-name", help=TUNNEL_NAME),
    # domain_suffix: bool = typer.Option(False, "--domain-suffix", help=DOMAIN_SUFFIX),
) -> None:
# fmt: on
    """Get configuration values from pyproject.toml.
    
    Only non-secret configuration is exposed via this CLI.
    Secrets should be imported directly from src.values in your code.
    """
    # Show all configuration
    if all:
        typer.echo(f"project_name={PROJECT_NAME}")
        typer.echo(f"project_version={PROJECT_VERSION}")
        # Uncomment and add all your non-secret config values here:
        # typer.echo(f"flask_port={FLASK_PORT}")
        # typer.echo(f"server_url={SERVER_URL}")
        # typer.echo(f"database_path={DATABASE_PATH}")
        # typer.echo(f"database_url={DATABASE_URL}")
        # typer.echo(f"mqtt_port={MQTT_PORT}")
        # typer.echo(f"mqtt_topic={MQTT_TOPIC}")
        # typer.echo(f"tunnel_name={TUNNEL_NAME}")
        # typer.echo(f"domain_suffix={DOMAIN_SUFFIX}")
        return

    # Map parameters to their actual values
    param_map = {
        project_name: PROJECT_NAME,
        project_version: PROJECT_VERSION,
        # Uncomment and add all your config mappings here:
        # flask_port: FLASK_PORT,
        # server_url: SERVER_URL,
        # database_path: DATABASE_PATH,
        # database_url: DATABASE_URL,
        # mqtt_port: MQTT_PORT,
        # mqtt_topic: MQTT_TOPIC,
        # tunnel_name: TUNNEL_NAME,
        # domain_suffix: DOMAIN_SUFFIX,
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
