from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def generate_compose(services: list[dict], output_path: Path) -> None:
    template_dir = Path(__file__).parent / "templates"

    env = Environment(loader=FileSystemLoader(template_dir))

    template = env.get_template("docker-compose.yml.j2")
    result = template.render(services=services)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        result,
        encoding="utf-8"
    )


def generate_applications(services: list[dict], output_path: Path) -> None:
    applications = []

    for service in services:
        applications.append({
            "name": service["name"],
            "image": service["image"],
            "domain": service["domain"],
            "internal_port": service["internal_port"],
            "enabled": service["enabled"],
        })

    template_dir = Path(__file__).parent / "templates"

    env = Environment(loader=FileSystemLoader(template_dir))

    template = env.get_template("applications.yml.j2")
    result = template.render(applications=applications)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        result,
        encoding="utf-8"
    )
