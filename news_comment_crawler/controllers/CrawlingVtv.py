
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from bson import ObjectId
from datetime import datetime
from models.NewsComment import NewsComment
from models.NewsComment import SubComment

from controllers.CrawlingNews import CrawlingNews

class CrawlingVtv(CrawlingNews):

    def crawlingComment(self, url, element, news_obj):
        print("=============VTV=========")
        # get info selector in file config json
        ##-------------------------------------------------
        listCommentClassName = element["listCommentClassName"]
        #commentItemClassName = element["commentItemClassName"]
        #commentItemTagName = element["commentItemTagName"]
        #reactionClassName = element["reactionClassName"]
        #viewMoreCssSelector = element["viewMoreCssSelector"]
        #replyCommentClassName = element["replyCommentClassName"]
        #subCommentCssSelector = element["subCommentCssSelector"]
        #subCommentItemClassName = element["subCommentItemClassName"]
        #emptyCommentClassName = element["emptyCommentClassName"]
        ##-------------------------------------------------

        self.driver.get(url)
        self.driver.implicitly_wait(5) # seconds
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        try:
            list_comment_element = self.driver.find_element(By.CLASS_NAME, listCommentClassName)
        except :
            print("This article has no comment")
            return
        if list_comment_element.text == '':
            print("This article has no comment")
            return
        else:
            '''Xử lý lấy comment'''
        time.sleep(3)

 





