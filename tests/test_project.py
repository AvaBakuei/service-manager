import pytest

from pathlib import Path

from service_manager.project import initialize_project
from service_manager.exceptions import ProjectAlreadyExistsError


def test_initialize_project_creates_files(tmp_path: Path):
    initialize_project(tmp_path)

    services_file = tmp_path / "services.yml"

    assert services_file.exists()
    assert services_file.read_text(encoding="utf-8") == "services: {}\n"
    assert (tmp_path / ".env.example").exists()
    assert (tmp_path / "generated").is_dir()


def test_initialize_project_does_not_overwrite_existing_config(tmp_path: Path):
    services_file = tmp_path / "services.yml"

    services_file.write_text(
        "services:\n  test:\n  image:nginx\n",
        encoding="utf-8"
    )

    with pytest.raises(ProjectAlreadyExistsError):
        initialize_project(tmp_path)

    assert services_file.read_text(
        encoding="utf-8") == ("services:\n  test:\n  image:nginx\n")
