from dataclasses import dataclass
from typing import Any

@dataclass
class Message:
    type: Any
    data: dict