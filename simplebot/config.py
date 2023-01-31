from os import environ, path, urandom
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

SECRET_KEY = urandom(32)

SSL_CERT_PATH = environ.get("SSL_CERT_PATH")
SSL_KEY_PATH = environ.get("SSL_KEY_PATH")

DEVELOPMENT = True

if DEVELOPMENT:
    SERVER = "https://53a4-92-253-212-126.eu.ngrok.io"
    SSL_CONTEXT = None
    TOKEN = environ.get("VIBER_TOKEN_2")

else:
    SERVER = "https://testsix.rh-s.com:1338"
    SSL_CONTEXT = (SSL_CERT_PATH, SSL_KEY_PATH)
    TOKEN = environ.get("VIBER_TOKEN")


HOST = "0.0.0.0"
PORT = 1338
