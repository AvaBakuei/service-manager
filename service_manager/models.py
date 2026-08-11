from dataclasses import dataclass, asdict


@dataclass
class Service:
    name: str
    image: str
    internal_port: int
    domain: str
    enabled: bool
    health_path: str

    def to_dict(self) -> dict:
        return asdict(self)
