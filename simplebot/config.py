from os import environ, path, urandom
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

SECRET_KEY = urandom(32)

SSL_CERT_PATH = environ.get("SSL_CERT_PATH")
SSL_KEY_PATH = environ.get("SSL_KEY_PATH")

DEVELOPMENT = True

if DEVELOPMENT:
    SERVER = "https://a4c8-92-253-236-22.eu.ngrok.io"
    SSL_CONTEXT = None
    TOKEN = environ.get("VIBER_TOKEN_TEST")
    PORT = 30000

else:
    SERVER = "https://testsix.rh-s.com"
    SSL_CONTEXT = None
    TOKEN = environ.get("VIBER_TOKEN_2")
    PORT = 30000


HOST = None
