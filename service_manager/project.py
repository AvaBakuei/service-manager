from pathlib import Path

from .exceptions import ProjectAlreadyExistsError


def initialize_project(base_path: Path) -> None:
    services_file = base_path / "services.yml"
    env_file = base_path / ".env.example"
    generated_directory = base_path / "generated"

    if services_file.exists():
        raise ProjectAlreadyExistsError("services.yml already exists.")

    generated_directory.mkdir(exist_ok=True)

    services_file.write_text(
        "services: {}\n",
        encoding="utf-8"
    )

    env_file.touch()
