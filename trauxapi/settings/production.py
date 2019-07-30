from .base import *

ENV = 'PRD'
PRODUCTION = True
DEBUG = False
ALLOWED_HOSTS = ['trauxapi.herokuapp.com']
CORS_ORIGIN_WHITELIST = [
    "https://trauxweb.herokuapp.com",
    "https://www.trauxerp.com",
    "https://trauxerp.com",
]