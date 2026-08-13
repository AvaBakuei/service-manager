import pytest

from service_manager.exceptions import ServiceDoesNotExistError
from service_manager.service import services_list, show_service


def test_services_list_with_no_services():
    config = {
        "services": {}
    }

    with pytest.raises(ServiceDoesNotExistError):
        services_list(config)


def test_services_list_with_services():
    config = {
        "services": {
            "whoami": {
                "name": "whoami",
                "image": "traefik/whoami",
                "internal_port": 80,
                "domain": "whoami.example.local",
                "enabled": True,
                "health_path": "/",
            },
            "api": {
                "name": "api",
                "image": "company/api",
                "internal_port": 3000,
                "domain": "api.example.local",
                "enabled": False,
                "health_path": "/health",
            },
        }
    }

    table = services_list(config)

    assert table.row_count == 2


def test_show_service(capsys):
    config = {
        "services": {
            "whoami": {
                "name": "whoami",
                "image": "traefik/whoami",
                "internal_port": 80,
                "domain": "whoami.example.local",
                "enabled": True,
                "health_path": "/",
            }
        }
    }

    show_service("whoami", config)

    captured = capsys.readouterr()

    assert "Name: whoami" in captured.out
    assert "Image: traefik/whoami" in captured.out
    assert "Internal Port: 80" in captured.out
    assert "Domain: whoami.example.local" in captured.out


def test_show_service_does_not_exist():
    config = {
        "services": {}
    }

    with pytest.raises(ServiceDoesNotExistError):
        show_service("whoami", config)
