import json

class FileJsonConfig:
    def __init__(self):
        self.filename = "news_comment_crawler\list_news.json"
        #self.load_config()

    def load_config(self):
        with open(self.filename, "r") as f:
            return json.load(f)