from service_manager.models import Service


def test_service_model():
    service = Service(
        name="whoami",
        image="traefik/whoami",
        internal_port=80,
        domain="whoami.example.local",
        enabled=True,
        health_path="/",
    )

    assert service.name == "whoami"
    assert service.image == "traefik/whoami"
    assert service.internal_port == 80
    assert service.domain == "whoami.example.local"
    assert service.enabled is True
    assert service.health_path == "/"


def test_service_to_dict():
    service = Service(
        name="whoami",
        image="traefik/whoami",
        internal_port=80,
        domain="whoami.example.local",
        enabled=True,
        health_path="/",
    )

    assert service.to_dict() == {
        "name": "whoami",
        "image": "traefik/whoami",
        "internal_port": 80,
        "domain": "whoami.example.local",
        "enabled": True,
        "health_path": "/",
    }


def test_service_from_dict():
    data = {
        "name": "whoami",
        "image": "traefik/whoami",
        "internal_port": 80,
        "domain": "whoami.example.local",
        "enabled": True,
        "health_path": "/",
    }

    service = Service.from_dict(data)

    assert service.name == "whoami"
    assert service.image == "traefik/whoami"
    assert service.internal_port == 80
    assert service.domain == "whoami.example.local"
    assert service.enabled is True
    assert service.health_path == "/"
