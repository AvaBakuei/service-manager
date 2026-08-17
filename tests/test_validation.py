from service_manager.exceptions import ServiceAlreadyExistsError
from service_manager.models import Service
import pytest

from service_manager.validation import validate_service, validate_service_name, validate_config


def test_validate_service():
    service = Service(
        name="whoami",
        image="traefik/whoami",
        internal_port=80,
        domain="whoami.example.local",
        enabled=True,
        health_path="/",
    )

    validate_service(service)


def test_empty_service_name():
    service = Service(
        name="   ",
        image="traefik/whoami",
        internal_port=80,
        domain="whoami.example.local",
        enabled=True,
        health_path="/",
    )

    with pytest.raises(ValueError, match="Service name"):
        validate_service(service)


def test_empty_docker_image():
    service = Service(
        name="whoami",
        image="   ",
        internal_port=80,
        domain="whoami.example.local",
        enabled=True,
        health_path="/",
    )

    with pytest.raises(ValueError, match="Docker image"):
        validate_service(service)


def test_invalid_port():
    service = Service(
        name="whoami",
        image="traefik/whoami",
        internal_port=70000,
        domain="whoami.example.local",
        enabled=True,
        health_path="/",
    )

    with pytest.raises(ValueError, match="Internal port"):
        validate_service(service)


def test_empty_domain_name():
    service = Service(
        name="whoami",
        image="traefik/whoami",
        internal_port=80,
        domain="   ",
        enabled=True,
        health_path="/",
    )

    with pytest.raises(ValueError, match="Domain"):
        validate_service(service)


def test_invalid_health_path():
    service = Service(
        name="whoami",
        image="traefik/whoami",
        internal_port=80,
        domain="whoami.example.local",
        enabled=True,
        health_path="health",
    )

    with pytest.raises(ValueError, match="Health path"):
        validate_service(service)


def test_duplicate_service_name():
    services = {
        "whoami": {
            "image": "traefik/whoami",
        }
    }

    with pytest.raises(ServiceAlreadyExistsError, match="already exists"):
        validate_service_name("whoami", services)


def test_validate_config():
    config = {
        "services": {
            "whoami": {
                "name": "whoami",
                "image": "treafik/whoami",
                "internal_port": 8080,
                "domain": "whoami.example.com",
                "enabled": True,
                "health_path": "/"
            }
        }
    }

    errors = validate_config(config)
    assert errors == []


def test_validate_config_empty_image():
    config = {
        "services": {
            "whoami": {
                "name": "whoami",
                "image": "",
                "internal_port": 80,
                "domain": "whoami.example.local",
                "enabled": True,
                "health_path": "/",
            }
        }
    }

    errors = validate_config(config)

    assert "Docker image cannot be empty." in errors[0]


def test_validate_config_invalid_port():
    config = {
        "services": {
            "whoami": {
                "name": "whoami",
                "image": "traefik/whoami",
                "internal_port": 70000,
                "domain": "whoami.example.local",
                "enabled": True,
                "health_path": "/",
            }
        }
    }

    errors = validate_config(config)

    assert (
        "Internal port must be between 1 and 65535."
        in errors[0]
    )


def test_validate_config_invalid_health_path():
    config = {
        "services": {
            "whoami": {
                "name": "whoami",
                "image": "traefik/whoami",
                "internal_port": 80,
                "domain": "whoami.example.local",
                "enabled": True,
                "health_path": "health",
            }
        }
    }

    errors = validate_config(config)

    assert "Health path must start with '/'" in errors[0]


def test_validate_config_duplicate_domain():
    config = {
        "services": {
            "whoami": {
                "name": "whoami",
                "image": "traefik/whoami",
                "internal_port": 80,
                "domain": "example.com",
                "enabled": True,
                "health_path": "/",
            },
            "api": {
                "name": "api",
                "image": "company/api",
                "internal_port": 3000,
                "domain": "example.com",
                "enabled": True,
                "health_path": "/",
            },
        }
    }

    errors = validate_config(config)

    assert "Duplicate domain: example.com" in errors


def test_validate_config_no_enabled_service():
    config = {
        "services": {
            "whoami": {
                "name": "whoami",
                "image": "traefik/whoami",
                "internal_port": 80,
                "domain": "whoami.example.local",
                "enabled": False,
                "health_path": "/",
            }
        }
    }

    errors = validate_config(config)

    assert "At least one service must be enabled." in errors


def test_validate_config_collects_multiple_errors():
    config = {
        "services": {
            "whoami": {
                "name": "whoami",
                "image": "",
                "internal_port": 70000,
                "domain": "example.com",
                "enabled": False,
                "health_path": "health",
            },
            "api": {
                "name": "api",
                "image": "company/api",
                "internal_port": 3000,
                "domain": "example.com",
                "enabled": False,
                "health_path": "/",
            },
        }
    }

    errors = validate_config(config)

    assert any("Docker image cannot be empty." in error for error in errors)

    assert any(
        "Internal port must be between 1 and 65535." in error
        for error in errors
    )

    assert any(
        "Health path must start with '/'" in error
        for error in errors
    )

    assert any(
        "Duplicate domain: example.com" in error
        for error in errors
    )

    assert any(
        "At least one service must be enabled." in error
        for error in errors
    )
