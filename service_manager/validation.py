from .exceptions import ServiceAlreadyExistsError
from .models import Service


def get_service_validation_errors(service) -> list[str]:
    errors = []

    if not service.name.strip():
        errors.append("Service name cannot be empty.")

    if not service.image.strip():
        errors.append("Docker image cannot be empty.")

    if not 1 <= service.internal_port <= 65535:
        errors.append(
            "Internal port must be between 1 and 65535."
        )

    if not service.domain.strip():
        errors.append("Domain cannot be empty.")

    if not service.health_path.startswith("/"):
        errors.append("Health path must start with '/'.")

    return errors


def validate_service(service) -> None:
    errors = get_service_validation_errors(service)

    if errors:
        raise ValueError("\n".join(errors))


def validate_service_name(name: str, services: dict) -> None:
    if name in services:
        raise ServiceAlreadyExistsError(f"Service {name} already exists.")


def validate_config(config: dict) -> list[str]:
    errors = []
    services = config.get("services")
    if not services:
        errors.append("No service found.")
        return errors

    domains = set()
    enabled_services = 0

    for service_name, service_data in services.items():

        # Validate service fields
        try:
            service = Service.from_dict(service_data)
            validate_service(service)
        except ValueError as error:
            errors.append(
                f"Service '{service_name}': {error}"
            )

        # Check duplicate domains
        domain = service_data.get("domain", "").strip()
        if domain in domains:
            errors.append(f"Duplicate domain: {domain}")
        else:
            domains.add(domain)

        # Count enabled services
        if service_data.get("enabled", False):
            enabled_services += 1
    if enabled_services == 0:
        errors.append(
            "At least one service must be enabled."
        )

    return errors
