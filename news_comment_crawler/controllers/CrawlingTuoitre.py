from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from bson import ObjectId
from datetime import datetime
from models.NewsComment import NewsComment
from models.NewsComment import SubComment
from selenium.common.exceptions import NoSuchElementException
from controllers.CrawlingNews import CrawlingNews
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
class CrawlingTuoiTre(CrawlingNews):

    def crawlingComment(self, url, element, news_obj):
        print("=============TUOI TRE=========")
        # get info selector in file config json
        ##-------------------------------------------------
        listCommentCssSelector = element["listCommentCssSelector"]
        commentItemClassName = element["commentItemClassName"]
        # reactionCssSelector = element["reactionCssSelector"]
        viewMoreCssSelector = element["viewMoreCssSelector"]
        # replyCommentClassName = element["replyCommentClassName"]
        # subCommentCssSelector = element["subCommentCssSelector"]
        subCommentItemClassName = element["subCommentItemClassName"]
        viewReplyCssSelector = element["viewReplyCssSelector"]
        # reactionEmotionCssSelector = element["reactionEmotionCssSelector"]
        ##-------------------------------------------------

        self.driver.get(url)
        self.driver.implicitly_wait(10) # seconds
        try:
            
            comment_element = self.driver.find_element(By.CLASS_NAME, "ico.comment")
            comment_element.click()

            self.driver.implicitly_wait(5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            list_comment_element = self.driver.find_element(By.CSS_SELECTOR, "div.lstcommentpopup > ul")
        
        # # check empty
        # try:
        #     list_comment_element = self.driver.find_element(By.CSS_SELECTOR, "div.lstcommentpopup > ul")
            
        except :
            print("This article has no comment")
            return

        i = 0

        comments = list_comment_element.find_elements(By.CSS_SELECTOR, ".item-comment") #list <web-element>

        for comment in comments:
            i = i + 1
            commentText = comment.find_element(By.CLASS_NAME, "contentcomment").text.strip()
            try:
                remainElement = comment.find_element(By.CLASS_NAME, "remain")
                textContent = remainElement.get_attribute("innerHTML").strip()
                commentText += textContent 
                print("z-z")
            except NoSuchElementException:
                pass
            
            if(commentText!=""):
                print(commentText.strip())
                print(process_emotions(comment))
                reaction_dict = process_emotions(comment)
                if not NewsComment.checkCommentExist(commentText):
                    print("Aaaaaa", news_obj)
                    commentData = NewsComment(_id = ObjectId(), content=commentText, reaction=reaction_dict, news_url=url, news_id = news_obj, date_collected=datetime.now())
                    commentData.save()
                    print("done")
                    object_cmt_id = str(commentData._id)
                try:
                    showSubComment = comment.find_element(By.CSS_SELECTOR, viewReplyCssSelector)
                    showSubComment.click()
                    print("yeah")
                    self.driver.implicitly_wait(3)
                except:
                    pass
        time.sleep(5)

def process_emotions(comment):
    emotion_dict = {
        "spritecmt icolikereact": "Thích",
        "spritecmt icoheartreact": "Yêu thích",
        "spritecmt icolaughreact": "Haha",
        "spritecmt icosurprisedreact": "Ngạc nhiên",
        "spritecmt icosadreact": "Buồn",
        "spritecmt icoanggyreact": "Phẫn nộ"
        }
    reaction_dict = {}
    emotion_text = comment.find_elements(By.CLASS_NAME, "colreact")
    for emotion_element in emotion_text:
        num_emotions = [num.get_attribute("innerHTML") for num in emotion_element.find_elements(By.CSS_SELECTOR, "span.num")]
        emotion_types = [emotion.get_attribute("class") for emotion in emotion_element.find_elements(By.CSS_SELECTOR, "span.spritecmt")]
        for num, emotion_class in zip(num_emotions, emotion_types):
            reaction_dict[emotion_dict.get(emotion_class, emotion_class)] = num

    return reaction_dict