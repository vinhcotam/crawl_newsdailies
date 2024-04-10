from array import array
from mongoengine import *
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient


class SubComment(Document):
    _id = ObjectIdField()
    comment_id = StringField()
    content = StringField()
    reaction = DictField()
    meta = {'collection': 'news_sub_comment'}
    @classmethod
    def post_save(cls, sender, document, **kwargs):
        print(document._id)
    @staticmethod
    def checkSubCommentExist(comment_id, content):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['tobaco-crawler-webadmin-dev']
        comments_collection = db['news_sub_comment']
        existing_comment = comments_collection.find_one({"comment_id": comment_id, "content": content})
        if existing_comment:
            return True
        else:
            return False

class NewsComment(Document):
    _id = ObjectIdField()
    content = StringField()
    reaction = DictField()
    news_url = StringField()
    news_id = ObjectIdField()
    date_collected = DateTimeField()

    meta = {'collection': 'comments'}

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        print(document._id)

    @staticmethod
    def checkCommentExist(content):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['tobaco-crawler-webadmin-dev']
        comments_collection = db['comments']
        existing_comment = comments_collection.find_one({"content": content})
        if existing_comment:
            return True
        else:
            return False
