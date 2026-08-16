from pathlib import Path

import pytest
import yaml
from jinja2 import Environment, FileSystemLoader

from service_manager.generator import generate_compose


def test_compose_template():
    template_dir = (
        Path(__file__).parent.parent
        / "service_manager"
        / "templates"
    )

    env = Environment(
        loader=FileSystemLoader(template_dir)
    )

    template = env.get_template("docker-compose.yml.j2")

    services = [
        {
            "name": "whoami",
            "image": "traefik/whoami",
            "internal_port": 80,
            "domain": "whoami.example.local",
            "enabled": True,
        }
    ]

    result = template.render(services=services)

    assert "whoami:" in result
    assert "traefik/whoami" in result
    assert "whoami.example.local" in result
    assert "server.port=80" in result
    assert "proxy" in result


def test_compose_template_ignores_disabled_service():
    template_dir = (
        Path(__file__).parent.parent
        / "service_manager"
        / "templates"
    )

    env = Environment(
        loader=FileSystemLoader(template_dir)
    )

    template = env.get_template("docker-compose.yml.j2")

    services = [
        {
            "name": "whoami",
            "image": "traefik/whoami",
            "internal_port": 80,
            "domain": "whoami.example.local",
            "enabled": True,
        },
        {
            "name": "api",
            "image": "company/api",
            "internal_port": 3000,
            "domain": "api.example.local",
            "enabled": False,
        },
    ]

    result = template.render(services=services)

    assert "whoami:" in result
    assert "api:" not in result


def test_generate_compose(tmp_path: Path):
    output_path = tmp_path / "generated" / "docker-compose.yml"

    services = [
        {
            "name": "whoami",
            "image": "traefik/whoami",
            "internal_port": 80,
            "domain": "whoami.example.local",
            "enabled": True,
        }
    ]

    generate_compose(services, output_path)

    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "whoami:" in content
    assert "traefik/whoami" in content
    assert "whoami.example.local" in content
    assert "server.port=80" in content
    assert "proxy" in content


def test_generate_compose_ignores_disabled_services(
    tmp_path: Path,
):
    output_path = tmp_path / "docker-compose.yml"

    services = [
        {
            "name": "whoami",
            "image": "traefik/whoami",
            "internal_port": 80,
            "domain": "whoami.example.local",
            "enabled": True,
        },
        {
            "name": "api",
            "image": "company/api",
            "internal_port": 3000,
            "domain": "api.example.local",
            "enabled": False,
        },
    ]

    generate_compose(services, output_path)

    content = output_path.read_text(encoding="utf-8")

    assert "whoami:" in content
    assert "api:" not in content


def test_generate_multiple_services(tmp_path: Path):
    output_path = tmp_path / "docker-compose.yml"

    services = [
        {
            "name": "whoami",
            "image": "traefik/whoami",
            "internal_port": 80,
            "domain": "whoami.example.local",
            "enabled": True,
        },
        {
            "name": "nginx",
            "image": "nginx:alpine",
            "internal_port": 80,
            "domain": "nginx.example.local",
            "enabled": True,
        },
    ]

    generate_compose(services, output_path)

    content = output_path.read_text(encoding="utf-8")

    assert "whoami:" in content
    assert "nginx:" in content


def test_generate_traefik_configuration(tmp_path: Path):
    output_path = tmp_path / "docker-compose.yml"

    services = [
        {
            "name": "whoami",
            "image": "traefik/whoami",
            "internal_port": 8080,
            "domain": "whoami.example.local",
            "enabled": True,
        }
    ]

    generate_compose(services, output_path)

    content = output_path.read_text(encoding="utf-8")

    assert (
        "traefik.http.routers.whoami.rule="
        "Host(`whoami.example.local`)"
    ) in content

    assert (
        "traefik.http.services.whoami."
        "loadbalancer.server.port=8080"
    ) in content

    assert "proxy:" in content
    assert "external: true" in content


def test_generated_compose_is_valid_yaml(tmp_path: Path):
    output_path = tmp_path / "docker-compose.yml"

    services = [
        {
            "name": "whoami",
            "image": "traefik/whoami",
            "internal_port": 80,
            "domain": "whoami.example.local",
            "enabled": True,
        }
    ]

    generate_compose(services, output_path)

    content = output_path.read_text(encoding="utf-8")

    data = yaml.safe_load(content)

    assert data["services"]["whoami"]["image"] == "traefik/whoami"
    assert data["networks"]["proxy"]["external"] is True
