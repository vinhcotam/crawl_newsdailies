
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
        listCommentClassName = element["listCommentClassName"]
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
        # 
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            showMoreComment = self.driver.find_element(By.CLASS_NAME, "view-more.xtbl.ViewMoreComment")
            showMoreComment.click()
            self.driver.implicitly_wait(10)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            list_comment_element = self.driver.find_element(By.CLASS_NAME, "list-comment.content_cm")

        except :
            print("This article has no comment")
            return
        
        comments = list_comment_element.find_elements(By.CLASS_NAME, "item.box_cm")
        # print("zo", comments)

        # for i, comment in enumerate(comments):
        #     print(comment.get_attribute("innerHTML"))
        # commentsDate = list_comment_element.find_elements(By.CLASS_NAME, "time.timeago")
        # # print(commentsDate.get_attribute("innerHTML"))
        # for i, commentDate in enumerate(commentsDate):
        #             print(f"Date {i+1}: {commentDate.text}")
        for comment in comments:
            reaction_dict = {}
            # print(comment)
            # commentDateValue = commentDate.get_attribute("title")
            # print(comment.get_attribute("innerHTML"))
            commentText = comment.find_element(By.CLASS_NAME, 'text-comment.des.ReadMoreText.ct')
            commentDate = comment.find_element(By.CSS_SELECTOR, 'div.item-bottom > span.time.time-ago')
            commentText = commentText.get_attribute("innerHTML")
            commentDate = commentDate.get_attribute("title")
            date_comment = datetime.strptime(commentDate, "%Y-%m-%d %H:%M:%S")

            reaction = comment.find_element(By.CSS_SELECTOR, 'div.item-bottom > a.item-ls> span.total-like')
            print(reaction.get_attribute("innerHTML"))
            reaction = reaction.get_attribute("innerHTML")
            reaction_dict["Thích"] = reaction
            if not NewsComment.checkCommentExist(commentText):
                commentData = NewsComment(_id = ObjectId(), content = commentText, reaction = reaction_dict, news_url = url, news_id = news_obj, date_collected = datetime.now() , date_comment = date_comment)
                commentData.save()
                object_cmt_id = str(commentData._id)
            # print(commentData.to_json())
        time.sleep(5)

 





