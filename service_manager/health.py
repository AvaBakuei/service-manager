import httpx
import time


def health_check(service: dict) -> dict:
    domain = service["domain"]
    health = service["health_path"]
    url = f"http://{domain}{health}"

    start = time.perf_counter()
    try:
        response = httpx.get(url, timeout=5)
    except httpx.ConnectError:
        return {"status": "Unhealthy",
                "error": "Connection error"}
    except httpx.TimeoutException:
        return {"status": "Unhealthy",
                "error": "Connection timed out"}

    end = time.perf_counter()
    response_time = (end - start) * 1000

    if response.status_code == 200:
        result = {
            "status": "Healthy",
            "http_status": response.status_code,
            "response_time": round(response_time),
            "error": None
        }
    else:
        result = {
            "status": "Unhealthy",
            "http_status": response.status_code,
            "response_time": round(response_time),
            "error": "Connection timed out"
        }
    return result


def health_check_all(services: dict) -> dict:
    results = {}

    for service_name, service in services.items():
        results[service_name] = health_check(service)
    return results
