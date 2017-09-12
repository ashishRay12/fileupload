from mongoengine import Document, StringField, ListField, DateTimeField


class User(Document):
    user_id = StringField(max_length=50, required=True)
    password = StringField(required=True)
    salt = StringField(required=True)


class AuthInfo(Document):
    user_id = StringField(max_length=50, required=True)
    token = StringField(required=True)


class UserFiles(Document):
    user_id = StringField(max_length=50, required=True)
    file_names = StringField(max_length=50, required=True)
    upload_time = DateTimeField()
