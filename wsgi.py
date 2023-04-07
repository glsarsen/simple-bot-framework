import threading
import sched
import time

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


if DEVELOPMENT and __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, viber.set_webhook, (SERVER,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    app.run(host=HOST, port=PORT, debug=DEVELOPMENT, ssl_context=SSL_CONTEXT)
