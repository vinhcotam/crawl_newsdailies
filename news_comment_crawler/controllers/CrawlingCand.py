
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from bson import ObjectId
from datetime import datetime
from models.NewsComment import NewsComment
from models.NewsComment import SubComment
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from controllers.CrawlingNews import CrawlingNews
from selenium.webdriver.common.action_chains import ActionChains

class CrawlingCand(CrawlingNews):

    def crawlingComment(self, url, element, news_obj):
        print("=============CAND=========")
        # get info selector in file config json
        ##-------------------------------------------------
        listCommentCssSelector = element["listCommentCssSelector"]
        listCommentClassName = element["listCommentClassName"]
        commentItemTagName = element["commentItemTagName"]
        reactionClassName = element["reactionClassName"]
        viewMoreCssSelector = element["viewMoreCssSelector"]
        replyCommentClassName = element["replyCommentClassName"]
        subCommentCssSelector = element["subCommentCssSelector"]
        subCommentItemClassName = element["subCommentItemClassName"]
        ##-------------------------------------------------
        try:
            self.driver.get(url)
        # self.driver.implicitly_wait(10 ) # seconds
            wait = WebDriverWait(self.driver, 5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            list_comment_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "box-cmt")))
        except: 
            return
        try:
            list_comment_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "box-cmt")))
            # self.driver.execute_script("arguments[0].scrollIntoView();", list_comment_element)
            
            test = list_comment_element.find_element(By.CLASS_NAME, "box-content")
            html_content = test.get_attribute("innerHTML")
            print(list_comment_element.get_attribute("innerHTML"))
            print("----")
            print(html_content)
        except Exception as e:
            print(f"An error occurred: {e}")
        except :
            print("This article has no comment")
            return

        if list_comment_element.is_displayed == False:
            print("This article has no comment1")
            return
        else:
            liTags = list_comment_element.find_elements(By.TAG_NAME, commentItemTagName)
            for liTag in liTags:
                reaction_dict = {}
                commentText = liTag.find_element(By.TAG_NAME, 'p').text
                reaction = liTag.find_element(By.CLASS_NAME, reactionClassName).get_attribute('data-like')
                print(commentText + '---' + reaction)
                # save to database
                commentData = NewsComment(_id = ObjectId(), content = commentText, reaction = reaction_dict, news_url = url, news_id = news_obj, date_collected = datetime.now())

                commentData.save()
                # print(commentData.to_json())






