from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from bson import ObjectId
from datetime import datetime
from models.NewsComment import NewsComment
from models.NewsComment import SubComment
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from controllers.CrawlingNews import CrawlingNews
import re

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
        commentDateClassName = element["commentDateClassName"]

        self.driver.get(url)
        self.driver.implicitly_wait(10)  # seconds

        try:
            comment_element = self.driver.find_element(By.CLASS_NAME, "ico.comment")
            comment_element.click()
            self.driver.implicitly_wait(5)
        except NoSuchElementException:
            print("This article has no comment")
            return

        # Locate the popup element
        popup_element = self.driver.find_element(By.CSS_SELECTOR, "div.lstcommentpopup")

        # Scroll within the popup until no more new comments are loaded
        while True:
            previous_height = self.driver.execute_script("return arguments[0].scrollHeight", popup_element)
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", popup_element)
            time.sleep(2)  # Wait for new comments to load
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", popup_element)
            if new_height == previous_height:
                break

        list_comment_element = popup_element.find_element(By.CSS_SELECTOR, "ul")
        commentsDate = list_comment_element.find_elements(By.CSS_SELECTOR, ".timeago")
        comments = list_comment_element.find_elements(By.CSS_SELECTOR, ".item-comment")

        for commentDate, comment in zip(commentsDate, comments):
            commentText = comment.find_element(By.CLASS_NAME, "contentcomment").text.strip()
            commentDateValue = commentDate.get_attribute("title")
            commentDateValue = re.search(r"\d{4}-\d{2}-\d{2}", commentDateValue).group()

            try:
                remainElement = comment.find_element(By.CLASS_NAME, "remain")
                textContent = remainElement.get_attribute("innerHTML").strip()
                commentText += textContent
            except NoSuchElementException:
                pass

            if commentText:
                print(commentText.strip())
                reaction_dict = process_emotions(comment)
                print(reaction_dict)
                # Save the comment to the database if needed
                if not NewsComment.checkCommentExist(commentText):
                    commentData = NewsComment(
                        _id=ObjectId(),
                        content=commentText,
                        reaction=reaction_dict,
                        news_url=url,
                        news_id=news_obj,
                        date_collected=datetime.now(),
                        date_comment=commentDateValue
                    )
                    commentData.save()
                    print("Comment saved")
                    object_cmt_id = str(commentData._id)

                # try:
                #     showSubComment = comment.find_element(By.CSS_SELECTOR, viewReplyCssSelector)
                #     showSubComment.click()
                #     self.driver.implicitly_wait(3)
                # except NoSuchElementException:
                #     pass
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
