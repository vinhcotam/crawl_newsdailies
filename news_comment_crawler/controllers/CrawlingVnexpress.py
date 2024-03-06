
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from bson import ObjectId
from datetime import datetime
from models.NewsComment import NewsComment
from models.NewsComment import SubComment

from controllers.CrawlingNews import CrawlingNews

class CrawlingVnexpress(CrawlingNews):

    def checkStyleNone(self, selector):
        element = self.driver.find_element(By.ID, selector)
        style = element.get_attribute("style")
        if "none" in style:
            return True
        return False

    def crawlingComment(self, url, element):
        print("=============VNEXPRESS=========")

        # get info selector in file config json
        ##-------------------------------------------------
        listCommentCssSelector = element["listCommentCssSelector"]
        commentItemClassName = element["commentItemClassName"]
        reactionCssSelector = element["reactionCssSelector"]
        viewMoreCssSelector = element["viewMoreCssSelector"]
        replyCommentClassName = element["replyCommentClassName"]
        subCommentCssSelector = element["subCommentCssSelector"]
        subCommentItemClassName = element["subCommentItemClassName"]
        ##-------------------------------------------------

        self.driver.get(url)
        self.driver.implicitly_wait(5) # seconds
        # check isset comment in artical
        try:
            #list_comment_element = self.driver.find_element(By.CLASS_NAME, listCommentClassName)
            list_comment_element = self.driver.find_element(By.CSS_SELECTOR, listCommentCssSelector)
            if list_comment_element.is_displayed() == False:
                print("This article has no comment!")
                return
            showMoreComment = self.driver.find_element(By.CSS_SELECTOR, viewMoreCssSelector)
            # check show more comment btn
            while showMoreComment.is_displayed():
                showMoreComment.click()
                self.driver.implicitly_wait(5) # second
        except:
            pass

        comments = list_comment_element.find_elements(By.CLASS_NAME, commentItemClassName)
        print(len(comments))
        #loop in comments get content (text, react) of each comment
        i = 0
        for comment in comments:
            i = i + 1
            reaction = comment.find_element(By.CSS_SELECTOR, reactionCssSelector).text

                #save to database
            print(str(i) + self.getContent(comment) + reaction)

            commentData = NewsComment(_id = ObjectId(), content = self.getContent(comment), reaction = reaction, news_url = url, date_collected = datetime.now())
            try:

                showSubComment = comment.find_element(By.CLASS_NAME, replyCommentClassName)
                showSubComment.click()
                self.driver.implicitly_wait(3) # seconds

                subCommentElement = comment.find_element(By.CSS_SELECTOR, subCommentCssSelector)
                subComments = subCommentElement.find_elements(By.CLASS_NAME, subCommentItemClassName)
                #loop in comments get content (text, react) of each subcomment
                for subComment in subComments:
                    subReaction = subComment.find_element(By.CSS_SELECTOR, reactionCssSelector).text
                    #save to database
                    print('---' + self.getContent(subComment) + subReaction)
                    commentData.subcomments.append(SubComment(id=ObjectId(), content=self.getContent(subComment), reaction=subReaction))

            except:
                pass
            commentData.save()
            print(commentData.to_json())
        time.sleep(3)

    def getContent(self, elements):
        tags = elements.find_elements(By.CLASS_NAME, "full_content") if elements.find_elements(By.CLASS_NAME, "full_content") else elements.find_elements(By.CLASS_NAME, "content_more")
        # lấy ra nội dung của comment
        for j in tags:
            pHtml = j.get_attribute("innerHTML")
            # loại bỏ nội dung thẻ span 
            soup = BeautifulSoup(pHtml, "html.parser")
            for span in soup.find_all("span"):
                span.decompose()
            p_text_without_span = soup.get_text()
        return p_text_without_span
