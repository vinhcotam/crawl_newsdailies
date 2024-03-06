from selenium import webdriver
from mongoengine import connect
from models.NewsUrl import NewsUrl
from configs.FileJsonConfig import FileJsonConfig
from controllers.CommentFactory import CommentFactory

# Connect to the database
connect(db='news_comment_crawler', host='localhost', port=27017)

# Configure Firefox options
options = webdriver.FirefoxOptions()

# Create the Firefox WebDriver instance
driver = webdriver.Firefox(options=options)

# Load data from the file config json
fileJsonConfig = FileJsonConfig()
listNews = fileJsonConfig.load_config()

# Function to extract the domain from a URL
def getDomain(url):
    split_url = url.split('/')
    return split_url[2]
print("-----------------")
# Load the list of URLs from the database
newsUrl = NewsUrl()
urls = newsUrl.getUrl()
print(urls)
print(type(urls))
print("-----------------")
for document in urls:
    domain = getDomain(document["name_url"])  # Get the domain
    print(domain)
    # Check domain URL with key file json
    for key, value in listNews.items():
        if isinstance(value, dict):
            if key == domain:
                url = document["name_url"]
                print(url)
                factory = CommentFactory()
                article = factory.createCrawlingComment(domain, driver)
                article.crawlingComment(url, value)


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# driver = webdriver.Firefox()

# article_url = "https://vnexpress.net/ong-phan-van-mai-vanh-dai-4-tp-hcm-phai-dat-chuan-cao-toc-4714306.html"
# driver.get(article_url)

# wait = WebDriverWait(driver, 10)
# comments_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "main_show_comment")))

# comment_elements = comments_element.find_elements(By.CLASS_NAME, "full_content")

# # sub_comments_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sub_comment_item  ")))

# # sub_comment_elements = sub_comments_element.find_elements(By.CLASS_NAME, "full_content")



# for comment_element in comment_elements:
#     comment_text = comment_element.text
#     print(comment_text)
#     reply_comments = comment_element.find_elements(By.CLASS_NAME, "sub_comment_item")
#     for reply_comment in reply_comments:
#         reply_comment_text = reply_comment.find_element(By.CLASS_NAME, "full_content").text
#         print("Reply: " + reply_comment_text)

# driver.quit()
