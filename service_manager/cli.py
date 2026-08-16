import typer
from pathlib import Path
from typing import Annotated
from rich.console import Console
from .project import initialize_project
from .exceptions import ProjectAlreadyExistsError, ServiceAlreadyExistsError, ServiceDoesNotExistError
from .models import Service
from .validation import validate_service, validate_service_name
from .config import load_config, save_config, get_config_path
from .service import services_list, show_service
from .generator import generate_compose

app = typer.Typer()
console = Console()


@app.callback()
def main():
    """ Service Manager CLI. """
    pass


@app.command()
def init():
    """ Initialize a new service manager project. """

    try:
        initialize_project(Path.cwd())  # cwd = Current Working Directory
        typer.echo("Project initialized successfully.")
    except ProjectAlreadyExistsError as error:
        typer.echo(f"Error: {error}")


@app.command()
def add():
    """ Add a new Service. """
    try:
        name = typer.prompt("Service name")
        image = typer.prompt("Docker image")
        internal_port = typer.prompt("Internal Port", type=int)
        domain = typer.prompt("Domain")
        enabled = typer.confirm("Enable service?", default=True)
        health_path = typer.prompt("Health path", default="/")

        service = Service(
            name=name,
            image=image,
            internal_port=internal_port,
            domain=domain,
            enabled=enabled,
            health_path=health_path
        )

        validate_service(service)

        config = load_config(get_config_path())

        validate_service_name(name, config["services"])
        config["services"][name] = service.to_dict()
        save_config(get_config_path(), config)

        typer.echo(f"Service '{name}' added successfully.")

    except (ValueError, ServiceAlreadyExistsError) as error:
        typer.echo(f"Error: {error}")


@app.command("list")
def list_services():
    """ Show a List of Services. """
    config = load_config(get_config_path())

    try:
        table = services_list(config)
        console.clear()
        console.print(table)
    except ServiceDoesNotExistError as error:
        typer.secho(
            f"Error: {error}",
            fg=typer.colors.RED
        )


@app.command()
def show(service_name: Annotated[str, typer.Argument(help="The name of the service")]):
    """ Show a Service. """
    config = load_config(get_config_path())
    try:
        show_service(service_name, config)
    except ServiceDoesNotExistError as error:
        typer.secho(
            f"Error: {error}",
            fg=typer.colors.RED
        )


@app.command()
def generate():
    """Generate Docker Compose configuration."""
    output_path = Path.cwd() / "generated" / "docker-compose.yml"
    config = load_config(get_config_path())
    generate_compose(list(config["services"].values()), output_path)
    typer.echo(
        f"Docker Compose file generated at {output_path}"
    )


if __name__ == "__main__":
    app()
