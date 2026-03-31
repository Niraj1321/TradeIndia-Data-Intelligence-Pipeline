

import scrapy


class TradeindiaItem_link(scrapy.Item):
    URL=scrapy.Field()
    CATEGORY = scrapy.Field()


class TradeindiaItem_link_final(scrapy.Item):
    URL=scrapy.Field()
    CATEGORY = scrapy.Field()
    SUB_CATEGORY = scrapy.Field()
    u_id=scrapy.Field()


class TradeindiaItem_Product_Link(scrapy.Item):
    URL=scrapy.Field()
    CATEGORY = scrapy.Field()
    PAGE_NO = scrapy.Field()
    UNIQUE_ID=scrapy.Field()
    FILE_NAME = scrapy.Field()
    FOLDER_PATH = scrapy.Field()
    STATUS = scrapy.Field()



