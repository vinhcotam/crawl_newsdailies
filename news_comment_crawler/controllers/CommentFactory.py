from .CrawlingVnexpress import CrawlingVnexpress
from .CrawlingDantri import CrawlingDantri
from .CrawlingVietnamnet import CrawlingVietnamnet
from .CrawlingCand import CrawlingCand
from .CrawlingHanoimoi import CrawlingHanoimoi
from .CrawlingThanhnien import CrawlingThanhnien
from .CrawlingVtv import CrawlingVtv

class CommentFactory():

    '''Define news's domain'''
    def createCrawlingComment(self, domain, driver):

        if domain == "vnexpress.net":
            return CrawlingVnexpress(domain, driver)

        if domain == "dantri.com.vn":
            return CrawlingDantri(domain, driver)

        if domain == "thanhnien.vn":
            return CrawlingThanhnien(domain, driver)

        if domain == "cand.com.vn":
            return CrawlingCand(domain, driver)

        if domain == "hanoimoi.vn":
            return CrawlingHanoimoi(domain, driver)

        if domain == "vtv.vn":
            return CrawlingVtv(domain, driver)

        if domain == "vietnamnet.vn":
            return CrawlingVietnamnet(domain, driver)



