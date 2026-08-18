from unittest.mock import patch
from typer.testing import CliRunner
from service_manager.cli import app

runner = CliRunner()


@patch("service_manager.cli.compose_up")
def test_up(mock_compose_up):
    result = runner.invoke(app, ["up"])

    assert result.exit_code == 0
    mock_compose_up.assert_called_once()


@patch("service_manager.cli.compose_down")
def test_down(mock_compose_down):
    result = runner.invoke(app, ["down"])

    assert result.exit_code == 0
    mock_compose_down.assert_called_once()


@patch("service_manager.cli.compose_ps")
def test_ps(mock_compose_ps):
    result = runner.invoke(app, ["ps"])

    assert result.exit_code == 0
    mock_compose_ps.assert_called_once()


@patch("service_manager.cli.compose_logs")
def test_logs(mock_compose_logs):
    result = runner.invoke(app, ["logs", "whoami"])

    assert result.exit_code == 0
    mock_compose_logs.assert_called_once_with("whoami")


@patch("service_manager.cli.health_check")
def test_health(mock_health_check):
    mock_health_check.return_value = {
        "status": "Healthy",
        "http_status": 200,
        "response_time": 42,
        "error": None,
    }

    result = runner.invoke(app, ["health", "whoami"])

    assert result.exit_code == 0
    mock_health_check.assert_called_once()

    assert "Service: whoami" in result.stdout
    assert "Status: Healthy" in result.stdout
    assert "HTTP Status: 200" in result.stdout
    assert "Response Time: 42 ms" in result.stdout


@patch("service_manager.cli.health_check_all")
def test_health_all(mock_health_check_all):
    mock_health_check_all.return_value = {
        "whoami": {
            "status": "Healthy",
            "http_status": 200,
            "response_time": 42,
            "error": None,
        },
        "api": {
            "status": "Unhealthy",
            "http_status": None,
            "response_time": None,
            "error": "Connection timed out",
        },
    }

    result = runner.invoke(app, ["health", "--all"])

    assert result.exit_code == 0
    mock_health_check_all.assert_called_once()

    assert "Service: whoami" in result.stdout
    assert "Status: Healthy" in result.stdout
    assert "Service: api" in result.stdout
    assert "Status: Unhealthy" in result.stdout
    assert "Error: Connection timed out" in result.stdout
