from pathlib import Path

from service_manager.config import load_config, save_config


def test_save_and_load_config(tmp_path: Path):
    config_file = tmp_path / "services.yml"

    data = {
        "service": {
            "whoami": {
                "image": "traefik/whoami",
                "internal_port": 80,
            }
        }
    }

    save_config(config_file, data)
    result = load_config(config_file)
    assert data == result


def test_add_service_to_config(tmp_path: Path):
    config_file = tmp_path / "services.yml"
    data = {
        "services": {},
    }

    service = {
        "name": "whoami",
        "image": "traefik/whoami",
        "internal_port": 80,
        "domain": "whoami.example.local",
        "enabled": True,
        "health_path": "/",
    }

    data["services"]["whoami"] = service

    save_config(config_file, data)

    result = load_config(config_file)

    assert result["services"]["whoami"] == service
