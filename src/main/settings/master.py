import os
from mongoengine import connect
connect('myuserdb', host=os.environ['MONGO_IP'], port=int(os.environ['MONGO_PORT']))
