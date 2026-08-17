import subprocess

COMPOSE_FILE = "generated/docker-compose.yml"


def run_compose_command(command: list[str]) -> None:
    subprocess.run([
        "docker", "compose", "-f", COMPOSE_FILE, *command
    ], check=True)


def compose_up() -> None:
    run_compose_command(["up", "-d"])


def compose_down() -> None:
    run_compose_command(["down"])


def compose_ps() -> None:
    run_compose_command(["ps"])


def compose_logs(service_name: str) -> None:
    run_compose_command(["logs", service_name])
