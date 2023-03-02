import json
import logging
import datetime

from flask import url_for, Response
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.messages import TextMessage
from viberbot.api.messages import RichMediaMessage
from viberbot.api.messages import PictureMessage
from viberbot.api.messages import KeyboardMessage

from simplebot.google_sheets_writer import google_sheets_writer
from simplebot.handler.request_handler import Handler
from simplebot.message_tree import ElementTree, ElementType
from simplebot.question_worker import QuestionWorker
from simplebot.user import UserDatabase
from simplebot.viber_config import viber
from simplebot.analytics import Analytics
import simplebot.bot_messages as bm


class ViberHandler(Handler):
    """implementation of Handler interface for Viber messenger"""

    def __init__(
        self, element_tree: ElementTree = None, question_worker: QuestionWorker = None
    ):
        """

        Args:
            element_tree (ElementTree, optional): uses it to store messages
        for the dialogue with user. Defaults to None.
            question_worker (QuestionWorker, optional): uses it to process
        questions from user with a neural network. Defaults to None.
        """
        self.element_tree = element_tree
        self.question_worker = question_worker
        self.user_database = UserDatabase()
        self.analytics = Analytics()

        # Set up the logger for the bot
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s\n"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def handle(self, request: ViberMessageRequest):
        """Sends messages to user depending on current element object,
        also processes user input (in case element.type was ElementType.INPUT
        or ElementType.QUEESTION)

        Args:
            element (Element): element to handle
            request (ViberMessageRequest): request that triggered current element
        """
        user_viber_id = request.sender.id
        user = self.user_database.get_user(user_viber_id)
        user.last_action_date = datetime.datetime.now()
        message = request.message.text

        if user.dialog_status == "message":
            if user.step_index is None:
                index = self.element_tree.find_branch(message)
                if index is not None:
                    user.step_index = index + 1
                else:
                    # process as a question with a Neural Network, find a branch and write to user.step_index
                    branch = self.question_worker.process_question(message)
                    self.analytics.add_question(
                        viber_id=user_viber_id, question=message
                    )
                    index = self.element_tree.find_branch(branch)
                    user.step_index = index + 1
        if user.dialog_status == "input":
            element = self.element_tree.get_element(user.step_index)
            if element.data == "feedback":
                # write feedback to google sheets
                gsw = google_sheets_writer()
                gsw.save_feedback_to_gsheets(user, message)
                self.analytics.add_feedback(viber_id=user_viber_id, feedback=message)
            if element.data == "user_name":
                user.viber_id = request.sender.id
                user.login = request.sender.name
                user.name = request.message.text
            if element.data == "user_phone":
                user.phone = request.message.text
            if element.data == "google_login":
                user.google_login = request.message.text
            if element.data == "google_password":
                user.google_password = request.message.text
            if element.data == "linkedin_login":
                user.linkedin_login = request.message.text
            if element.data == "linkedin_password":
                user.linkedin_password = request.message.text
            if element.data == "discord_login":
                user.discord_login = request.message.text

            user.step_index += 1
            user.dialog_status = "message"
            self.user_database.update_user()
        while True:
            print(user)
            element = self.element_tree.get_element(user.step_index)
            if element.type == ElementType.BRANCH:
                user.step_index = None
                self.user_database.update_user()
                return
            if element.type == ElementType.INPUT:
                user.dialog_status = "input"
                self.user_database.update_user()
                return
            if element.type == ElementType.TEXT:
                keyboard=json.loads(user.keyboard)
                if keyboard is None:
                    keyboard = bm.NEW_USER_MENU
                viber.send_messages(
                    user_viber_id,
                    TextMessage(
                        text=element.data,
                        keyboard=keyboard,
                        min_api_version=7,
                    ),
                )
            if element.type == ElementType.PICTURE:
                viber.send_messages(
                    user_viber_id,
                    PictureMessage(
                        media=url_for(
                            "static",
                            filename=f"pictures/{element.data}",
                            _external=True,
                        ),
                        keyboard=json.loads(user.keyboard),
                        min_api_version=7,
                    ),
                )
            if element.type == ElementType.TRIGGER:
                # it does nothing but indicates the start from the middle of a branch
                pass
            if element.type == ElementType.URL:
                viber.send_messages(
                    user_viber_id,
                    RichMediaMessage(
                        rich_media=bm.urls(element.data),
                        keyboard=json.loads(user.keyboard),
                        min_api_version=7,
                    ),
                )
            if element.type == ElementType.BUTTON:
                messages = [RichMediaMessage(
                                rich_media=bm.buttons(data_set),
                                keyboard=json.loads(user.keyboard),
                                min_api_version=7,) 
                            for data_set in bm.chunks(element.data, 5)]
                
                viber.send_messages(
                    user_viber_id,
                    messages,
                )
            if element.type == ElementType.TIMER:
                # time.sleep(element.data)
                # TODO: make it async. Problems because it makes handler work weird with flask threads?
                pass
            if element.type == ElementType.KEYBOARD:
                # # removed buttons in chat - only buttons in keyboard
                # user.keyboard = json.dumps(element.data)
                # self.user_database.update_user()
                user.keyboard = json.dumps(element.data)
                self.user_database.update_user()
                message = KeyboardMessage(keyboard=element.data, min_api_version=7)
                viber.send_messages(user_viber_id, message)
                
            if element.type == "action" and element.data == "gs_write_user":
                gsw = google_sheets_writer()
                gsw.save_user_to_gsheets(user)

            user.step_index += 1
            if user.step_index >= self.element_tree.get_length():
                return

    def process_request(self, request):
        self.logger.debug(f"recieved request. post data: {request.get_data()}")

        # checking the signature of the request
        if not viber.verify_signature(
            request.get_data(), request.headers.get("X-Viber-Content-Signature")
        ):
            return Response(status=403)

        viber_request = viber.parse_request(request.get_data())

        # Processing bot subscription request, to start conversation with a bot
        if isinstance(viber_request, ViberConversationStartedRequest):
            user = self.user_database.get_user(viber_request.user.id)
            user.joined_date = datetime.datetime.now()
            self.user_database.update_user()

            viber.send_messages(
                viber_request.user.id,
                [RichMediaMessage(rich_media=bm.START_MESSAGE, min_api_version=7)],
            )

        # Processing requests during a conversation with a bot
        if isinstance(viber_request, ViberMessageRequest):
            self.handle(request=viber_request)

        # In case request failed
        if isinstance(viber_request, ViberFailedRequest):
            self.logger.warn(
                f"Client failed receiving message. failure: {viber_request}"
            )
