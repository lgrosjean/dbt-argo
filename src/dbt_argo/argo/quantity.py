from dataclasses import dataclass


@dataclass
class Quantity:
    """Base quantity class"""

    cpu: str
    memory: str


@dataclass
class Limits(Quantity):
    """Limits quantity"""

    cpu: str = "0.15"
    memory: str = "300Mi"


@dataclass
class Requests(Quantity):
    """Requests quantity"""

    cpu: str = "0.1"
    memory: str = "200Mi"
