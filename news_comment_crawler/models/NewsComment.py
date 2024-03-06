from array import array
from mongoengine import *
from datetime import datetime
from bson import ObjectId


class SubComment(EmbeddedDocument):
    _id = ObjectIdField()
    content = StringField()
    reaction = StringField()


class NewsComment(Document):
    _id = ObjectIdField()
    content = StringField()
    reaction = StringField()
    news_url = StringField() #
    subcomments = EmbeddedDocumentListField(SubComment)
    date_collected = DateTimeField()
    meta = {'collection': 'news_comment'}
    @classmethod
    def post_save(cls, sender, document, **kwargs):
        print(document._id)
