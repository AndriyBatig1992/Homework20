from mongoengine import Document, StringField, BooleanField,ObjectIdField
from mongoengine import connect

connect(host="mongodb+srv://userweb:1234@myprojectdbcluster.t5vswpc.mongodb.net/asha2", ssl=True)


class Contact(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    send = BooleanField()
    phone_number = StringField()
    preferred_notifications = StringField(default="email")

