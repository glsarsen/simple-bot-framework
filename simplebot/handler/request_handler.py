from __future__ import annotations
from abc import ABC, abstractmethod

from simplebot.message_tree import Element

from simplebot.question_worker import QuestionWorker
from simplebot.user import UserDatabase
from simplebot.message_tree import ElementTree


class Handler(ABC):
    """abstract class (interface) of request handler

    handles elements in element tree, and executes corresponding actions
    """

    def set_element_tree(self, element_tree: ElementTree):
        """creates element_tree variable as a reference to
        ElementTree class containing current Handler

        Is called from ElementTree class

        Args:
            element_tree (ElementTree): ElementTree class containing current Handler
        """
        self.element_tree = element_tree

    def set_user_database(self, user_database: UserDatabase):
        """registers user_databse object to interact with user database

        Args:
            user_database (UserDatabase): object to handle working with user database
        """
        self.user_database = user_database

    def set_question_worker(self, question_worker: QuestionWorker):
        """Registers question worker to analyze questions from user

        Args:
            question_worker (QuestionWorker): qusetion worker object
        """
        self.question_worker = question_worker

    @abstractmethod
    def handle(self, element: Element, request):
        """abstract method to handle current element

        Args:
            element (Element): element to handle
            request (ViberMessageRequest): request that triggered current element
        """
        return

    @abstractmethod
    def process_request(self, request):
        """Process the incoming request - check signature, send initial message, send message on failure, handle user actions

        Args:
            request (Any): request to process
        """
        return
