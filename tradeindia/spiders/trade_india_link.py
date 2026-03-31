import scrapy
from scrapy.cmdline import execute
from tradeindia.items import TradeindiaItem_link
from tradeindia.db_config import cursor,con
from tradeindia.header_cookies import headers,cookies


class TradeIndiaLinkSpider(scrapy.Spider):
    name = "trade_india_link"
    allowed_domains = ["www.tradeindia.com"]
    start_urls = ["https://www.tradeindia.com/"]



    def __init__(self):
        query=f"""
        CREATE TABLE IF NOT EXISTS {self.name}(
        ID INT PRIMARY KEY AUTO_INCREMENT,
        URL VARCHAR(300),
        CATEGORY VARCHAR(300),
        STATUS VARCHAR(20) DEFAULT 'PENDING'
        );
        """
        cursor.execute(query)
        con.commit()
        self.logger.info(f"table created sucessfully...")


    def start_requests(self):
        yield scrapy.Request('https://www.tradeindia.com/seller/', cookies=cookies, headers=headers)

    def parse(self, response,**kwargs):
        if response.status==200:
            base_link_section=response.xpath('//div[@class="row mt-3"]//div[@class="cat-det-wrp"]/a[@target="_self"]//@href').getall()
            for link in base_link_section:
                item = TradeindiaItem_link()

                category_name=link.split('/seller/')[-1].replace('/','')
                item['URL'] = link
                item['CATEGORY'] = category_name.upper()
                yield item










if __name__ == '__main__':
    execute(f"scrapy crawl trade_india_link".split())
