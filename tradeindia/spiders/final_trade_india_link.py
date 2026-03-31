import scrapy
from tradeindia.items import TradeindiaItem_link_final
from parsel import Selector
from tradeindia.db_config import cursor,con,link_table
from tradeindia.header_cookies import headers,cookies
from scrapy.cmdline import execute

class FinalTradeIndiaLinkSpider(scrapy.Spider):
    name = "final_trade_india_link"
    allowed_domains = ["www.tradeindia.com"]
    start_urls = ["https://www.tradeindia.com"]

    def __init__(self):
        query = f"""
         CREATE TABLE IF NOT EXISTS {self.name}(
         ID INT PRIMARY KEY AUTO_INCREMENT,
         URL VARCHAR(300),
         CATEGORY VARCHAR(300),
         SUB_CATEGORY VARCHAR(300),
         Data_count VARCHAR(30) DEFAULT NULL,
         filter VARCHAR(30) DEFAULT NULL,
         STATUS VARCHAR(20) DEFAULT 'PENDING'
         );
         """
        cursor.execute(query)
        con.commit()
        self.logger.info(f"table created sucessfully...")

    def start_requests(self):

        query=f"select * from {link_table} where status='Pending'"
        cursor.execute(query)
        all_data=cursor.fetchall()
        for data in all_data:
            meta={"u_id":data[0],"category":data[2]}
            yield scrapy.Request(data[1], cookies=cookies, headers=headers,meta=meta,dont_filter=True)
            break


    def parse(self, response, **kwargs):
        if response.status == 200:
            all_category_link = response.xpath(
                '//div[@class="row cat-row"]//div[@class="col-lg-3 col-6"]//div[contains(@class,"image-section")]/a[contains(@class,"title")]').getall()
            if not all_category_link:
                all_category_link=response.xpath('//div[contains(@class,"catshowcase-section")]/div/a').getall()

            total_data=len(all_category_link)-1
            for no,sub_link in enumerate(all_category_link):
                item = TradeindiaItem_link_final()

                sub_link_html = Selector(sub_link)
                sub_category_name = sub_link_html.xpath('.//*/text()').get()
                sub_category_link = sub_link_html.xpath('.//@href').get()

                item['URL'] = sub_category_link
                item['CATEGORY'] = response.meta['category']
                item['SUB_CATEGORY'] = sub_category_name.upper()
                if total_data==no:
                    item['u_id']=response.meta['u_id']
                else:
                    item['u_id'] = None

                yield item


if __name__ == '__main__':
    execute(f"scrapy crawl final_trade_india_link".split())
