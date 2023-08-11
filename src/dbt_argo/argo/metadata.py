from dataclasses import dataclass


@dataclass
class Metadata:
    """Metadata model"""

    name: str
    namespace: str = "default"
