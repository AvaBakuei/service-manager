import httpx
from unittest.mock import patch
from service_manager.health import health_check, health_check_all


@patch("service_manager.health.httpx.get")
def test_health_check_success(mock_get):
    mock_get.return_value = httpx.Response(200)

    service = {
        "domain": "whoami.example.com",
        "health_path": "/"
    }

    result = health_check(service)

    assert result["status"] == "Healthy"
    assert result["http_status"] == 200
    assert "response_time" in result


@patch("service_manager.health.httpx.get")
def test_health_check_server_error(mock_get):
    mock_get.return_value = httpx.Response(500)

    service = {
        "domain": "whoami.example.com",
        "health_path": "/"
    }

    result = health_check(service)

    assert result["status"] == "Unhealthy"
    assert result["http_status"] == 500
    assert "response_time" in result


@patch("service_manager.health.httpx.get")
def test_health_check_timeout(mock_get):
    mock_get.side_effect = httpx.TimeoutException("Connection timed out")

    service = {
        "domain": "whoami.example.com",
        "health_path": "/"
    }

    result = health_check(service)

    assert result["status"] == "Unhealthy"
    assert result["error"] == "Connection timed out"


@patch("service_manager.health.httpx.get")
def test_health_check_dns_connection(mock_get):
    mock_get.side_effect = httpx.ConnectError("DNS error")

    service = {
        "domain": "invald.example.com",
        "health_path": "/"
    }

    result = health_check(service)

    assert result["status"] == "Unhealthy"
    assert result["error"] == "Connection error"


@patch("service_manager.health.httpx.get")
def test_health_check_connection_refused(mock_get):
    mock_get.side_effect = httpx.ConnectError("Connection refused")

    service = {
        "domain": "localhost",
        "health_path": "/",
    }

    result = health_check(service)

    assert result["status"] == "Unhealthy"
    assert result["error"] == "Connection error"


@patch("service_manager.health.httpx.get")
def test_health_check_all(mock_get):
    mock_get.side_effect = [
        httpx.Response(200),
        httpx.ConnectError("Connection refused"),
    ]

    services = {
        "whoami": {
            "domain": "whoami.example.local",
            "health_path": "/",
        },
        "api": {
            "domain": "api.example.local",
            "health_path": "/health",
        },
    }

    results = health_check_all(services)

    assert results["whoami"]["status"] == "Healthy"
    assert results["api"]["status"] == "Unhealthy"
