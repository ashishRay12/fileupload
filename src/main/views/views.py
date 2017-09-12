import falcon
import hashlib
import json
from uuid import uuid4
from mongoengine import DoesNotExist
from datetime import datetime
from ..models import AuthInfo, User, UserFiles


class Register(object):

    def on_post(self, req, resp, form={}):

        try:
            User.objects.get(user_id=form["user_id"])
            resp.status = falcon.HTTP_200
            resp.content_type = 'application/json'
            resp.body = json.dumps({"messege": "try another username"})
        except DoesNotExist:
            salt = uuid4().get_hex()
            hashed_password = hashlib.sha512(form["password"] + salt).hexdigest()
            user_data = User(user_id=form["user_id"], password=hashed_password, salt=salt)
            user_data.save()
            resp.status = falcon.HTTP_200
            resp.content_type = 'application/json'
            resp.body = json.dumps({"messege": "Registered successfully"})


class Authenticate(object):

    # uuid for creatind unique token for authentication
    # AuthInfo collection for logedin user or active user
    # user_info --> User_data

    def on_post(self, req, resp, form={}):
        try:
            user_info = User.objects.get(user_id=form["user_id"])
            salt = user_info["salt"]
            hash_pass = hashlib.sha512(form["password"] + salt).hexdigest()
            if hash_pass == user_info["password"]:
                token = uuid4().get_hex()
                AuthInfo.objects(user_id=form["user_id"]).update_one(set__user_id=form["user_id"],
                                                                      set__token=token, upsert=True)
                message = {"token": token}
                resp.status = falcon.HTTP_200
                resp.content_type = 'application/json'
                resp.body = json.dumps(message)
            else:
                raise Exception("invalid password")
        except Exception:
            message = {"message": "password not matched"}
            resp.status = falcon.HTTP_401
            resp.content_type = 'application/json'
            resp.body = json.dumps(message)


class UploadFiles(object):

    def on_post(self, req, resp, form={}):

        file_data = UserFiles(user_id=form["user_id"], file_names=form["file_name"], upload_time=datetime.now())
        file_data.save()
        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        resp.body = json.dumps({"message": "file saved"})


class QueryFiles(object):

    def on_get(self, req, resp, form={}):
        files_list = UserFiles.objects(user_id=form["user_id"]).only("file_names", "upload_time")
        new_list = [{"file_name": obj.file_names, "date": str(obj.upload_time)} for obj in files_list]

        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        resp.body = json.dumps({"files": new_list})
