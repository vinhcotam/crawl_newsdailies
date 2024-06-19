from selenium import webdriver
from mongoengine import connect
from models.NewsUrl import NewsUrl
from configs.FileJsonConfig import FileJsonConfig
from controllers.CommentFactory import CommentFactory

# Connect to the database
connect(db='tobaco-crawler-webadmin-dev', host='localhost', port=27017)

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
# url_to_crawl = "https://tuoitre.vn/canh-bao-vape-dang-len-vao-truong-gia-dang-son-moi-but-usb-20210108222708055.htm"

# Specify the URL you want to crawl
list_urrl = ["https://vnexpress.net/tai-sao-chi-8-nguoi-nghien-bo-thuoc-la-thanh-cong-3837618.html"
    
]
for url_to_crawl in list_urrl:
# Create a dummy document with the URL to crawl
    dummy_document = {
        "news_url": url_to_crawl,
        "_id": "dummy_id"
    }

    # Check domain URL with key file json
    for key, value in listNews.items():
        if isinstance(value, dict):
            if key == getDomain(url_to_crawl):
                factory = CommentFactory()
                article = factory.createCrawlingComment(key, driver)
                article.crawlingComment(url_to_crawl, value, dummy_document)

    # Close the WebDriver
driver.quit()