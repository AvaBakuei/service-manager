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
