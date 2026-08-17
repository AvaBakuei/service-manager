from unittest.mock import patch
from service_manager.docker import run_compose_command, compose_up, compose_down, compose_ps, compose_logs

COMPOSE_FILE = "generated/docker-compose.yml"


@patch("service_manager.docker.subprocess.run")
def test_run_compose_command(mock_run):
    run_compose_command(["ps"])

    mock_run.assert_called_once_with([
        "docker", "compose", "-f", COMPOSE_FILE, "ps"
    ], check=True)


@patch("service_manager.docker.subprocess.run")
def test_compose_up(mock_run):
    compose_up()

    mock_run.assert_called_once_with([
        "docker", "compose", "-f", COMPOSE_FILE, "up", "-d"
    ], check=True)


@patch("service_manager.docker.subprocess.run")
def test_compose_down(mock_run):
    compose_down()

    mock_run.assert_called_once_with([
        "docker", "compose", "-f", COMPOSE_FILE, "down"
    ], check=True)


@patch("service_manager.docker.subprocess.run")
def test_compose_ps(mock_run):
    compose_ps()

    mock_run.assert_called_once_with([
        "docker", "compose", "-f", COMPOSE_FILE, "ps"
    ], check=True)


@patch("service_manager.docker.subprocess.run")
def test_compose_logs(mock_run):
    compose_logs("whoami")

    mock_run.assert_called_once_with([
        "docker", "compose", "-f", COMPOSE_FILE, "logs", "whoami"
    ], check=True)
