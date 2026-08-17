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
