from __future__ import annotations
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from simplebot.message_tree import ElementType


class Element:
    """abstraction of a message from bot to user

    contains message type and associated data
    """

    def __init__(self, type: ElementType, data: Any):
        self.type = type
        self.data = data

    def __repr__(self):
        return f"Element({self.type}, {self.data})"
