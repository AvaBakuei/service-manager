import typer
from pathlib import Path

from .project import initialize_project
from .exceptions import ProjectAlreadyExistsError

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


if __name__ == "__main__":
    app()
