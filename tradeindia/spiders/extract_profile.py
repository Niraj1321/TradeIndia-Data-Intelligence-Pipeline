import os.path
from scrapy.cmdline import execute

import scrapy,json
from scrapy import signals
from tradeindia.db_config import cursor,con, profile_table,page_table,product_page_save_path


from tradeindia.header_cookies import headers,cookies


class ExtractProfileSpider(scrapy.Spider):
    name = "extract_profile"
    allowed_domains = ["www.tradeindia.com"]
    start_urls = ["https://www.tradeindia.com/"]

    def __init__(self, start_id, end_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.folder_path = product_page_save_path
        self.start_id = start_id
        self.end_id = end_id

    def on_response_received(self, response, request, spider):
        # Only act on non-200
        if response.status != 200:
            u_id=request.meta.get('u_id')
            self.logger.info(f"[Signal] Non-200 status: {response.status} for {response.url}")
            update_query = f"update {page_table} set status='{response.status}' where id={u_id}"
            cursor.execute(update_query)
            self.logger.info(f"{page_table} ID's :{u_id} updated successfully...")
            con.commit()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.start_id = kwargs.get('start_id')  # Safely extract it
        spider.end_id = kwargs.get('end_id')
        crawler.signals.connect(spider.on_response_received, signal=signals.response_received)
        return spider

    def start_requests(self):

        # query = f"select * from {page_table} where status='Pending' and id between {self.start_id} and {self.end_id} limit 5000"

        query = f"select * from {page_table} where status='PENDING' limit 10000"
        cursor.execute(query)
        all_data = cursor.fetchall()

        for data in all_data:

            u_id=data[0]
            url=data[1]
            category=data[2]
            page_no=data[3]

            new_folder_path=os.path.join(self.folder_path,category.replace('-','_').replace('/','_').replace("'",""))
            os.makedirs(new_folder_path,exist_ok=True)
            file_path=os.path.join(new_folder_path,f"{page_no}.txt")

            meta={"u_id":u_id,"category":category,"page":page_no,"file_path":file_path,"file":f"{page_no}.txt","folder_path":new_folder_path}

            if os.path.exists(file_path):
                yield scrapy.FormRequest(f"file:///{file_path}",meta=meta,dont_filter=True)
            else:
                yield scrapy.Request(url,headers=headers,cookies=cookies,meta=meta,dont_filter=True)
            break


    def parse(self, response, **kwargs):
        if response.status==200:
            u_id=response.meta['u_id']
            category = response.meta['category']
            file = response.meta['file']
            folder_path = response.meta['folder_path']
            file_path = response.meta['file_path']
            json_dic=None

            try:
                json_dic = json.loads(response.text)
            except Exception as e:
                self.logger.info(f"Exception:{e}")

            try:
                current_page = json_dic['listing']['pagination']['current_page']
            except Exception as e:
                current_page = json_dic['listing_data']['pagination']['current_page']
                self.logger.warning(f"Single Api Request can be Ariived...")

            if not os.path.exists(file_path):
                try:
                    with open(file_path, "w", encoding="utf-8") as fp:
                        json.dump(json_dic, fp, indent=4)
                        self.logger.info(f"File write Successfully...")
                except:
                    os.remove(file_path)
                    self.logger.info(f"{file} file deleted...")

            try:
                result = json_dic['listing']['data']
            except:
                result = json_dic['listing_data']['listing_data']



            profile_list = []
            if result:
                for result_dic in result:
                    p_url = "https://www.tradeindia.com" + result_dic['profile_url']
                    profile_list.append((p_url, category, current_page,))
                query = f"insert ignore into {profile_table}(URL,CATEGORY,PAGE_NO) values(%s,%s,%s)"
                cursor.executemany(query, profile_list)
                con.commit()
                self.logger.info(f"Page :{current_page} all {len(result)} Records Inserted successfully..")

                update_query = f"update {page_table} set status='Done',FILE_NAME='{file}',FOLDER_PATH='{folder_path}' where id={u_id}"
                cursor.execute(update_query)
                self.logger.info(f"{page_table} ID's :{u_id} updated successfully...")
                con.commit()
            else:
                # os.remove(file_path)
                # self.logger.info(f"{file} file deleted...")
                update_query = f"update {page_table} set status='Result Not Found' where id={u_id}"
                cursor.execute(update_query)
                self.logger.info(f"{page_table} ID's :{u_id} updated successfully...")
                con.commit()

    def insert_data(self, item, table_name):
        keys = ", ".join(item.keys())
        placeholders = ", ".join(["%s"] * len(item))
        values = tuple(item.values())

        insert_query = f"""
            INSERT IGNORE INTO {table_name} ({keys})
            VALUES ({placeholders})
        """

        try:
            cursor.execute(insert_query, values)
            con.commit()
            self.logger.info("Data inserted successfully.")
        except Exception as e:
            self.logger.error(f"Failed to insert data: {e}")


if __name__ == '__main__':
    execute(f"scrapy crawl extract_profile -a start_id=120001 -a end_id=169411".split())


