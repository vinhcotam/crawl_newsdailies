from abc import ABC, abstractclassmethod

# Define abstract class
class CrawlingNews(ABC):
    def __init__(self, domain, driver):
        self.driver = driver
        self.domain = domain
    @abstractclassmethod
    def crawlingComment(self, url, element):
        pass