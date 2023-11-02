from mongoengine import connect, Document, StringField, ReferenceField, ListField

connect(host="mongodb+srv://userweb:1234@myprojectdbcluster.t5vswpc.mongodb.net/part1", ssl=True)

class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()