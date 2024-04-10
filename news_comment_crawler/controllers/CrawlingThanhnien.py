
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from bson import ObjectId
from datetime import datetime
from models.NewsComment import NewsComment
from models.NewsComment import SubComment

from controllers.CrawlingNews import CrawlingNews

class CrawlingThanhnien(CrawlingNews):

    def crawlingComment(self, url, element, news_obj):
        print("=============Thanhnien=========")
        # get info selector in file config json
        ##-------------------------------------------------
        listCommentCssSelector = element["listCommentCssSelector"]
        commentItemClassName = element["commentItemClassName"]
        # commentItemTagName = element["commentItemTagName"]
        reactionClassName = element["reactionClassName"]
        viewMoreCssSelector = element["viewMoreCssSelector"]
        replyCommentClassName = element["replyCommentClassName"]
        subCommentCssSelector = element["subCommentCssSelector"]
        subCommentItemClassName = element["subCommentItemClassName"]
        # emptyCommentClassName = element["emptyCommentClassName"]
        ##-------------------------------------------------

        self.driver.get(url)
        self.driver.implicitly_wait(5) # seconds
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        try:
            list_comment_element = self.driver.find_element(By.CSS_SELECTOR, listCommentCssSelector)
        except :
            print("This article has no comment")
            return
        if list_comment_element.is_displayed() == False:
            print("This article has no comment")
            return
        comments = list_comment_element.find_elements(By.CLASS_NAME, commentItemClassName)
        showMoreComment = self.driver.find_element(By.CSS_SELECTOR, viewMoreCssSelector)
        while showMoreComment.is_displayed():
            showMoreComment.click()
            self.driver.implicitly_wait(5)
        for comment in comments:
            reaction_dict = {}
            commentText = comment.find_element(By.CLASS_NAME, 'text-comment').text
            reaction = comment.find_element(By.CLASS_NAME, 'total-like').text
            print(commentText + '---' + reaction)
            reaction_dict["Thích"] = reaction
            if not NewsComment.checkCommentExist(commentText):
                commentData = NewsComment(_id = ObjectId(), content = commentText, reaction = reaction_dict, news_url = url, news_id = news_obj, date_collected = datetime.now())
                commentData.save()
                object_cmt_id = str(commentData._id)
            # print(commentData.to_json())
        time.sleep(5)

 





