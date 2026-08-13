import typer
from rich.table import Table

from .exceptions import ServiceDoesNotExistError


def services_list(config: dict) -> Table:
    if not config["services"]:
        raise ServiceDoesNotExistError(f"There are no services.")

    table = Table(show_footer=False, title="List of Services")
    table.add_column("Name",  style="cyan")
    table.add_column("IMAGE", style="magenta")
    table.add_column("DOMAIN", style="green")
    table.add_column("ENABLED", style="yellow")

    for service in config["services"].values():
        table.add_row(service["name"], service["image"],
                      service["domain"], str(service["enabled"]))
    return table


def show_service(service_name: str, config: dict) -> None:
    if service_name not in config["services"]:
        raise ServiceDoesNotExistError(
            f"Service '{service_name}' does not exist.")

    service = config["services"][service_name]

    typer.secho(f"Name: {service['name']}",
                fg=typer.colors.GREEN)
    typer.secho(f"Image: {service['image']}",
                fg=typer.colors.GREEN)
    typer.secho(
        f"Internal Port: {service['internal_port']}",
        fg=typer.colors.GREEN)
    typer.secho(f"Domain: {service['domain']}",
                fg=typer.colors.GREEN)
    typer.secho(
        f"Health Path: {service['health_path']}",
        fg=typer.colors.GREEN)
    typer.secho(f"Enabled: {service['enabled']}",
                fg=typer.colors.GREEN)
