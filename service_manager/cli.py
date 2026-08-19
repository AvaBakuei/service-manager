import typer
from pathlib import Path
from typing import Annotated
from rich.console import Console
from .project import initialize_project
from .exceptions import ProjectAlreadyExistsError, ServiceAlreadyExistsError, ServiceDoesNotExistError
from .models import Service
from .validation import validate_service, validate_service_name, validate_config
from .config import load_config, save_config, get_config_path
from .service import services_list, show_service
from .generator import generate_compose, generate_applications
from .docker import compose_up, compose_down, compose_ps, compose_logs
from .health import health_check, health_check_all

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
    applications_path = Path.cwd() / "applications.yml"

    config = load_config(get_config_path())
    services = list(config["services"].values())

    generate_compose(services, output_path)
    generate_applications(services, applications_path)

    typer.echo(
        f"Docker Compose file generated at {output_path}"
    )
    typer.echo(
        f"Applications file generated at {applications_path}"
    )


@app.command()
def validate():
    """Validate the service configuration."""
    config = load_config(get_config_path())
    errors = validate_config(config)

    if errors:
        typer.secho("Configuration validation failed:", fg=typer.colors.RED)
        for error in errors:
            typer.echo(f"- {error}")

        raise typer.Exit(code=1)

    typer.secho("Configuration is valid.", fg=typer.colors.GREEN)


@app.command()
def up():
    """Start all services."""
    compose_up()


@app.command()
def down():
    """Stop and remove all services."""
    compose_down()


@app.command()
def ps():
    """Show running services."""
    compose_ps()


@app.command()
def logs(service_name: Annotated[str, typer.Argument(help="The name of the service")]):
    """Show service logs."""
    compose_logs(service_name)


def print_health_result(service_name: str, result: dict) -> None:
    typer.echo(f"Service: {service_name}")
    typer.echo(f"Status: {result['status']}")

    if result["error"]:
        typer.echo(f"Error: {result['error']}")
        return

    typer.echo(f"HTTP Status: {result['http_status']}")
    typer.echo(f"Response Time: {result['response_time']} ms")


@app.command()
def health(
    service_name: Annotated[
        str | None,
        typer.Argument(help="The name of the service")
    ] = None,
    all: bool = typer.Option(
        False,
        "--all",
        help="Check all services"
    ),
):
    """Check service health."""

    config = load_config(get_config_path())
    services = config["services"]

    if all:
        results = health_check_all(services)

        for service_name, result in results.items():
            print_health_result(service_name, result)

        return

    if service_name not in services:
        raise ServiceDoesNotExistError(
            f"Service '{service_name}' does not exist."
        )

    result = health_check(services[service_name])
    print_health_result(service_name, result)


if __name__ == "__main__":
    app()
