
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from bson import ObjectId
from datetime import datetime
from models.NewsComment import NewsComment
from models.NewsComment import SubComment

from controllers.CrawlingNews import CrawlingNews

class CrawlingDantri(CrawlingNews):

    def crawlingComment(self, url, element):
        print("=============DAN TRI=========")
        # get info selector in file config json
        ##-------------------------------------------------
        listCommentCssSelector = element["listCommentCssSelector"]
        commentItemClassName = element["commentItemClassName"]
        reactionCssSelector = element["reactionCssSelector"]
        viewMoreCssSelector = element["viewMoreCssSelector"]
        replyCommentClassName = element["replyCommentClassName"]
        subCommentCssSelector = element["subCommentCssSelector"]
        subCommentItemClassName = element["subCommentItemClassName"]
        emptyCommentClassName = element["emptyCommentClassName"]
        ##-------------------------------------------------

        self.driver.get(url)
        self.driver.implicitly_wait(5) # seconds

        list_comment_element = self.driver.find_element(By.CSS_SELECTOR, listCommentCssSelector)
        #check empty
        try:
            list_comment_element = self.driver.find_element(By.CSS_SELECTOR, listCommentCssSelector)

        except :
            print("This article has no comment")
            return

        if list_comment_element.is_displayed == False:
            print("This article has no comment!")
            return
        
        else:
            i = 0
            comments = list_comment_element.find_elements(By.CLASS_NAME, commentItemClassName) #list <web-element>
            #lặp qua từng comments thực hiện các việc sau: 
            # lấy ra các comment chính - và comment phụ
            for comment in comments:
                i = i + 1
                commentText = comment.find_element(By.CLASS_NAME, "comment-text").text
                reaction = comment.find_element(By.CSS_SELECTOR, reactionCssSelector).text
                
                # save to database
                commentData = NewsComment(_id = ObjectId(), content = commentText, reaction = reaction, news_url = url, date_collected = datetime.now())
                #sub comment
                try:
                   showSubComment = comment.find_element(By.CLASS_NAME, 'view_all_reply')
                   showSubComment.click()
                   time.sleep(3)

                   subCommentElement = comment.find_element(By.CSS_SELECTOR, 'div.sub_comment')
                   subComments = subCommentElement.find_elements(By.CLASS_NAME, 'sub_comment_item')
                   print(subComments)
                #    for subComment in subComments:
                #        #luu vao database
                #        commentData.subcomments.append(sub_comment(id=ObjectId(), content=self.getContent(subComment), reaction=self.getReaction(subComment)))
                    
                except:
                   pass
                commentData.save()
                print(commentData.to_json())

            time.sleep(3)

