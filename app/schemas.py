from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any
from uuid import UUID


class FieldEnum(Enum):
    def _generate_next_value_(  # type: ignore
        name: str, start: int, count: int, last_values: list
    ) -> Any:
        return count

    id = auto()
    parent_id = auto()
    title = auto()
    registered_in = auto()


@dataclass
class Node:
    id: UUID
    parent_id: UUID
    title: str
    registered_in: datetime
