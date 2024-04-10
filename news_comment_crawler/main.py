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
print("-----------------")
# Load the list of URLs from the database
newsUrl = NewsUrl()
urls = newsUrl.getUrl()
print(urls)
print(type(urls))
print("-----------------")
for document in urls:
    domain = getDomain(document["news_url"])  # Get the domain
    print(domain)
    # Check domain URL with key file json
    for key, value in listNews.items():
        if isinstance(value, dict):
            if key == domain:
                url = document["news_url"]
                news_obj = document["_id"]
                print(url)
                factory = CommentFactory()
                article = factory.createCrawlingComment(domain, driver)
                article.crawlingComment(url, value, news_obj)



