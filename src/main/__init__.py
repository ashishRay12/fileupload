import falcon
from helpers import AuthMiddleware
app = falcon.API(middleware=[AuthMiddleware()])


from .settings import *
from views import *
