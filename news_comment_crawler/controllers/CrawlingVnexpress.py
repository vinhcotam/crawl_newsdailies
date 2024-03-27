
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
        reactionDetail = element["reactionDetail"]
        ##-------------------------------------------------

        self.driver.get(url)
        self.driver.implicitly_wait(5) # seconds
        # check isset comment in artical
        try:
            list_comment_element = self.driver.find_element(By.CSS_SELECTOR, listCommentCssSelector)
            if not list_comment_element.is_displayed():
                print("This article has no comment!")
                return
        except NoSuchElementException:
            print("This article has no comment!")
            return
        try:
            showMoreComment = self.driver.find_element(By.CSS_SELECTOR, viewMoreCssSelector)
            while showMoreComment.is_displayed():
                showMoreComment.click()
                self.driver.implicitly_wait(5) 
        except NoSuchElementException:
            pass
        comments = list_comment_element.find_elements(By.CLASS_NAME, commentItemClassName)
        # print(len(comments))
        #loop in comments get content (text, react) of each comment
        i = 0
        for comment in comments:
            i = i + 1
            reaction_dict = {}
            reaction = comment.find_element(By.CSS_SELECTOR, reactionCssSelector).text
            reactionDetail = ".reactions-detail"
            reaction_items = comment.find_elements(By.CSS_SELECTOR, reactionDetail)

            for reaction_detail in reaction_items:
                img_elements = reaction_detail.find_elements(By.TAG_NAME, "img")
                strong_elements = reaction_detail.find_elements(By.TAG_NAME, "strong")
                for img, strong in zip(img_elements, strong_elements):
                    emotions = img.get_attribute("alt")
                    quantity = strong.get_attribute("innerHTML")
                    reaction_dict[emotions] = quantity
                # save to database
            # print(str(i) + self.getContent(comment) + reaction)
            if not NewsComment.checkCommentExist(self.getContent(comment)):
                commentData = NewsComment(_id = ObjectId(), content=self.getContent(comment), reaction=reaction_dict, news_url=url, date_collected=datetime.now())
                commentData.save()
                object_cmt_id = str(commentData._id)
            # else:
            #     print("not save")
            # get object id
            try:
                sub_reaction_dict = {}
                showSubComment = comment.find_element(By.CLASS_NAME, replyCommentClassName)
                showSubComment.click()
                self.driver.implicitly_wait(3) # seconds
                # print("test1: ", comment.get_attribute("innerHTML"))
                subCommentElement = comment.find_element(By.CSS_SELECTOR, subCommentCssSelector)
                subComments = subCommentElement.find_elements(By.CLASS_NAME, subCommentItemClassName)
                # loop in comments get content (text, react) of each subcomment
                # print("--------")
                for subComment in subComments:
                    # text = subComment.get_attribute("innerHTML")
                    # print("text: ", text)
                    subReaction = subComment.find_element(By.CSS_SELECTOR, reactionCssSelector).text
                    img_elements = reaction_detail.find_elements(By.TAG_NAME, "img")
                    strong_elements = reaction_detail.find_elements(By.TAG_NAME, "strong")
                    for img, strong in zip(img_elements, strong_elements):
                        sub_emotions = img.get_attribute("alt")
                        sub_quantity = strong.get_attribute("innerHTML")
                        # print("----", sub_emotions)
                        # print("----", sub_quantity)
                        sub_reaction_dict[sub_emotions] = sub_quantity
                        # print(object_cmt_id)
                        if object_cmt_id is not None:
                            if not SubComment.checkSubCommentExist(object_cmt_id, self.getContent(comment)):
                                subCommentData = SubComment(_id = ObjectId(),comment_id=object_cmt_id, content=self.getContent(subComment), reaction=sub_reaction_dict)
                                subCommentData.save()
                                print("check check")
                                print(self.getContent(subComment))
                        # else:
                        #     print("not save")

                        # reaction_dict[emotions] = quantity
                    # save to database
                    # print('---' + self.getContent(subComment) + subReaction)

            except:
                pass
            # print(commentData.to_json())
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
