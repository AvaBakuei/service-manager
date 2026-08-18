# Service Manager

A CLI tool for defining, validating, generating, and managing Docker services.

## Requirements

- Python 3.10+
- Docker
- Docker Compose
- Git

## Installation

Clone the repository:

```bash
git clone https://github.com/AvaBakuei/service-manager.git
cd service-manager
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
pip install -e .
```

For development and testing:

```bash
pip install -e ".[dev]"
```

## Usage

Service Manager provides commands for creating, validating, generating, and managing Docker services.

### Initialize a project

```bash
service-manager init
```

### Add a service

```bash
service-manager add
```

### List services

```bash
service-manager list
```

### Show a service

```bash
service-manager show <service-name>
```

### Validate configuration

```bash
service-manager validate
```

This checks the service configuration and reports configuration errors.

### Generate Docker Compose

```bash
service-manager generate
```

The generated Docker Compose file is created at:

```text
generated/docker-compose.yml
```

### Start services

```bash
service-manager up
```

### Stop services

```bash
service-manager down
```

### Show running services

```bash
service-manager ps
```

### Show service logs

```bash
service-manager logs <service-name>
```

### Check service health

Check a specific service:

```bash
service-manager health <service-name>
```

Check all services:

```bash
service-manager health --all
```

## Configuration

Services are defined in `services.yml`.

Example:

```yaml
services:
  whoami:
    name: whoami
    image: traefik/whoami
    internal_port: 80
    domain: whoami.example.com
    enabled: true
    health_path: /
```

### Configuration fields

| Field           | Description                                   |
| --------------- | --------------------------------------------- |
| `name`          | Service name                                  |
| `image`         | Docker image used by the service              |
| `internal_port` | Port used by the service inside the container |
| `domain`        | Domain used by Traefik                        |
| `enabled`       | Whether the service is enabled                |
| `health_path`   | HTTP path used for health checks              |

## Docker Compose

The `generate` command uses the service configuration to generate a Docker Compose file.

Example generated configuration:

```yaml
services:
  whoami:
    image: service-manager-whoami:latest
    restart: unless-stopped
    networks:
      - proxy
    labels:
      traefik.enable: "true"
      traefik.http.routers.whoami.rule: Host(`whoami.example.com`)
      traefik.http.services.whoami.loadbalancer.server.port: "80"

networks:
  proxy:
    name: proxy
    external: true
```

The generated configuration uses Traefik labels to route HTTP requests to the configured service.

## Architecture

The project is organized into several small modules, with each module responsible for a specific part of the application.

```text
                         CLI
                          │
                          ▼
                       cli.py
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
       Config         Validation        Health
          │               │                │
          ▼               ▼                ▼
       YAML data      Service rules      HTTPX
                          │
                          ▼
                      Generator
                          │
                          ▼
                        Jinja2
                          │
                          ▼
                 Docker Compose file
                          │
                          ▼
                       Docker
```

### Main components

- `cli.py` — Defines the command-line interface using Typer.
- `config.py` — Loads and manages YAML configuration.
- `models.py` — Contains the `Service` data model.
- `service.py` — Handles service-related operations.
- `validation.py` — Validates service and configuration data.
- `generator.py` — Generates Docker Compose configuration using Jinja2.
- `docker.py` — Runs Docker Compose commands using `subprocess`.
- `health.py` — Performs HTTP health checks using HTTPX.
- `project.py` — Handles project initialization.
- `exceptions.py` — Contains custom application exceptions.

## Project Structure

```text
service-manager/
├── service_manager/
│   ├── cli.py
│   ├── config.py
│   ├── docker.py
│   ├── exceptions.py
│   ├── generator.py
│   ├── health.py
│   ├── models.py
│   ├── project.py
│   ├── service.py
│   ├── validation.py
│   └── templates/
│       └── docker-compose.yml.j2
│
├── tests/
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_docker.py
│   ├── test_generator.py
│   ├── test_health.py
│   ├── test_models.py
│   ├── test_project.py
│   ├── test_service.py
│   └── test_validation.py
│
├── services.yml
├── pyproject.toml
├── README.md
└── .gitignore
```

## Testing

The project uses `pytest` for testing.

Run all tests:

```bash
pytest
```

The test suite covers:

- CLI commands
- Configuration handling
- Docker commands
- Docker Compose generation
- Health checks
- Service models
- Project initialization
- Service management
- Configuration validation

## Troubleshooting

### Docker is not running

Make sure Docker Desktop is running before using Docker-related commands:

```bash
service-manager up
```

### Docker image cannot be found

Make sure the Docker image specified in `services.yml` exists.

You can check available local images with:

```bash
docker image ls
```

You can also pull an image manually:

```bash
docker pull <image-name>
```

### Docker Compose configuration is invalid

First validate the configuration:

```bash
service-manager validate
```

Then regenerate the Docker Compose file:

```bash
service-manager generate
```

You can inspect the generated configuration with:

```bash
docker compose -f generated/docker-compose.yml config
```

### Health check fails

Check the `domain` and `health_path` values in `services.yml`.

For example:

```yaml
domain: whoami.example.com
health_path: /
```

Check whether the service is running:

```bash
service-manager ps
```

Check the service logs:

```bash
service-manager logs whoami
```

You can also run the health check directly:

```bash
service-manager health whoami
```

### Proxy network does not exist

The generated Compose configuration uses an external Docker network named `proxy`.

Check existing networks:

```bash
docker network ls
```

If the network does not exist, create it:

```bash
docker network create proxy
```

## Current Limitations

- Health checks currently use HTTP.
- Health check URLs use the `http://` scheme.
- Docker commands require Docker to be installed and running.
- The generated Docker Compose configuration expects an external Docker network named `proxy`.
- Service configuration is stored in a YAML file.
- The project currently focuses on local Docker Compose management.
- Authentication and authorization for Docker services are not handled by the application.

## Development

Install the development dependencies:

```bash
pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

## License

This project is currently provided for development and educational purposes.
