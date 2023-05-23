from os import environ, path, urandom
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

SECRET_KEY = urandom(32)

SSL_CERT_PATH = environ.get("SSL_CERT_PATH")
SSL_KEY_PATH = environ.get("SSL_KEY_PATH")

DEVELOPMENT = False

if DEVELOPMENT:
    SERVER = "https://1b94-92-253-212-37.ngrok-free.app"
    SSL_CONTEXT = None
    TOKEN = environ.get("VIBER_TOKEN_3")
    PORT = 30000

else:
    SERVER = "https://chatbot.rhelpers.com"
    SSL_CONTEXT = None
    TOKEN = environ.get("VIBER_TOKEN_3")
    PORT = 30000


HOST = None
