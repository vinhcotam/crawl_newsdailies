
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from bson import ObjectId
from datetime import datetime
from models.NewsComment import NewsComment
from models.NewsComment import SubComment

from controllers.CrawlingNews import CrawlingNews

class CrawlingCand(CrawlingNews):

    def crawlingComment(self, url, element):
        print("=============CAND=========")
        # get info selector in file config json
        ##-------------------------------------------------
        listCommentCssSelector = element["listCommentCssSelector"]
        commentItemTagName = element["commentItemTagName"]
        reactionClassName = element["reactionClassName"]
        viewMoreCssSelector = element["viewMoreCssSelector"]
        replyCommentClassName = element["replyCommentClassName"]
        subCommentCssSelector = element["subCommentCssSelector"]
        subCommentItemClassName = element["subCommentItemClassName"]
        ##-------------------------------------------------

        self.driver.get(url)
        self.driver.implicitly_wait(5) # seconds

        try:
            list_comment_element = self.driver.find_element(By.CSS_SELECTOR, listCommentCssSelector)

        except :
            print("This article has no comment")
            return

        if list_comment_element.is_displayed == False:
            print("This article has no comment")
            return
        else:
            liTags = list_comment_element.find_elements(By.TAG_NAME, commentItemTagName)
            for liTag in liTags:
                reaction_dict = {}
                commentText = liTag.find_element(By.TAG_NAME, 'p').text
                reaction = liTag.find_element(By.CLASS_NAME, reactionClassName).get_attribute('data-like')
                print(commentText + '---' + reaction)
                # save to database
                commentData = NewsComment(_id = ObjectId(), content = commentText, reaction = reaction_dict, news_url = url, date_collected = datetime.now())

                commentData.save()
                # print(commentData.to_json())






