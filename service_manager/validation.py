from .models import Service
from .exceptions import ServiceAlreadyExistsError


def validate_service(service) -> None:
    if not service.name.strip():
        raise ValueError("Service name cannot be empty.")
    if not service.image.strip():
        raise ValueError("Docker image cannot be empty.")
    if not 1 <= service.internal_port <= 65535:
        raise ValueError("Internal port must be between 1 and 65535.")
    if not service.domain.strip():
        raise ValueError("Domain cannot be empty.")
    if not service.health_path.startswith("/"):
        raise ValueError("Health path must start with '/'.")
#  Prevent the duplicate service name


def validate_service_name(name: str, services: dict) -> None:
    if name in services:
        raise ServiceAlreadyExistsError(f"Service {name} already exists.")
