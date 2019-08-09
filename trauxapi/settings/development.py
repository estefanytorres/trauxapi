from .base import *

ENV = 'DEV'
PRODUCTION = False
DEBUG = False
ALLOWED_HOSTS = ['trauxapi-dev.herokuapp.com']
CORS_ORIGIN_WHITELIST = [
    "https://trauxweb-dev.herokuapp.com",
    "https://trauxapp-dev.herokuapp.com",
]