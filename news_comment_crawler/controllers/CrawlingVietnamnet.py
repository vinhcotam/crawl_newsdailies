
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from bson import ObjectId
from datetime import datetime
from models.NewsComment import NewsComment
from models.NewsComment import SubComment

from controllers.CrawlingNews import CrawlingNews

class CrawlingVietnamnet(CrawlingNews):

    def crawlingComment(self, url, element, news_obj):
        print("=============Vietnamnet=========")
        # get info selector in file config json
        ##-------------------------------------------------
        iframeCssSelector = element["iframeCssSelector"]
        listCommentCssSelector = element["listCommentCssSelector"]
        commentItemClassName = element["commentItemClassName"]
        reactionCssSelector = element["reactionCssSelector"]
        subCommentTagName = element["subCommentTagName"]
        subCommentReaction = element["subCommentReaction"]
        viewMoreCssSelector = element["viewMoreCssSelector"]
        viewReplyCssSelector = element["viewReplyCssSelector"]
        ##-------------------------------------------------

        self.driver.get(url)
        self.driver.implicitly_wait(5) # seconds

        '''Chuyển đổi sang iframe comments'''       
        iframeConvert = self.driver.find_element(By.CSS_SELECTOR, iframeCssSelector)
        self.driver.switch_to.frame(iframeConvert)
        '''Click btn view more comment'''
        try:
            print("zoooooo")
            view_more_button = self.driver.find_element(By.CSS_SELECTOR, viewMoreCssSelector)
            view_more_button.click()
            time.sleep(3)
        except:
            pass
    
        try:
            list_comment_element = self.driver.find_element(By.CSS_SELECTOR, listCommentCssSelector)

        except :
            print("This article has no comment")
            return
        """Lấy nội dung comment và lưu vào database"""
        if list_comment_element.is_displayed == False:
            print("This article has no comment")
            return   
        comments = list_comment_element.find_elements(By.CSS_SELECTOR, commentItemClassName)
        
        for comment in comments:
            '''Lấy comments'''
            print(comment.get_attribute("innerHTML"))
            commentText = comment.find_element(By.CLASS_NAME, "LinesEllipsis").text
            reaction_dict = {}
            '''Lấy reaction của comment'''
            try:
                
                reaction = comment.find_element(By.CSS_SELECTOR, reactionCssSelector).text
                reaction_dict['Vui'] = reaction
            except:
                reaction = "0"
        
            print("--" + commentText + reaction)
            if not NewsComment.checkCommentExist(commentText):
                commentData = NewsComment(_id = ObjectId(), content = commentText, reaction = reaction_dict, news_url = url, news_id = news_obj, date_collected = datetime.now())
                '''Hiển thị comments phụ'''
                commentData.save()
                object_cmt_id = str(commentData._id)
            try:
                print("--------")
                viewReply = self.driver.find_element(By.CSS_SELECTOR, viewReplyCssSelector)
                print(viewReply)
                print("zoooooo1")
                viewReply.click()
                self.driver.implicitly_wait(10)
                subCommentElement = comment.find_element(By.CSS_SELECTOR, subCommentTagName)
                subComments = subCommentElement.find_elements(By.CLASS_NAME, subCommentReaction)
                print("-------")
                print(subCommentElement)
                print(subComments)
                for subComment in subComments:
                    print("text")
                    print(subComment.get_attribute("innerHTML"))
                    print("reaction")
                    # save to database
            except:
                pass
            # subComments = comment.find_elements(By.TAG_NAME, subCommentTagName)
            # for subComment in subComments:
            #     subCommentText = subComment.find_element(By.TAG_NAME, "p").text
            #     '''Lấy reaction của comment'''
            #     try:
            #         subReact= subComment.find_element(By.CSS_SELECTOR, reactionCssSelector).text
            #     except:
            #         subReact = "0"
            #     print("subcomment: " + subCommentText + subReact)
            #     commentData.subcomments.append(SubComment(id=ObjectId(), content=subCommentText, reaction=subReact))
            # print(commentData.to_json())
        time.sleep(3)







