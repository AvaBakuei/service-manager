import typer
from pathlib import Path

from .project import initialize_project
from .exceptions import ProjectAlreadyExistsError, ServiceAlreadyExistsError
from .models import Service
from .validation import validate_service
from .config import load_config, save_config
from .validation import validate_service_name, validate_service

app = typer.Typer()


@app.callback()
def main():
    """ Service Manager CLI. """
    pass


@app.command()
def init():
    """ Initialize a new service manager project. """

    try:
        initialize_project(Path.cwd())  # cwd = Current Working Directory
        print("Project initialized successfully.")
    except ProjectAlreadyExistsError as error:
        print(f"Error: {error}")


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
        print(service)

        config_path = Path.cwd() / "services.yml"
        config = load_config(config_path)

        validate_service_name(name, config["services"])
        config["services"][name] = service.to_dict()
        save_config(config_path, config)

        typer.echo(f"Service '{name}' added successfully.")

    except (ValueError, ServiceAlreadyExistsError) as error:
        typer.echo(f"Error: {error}")


if __name__ == "__main__":
    app()
