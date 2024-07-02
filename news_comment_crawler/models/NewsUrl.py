from array import array
from mongoengine import *
from datetime import datetime
from bson import ObjectId

class NewsUrl(Document):
    # _id = ObjectIdField()
    # website = ObjectIdField()
    # topic = ObjectIdField()
    # keyword = ObjectIdField()
    # crawlerconfig = ObjectIdField()
    # news_group = ObjectIdField()
    # group_news = IntField()
    # name = StringField()
    # news_url = StringField()
    # news_title = StringField()
    # news_summary = StringField()
    # npl_authors = ListField()
    # npl_date = DateField()
    # npl_content = MultiLineStringField()
    # npl_keywords = ListField()
    # npl_summary = StringField()
    # created = DateField()
    # collected = DateField()
    # posted = DateField()
    # meta = {'collection': 'newsdailies'}
    # @classmethod
    # def post_save(cls, sender, document, **kwargs):
    #     print(document._id)

    # '''Get News's URL from Database'''
    # def getUrl(self):
    #     urls = NewsUrl.objects()
    #     return urls
    _id = ObjectIdField()
    news_url = StringField()
    meta = {'collection': 'news_url'}
    @classmethod
    def post_save(cls, sender, document, **kwargs):
        print(document._id)

    '''Get News's URL from Database'''
    def getUrl(self):
        urls = NewsUrl.objects()
        return urls
    '''Test'''
    # def insertUrl(self, listUrl):
    #     # tạo array list các bài báo
    #     #listUrl = ['https://dantri.com.vn/kinh-doanh/pho-thong-doc-se-khong-ha-chuan-tin-dung-20230621114057709.htm']

    #     lenListUrl = len(listUrl)
    #     print(lenListUrl)
    #     for i in range(lenListUrl):

    #         '''insert url to database'''

    #         newsUrlModel = NewsUrl(_id = ObjectId() , name_url = listUrl[i])
    #         newsUrlModel.save()
    #         print(newsUrlModel.to_json())


#insert url to database for testing
# listUrl = ['https://dantri.com.vn/kinh-doanh/pho-thong-doc-se-khong-ha-chuan-tin-dung-20230621114057709.htm'
#           , 'https://vietnamnet.vn/duong-tinh-cua-phuong-oanh-truoc-khi-dang-ky-ket-hon-voi-shark-binh-2154981.html'
#           , 'https://hanoimoi.vn/khai-mac-hoi-nghi-lan-thu-muoi-ba-ban-chap-hanh-dang-bo-thanh-pho-ha-noi-khoa-xvii-538828.html'
#           , 'https://cand.com.vn/Chong-dien-bien-hoa-binh/doi-tuong-nguyen-van-dai-trang-tron-xuyen-tac-vu-gay-roi-antt-o-dak-lak-i697108/'
#           , 'https://cand.com.vn/Ban-tin-113/van-chuyen-4-banh-heroin-voi-gia-cuoc-20-trieu-dong-i699952/'
#           , 'https://thanhnien.vn/noi-lo-tri-tue-nhan-tao-tiep-quan-the-gioi-185230629122510256.htm'
#           , 'https://thanhnien.vn/ca-mau-trung-tam-y-te-hu-minh-da-hoan-tra-2-ti-dong-tam-ung-18523071114213385.htm'
#           , 'https://vnexpress.net/dia-phuong-chua-ban-giao-du-mat-bang-12-du-an-cao-toc-bac-nam-4625290.html'
#           , 'https://vnexpress.net/loat-du-an-o-tp-hcm-se-khoi-dong-nho-co-che-moi-4625260.html'
#           , 'https://dantri.com.vn/kinh-doanh/pho-thong-doc-se-khong-ha-chuan-tin-dung-20230621114057709.htm'
#           , 'https://dantri.com.vn/xa-hoi/vu-tan-cong-o-dak-lak-se-som-dua-ra-xet-xu-cac-doi-tuong-pham-toi-20230707212714509.htm']
# newsUrl.insertUrl(listUrl)