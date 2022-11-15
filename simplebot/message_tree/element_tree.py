from __future__ import annotations
from typing import Any
import json

from simplebot.message_tree import Element
from simplebot.message_tree import ElementType


class ElementTree:
    """Message tree class

    contains all of the bot messages, and tracks current state of dialogue with user
    """

    def __init__(self):
        """
        Args:
            handler (Handler): message handler
            state (State): initial state of ElementTree
        """
        self.element_list: list[Element] = []

    def add_element(self, type: ElementType, data: Any):
        """adds a new element to ElementTree

        Args:
            type (ElementType): type of element to add to ElementTree
            data (Any): associated data of an element
        """
        self.element_list.append(Element(type, data))
        return self

    def get_element(self, index):
        return self.element_list[index]

    def get_length(self):
        return len(self.element_list)

    def from_object(self, obj):
        for element in obj:
            self.add_element(element["element"], element["data"])

    def from_file(self, file):
        with open("messages.json", "r") as f:
            elements = json.load(f)
            self.from_object(elements)

    def find_branch(self, branch: str):
        """looks through ElementTree message_list for a branch
        возвращает индекс найденной ветки

        Args:
            branch (str): branch to look for
        """
        for index, element in enumerate(self.element_list):
            if (
                element.type == ElementType.BRANCH
                or element.type == ElementType.TRIGGER
            ) and element.data == branch:
                return index
        return None
