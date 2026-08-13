from pathlib import Path
import yaml


# Read From services.yaml file
def load_config(path: Path) -> dict:
    if not path.exists():
        return {"services": {}}

    with path.open("r", encoding="utf-8") as file:
        # yaml_load convert yaml file to Python Dictionary
        data = yaml.safe_load(file)

    if data is None:
        return {"services": {}}

    return data


# Write and Save config
def save_config(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(
            data,
            file,
            sort_keys=False,
            allow_unicode=True
        )


def get_config_path() -> Path:
    return Path.cwd() / "services.yml"
