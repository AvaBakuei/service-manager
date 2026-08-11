import pytest

from service_manager.validation import validate_service, validate_service_name
from service_manager.models import Service
from service_manager.exceptions import ServiceAlreadyExistsError


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
