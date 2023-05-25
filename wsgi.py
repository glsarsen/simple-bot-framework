from flask import request, Response

from simplebot.viber_config import viber
from simplebot import init_app
from simplebot.dialogue import rhandler
from config import SERVER, HOST, PORT, DEVELOPMENT, SSL_CONTEXT

app = init_app()


@app.route("/", methods=["POST"])
def incoming():
    rhandler.process_request(request)

    return Response(status=200)

