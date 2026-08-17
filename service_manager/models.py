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

    @classmethod
    def from_dict(cls, data: dict) -> "Service":
        return cls(
            name=data["name"],
            image=data["image"],
            internal_port=data["internal_port"],
            domain=data["domain"],
            enabled=data["enabled"],
            health_path=data["health_path"],
        )
