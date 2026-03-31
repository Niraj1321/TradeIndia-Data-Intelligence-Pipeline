import json
import os.path

import scrapy
from scrapy import signals
from tradeindia.db_config import cursor,con, final_link_table,page_table,folder_path
# from db_config import cursor,con, final_link_table
from tradeindia.header_cookies import headers,cookies
from scrapy.cmdline import execute

class TradeIndiaLinkProductLinkSpider(scrapy.Spider):
    name = "trade_india_link_profile_link"
    allowed_domains = ["www.tradeindia.co="]
    start_urls = ["https://www.tradeindia.co="]
    product_link=page_table


    def __init__(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.product_link}(
            ID INT PRIMARY KEY AUTO_INCREMENT,
            URL VARCHAR(300),
            CATEGORY VARCHAR(300),
            PAGE_NO VARCHAR(20),
            FILE_NAME VARCHAR(200) DEFAULT NULL,
            FOLDER_PATH VARCHAR(200) DEFAULT NULL,
            STATUS VARCHAR(20) DEFAULT 'PENDING'
            );
            """
        profile_query=f"""
                     CREATE TABLE IF NOT EXISTS {self.name}(
                    ID INT PRIMARY KEY AUTO_INCREMENT,
                    URL VARCHAR(300) UNIQUE,
                    CATEGORY VARCHAR(300),
                    PAGE_NO VARCHAR(20),
                    UNIQUE_ID VARCHAR(300) DEFAULT NULL,
                    FILE_NAME VARCHAR(200) DEFAULT NULL,
                    FOLDER_PATH VARCHAR(200) DEFAULT NULL,
                    STATUS VARCHAR(20) DEFAULT 'PENDING'
                    );
                    """
        cursor.execute(query)
        cursor.execute(profile_query)
        con.commit()
        self.folder_path=folder_path
        self.logger.info(f"table created sucessfully...")

    def start_requests(self):

        query = f"select * from {final_link_table} where status='Pending'"
        # query = f"select * from {final_link_table} where status='500' limit 100"

        cursor.execute(query)
        all_data = cursor.fetchall()

        for data in all_data:

            base_url=data[1]
            new_folder_path = os.path.join(self.folder_path,data[2].replace('-','_'))
            os.makedirs(self.folder_path,exist_ok=True)
            new_folder_path=os.path.join(new_folder_path,data[3].replace('-','_').replace('/','_'))
            os.makedirs(new_folder_path, exist_ok=True)
            file_name=f"{data[0]}.txt"
            file_path=os.path.join(new_folder_path,file_name)

            if 'api' not in data[1]:
                product_url = data[1].split('.com/')[-1]
                base_url = f'https://api.tradeindia.com/seller-category/categories/seller-sub-category-entire-data?url=/{product_url}&page=1&per_page=50'

            meta = {"url":base_url,"file_path":file_path,"u_id": data[0],"primary_category":data[2], "category": data[3], "file_name": file_name, "folder_path": self.folder_path}
            if not os.path.exists(file_path):
                yield scrapy.Request(base_url, cookies=cookies, headers=headers, meta=meta, dont_filter=True)
            else:
                yield scrapy.FormRequest(f"file:///{file_path}", meta=meta, dont_filter=True)
            # break

    def on_response_received(self, response, request, spider):
        # Only act on non-200
        if response.status != 200:
            u_id=request.meta.get('u_id')
            self.logger.info(f"[Signal] Non-200 status: {response.status} for {response.url}")
            update_query = f"update {final_link_table} set status='{response.status}' where id={u_id}"
            cursor.execute(update_query)
            self.logger.info(f"{final_link_table} ID's :{u_id} updated successfully...")
            con.commit()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.start_id = kwargs.get('start_id')  # Safely extract it
        spider.end_id = kwargs.get('end_id')
        crawler.signals.connect(spider.on_response_received, signal=signals.response_received)
        return spider

    def parse(self, response, **kwargs):
        if response.status == 200:
            is_executable=False
            url=response.meta['url']
            primary_category=response.meta['primary_category']
            u_id=response.meta['u_id']
            category=response.meta['category']
            file=response.meta['file_name']
            folder_path = response.meta['folder_path']
            file_path=response.meta['file_path']
            total_result=None
            try:
                json_dic = json.loads(response.text)
            except Exception as e:
                product_url = url.split('.com/')[-1]
                base_url = f'https://api.tradeindia.com/seller-category/categories/seller-sub-category-entire-data?url=/{product_url}&page=1&per_page=50'
                u_query=f"update {final_link_table} set URL='{base_url}' where id={u_id}"
                cursor.execute(u_query)
                con.commit()
                self.logger.info(f"Url can be Changed...")

                self.logger.info(f'Response Getting in html Form...')
            # if not f"file:///" in response.url:
            #     json_dic = json.loads(response.text)
            # else:
            #     json_dic=response.text
            try:
                current_page = json_dic['listing']['pagination']['current_page']
                total_result = json_dic['listing']['listing_count']
            except Exception as e:
                current_page = json_dic['listing_data']['pagination']['current_page']
                total_result = json_dic['listing_data']['listing_count']
                self.logger.warning(f"Single Api Request can be Ariived...")

            item={}
            if total_result>20000:
                try:
                    top_category=json_dic['top_categories']['top_micro_categories_data']
                    for cat in top_category:
                        base_u = f'https://api.tradeindia.com/manufacturers/manufacturers/single-api?url={cat['url']}&page={current_page}&per_page=50&current_page={current_page}&top_rated_seller_limit=5&top_rated_product_limit=10&testimonial_limit=10&complete_url={cat['url'].replace('/', '%2F')}',
                        item['URL'] = base_u
                        item['CATEGORY'] = primary_category
                        item['SUB_CATEGORY'] = f"{category}/{cat['keyword'].upper()}"
                        self.insert_data(item, final_link_table)
                except:
                    top_category=json_dic['list_city_data']
                    for cat in top_category:
                        base_u=f"https://www.tradeindia.com/{cat['url']}"
                        item['URL'] = base_u
                        item['CATEGORY'] = primary_category
                        item['SUB_CATEGORY'] = f"{category}/{cat['city_name'].upper()}"
                        self.insert_data(item,final_link_table)
                    delete_query=f"delete from {final_link_table} where id={u_id}"
                    cursor.execute(delete_query)
                    con.commit()
                    self.logger.info(f"{u_id} ids data deleted successfully...")

            elif total_result<20000 and total_result>10000:
                filetr_key=['manufacturer','supplier','exporter','traders','wholesaler_or_distributor']
                filter_flag=False
                for f in filetr_key:
                    if f in url:
                        filter_flag=True
                        break
                if not filter_flag:
                    for f in filetr_key:
                        if 'single-api' in url:
                            chunk_url = url.split('&page')
                            new_url = f"{chunk_url[0]}&{f}=true&page{chunk_url[1]}"

                        else:
                            try:
                                new_url = url.split('/&page')[0] + f'/&{f}=true&page' + url.split('/&page')[1]
                            except Exception as e:
                                self.logger.info(f"Error Found on ID's : {u_id} ....")


                        item['URL'] = new_url
                        item['CATEGORY'] = primary_category
                        item['SUB_CATEGORY'] = f"{category}"
                        item['filter'] = f"Yes"
                        self.insert_data(item, final_link_table)

                    delete_query = f"delete from {final_link_table} where id={u_id}"
                    cursor.execute(delete_query)
                    con.commit()
                    try:
                        os.remove(file_path)
                    except:
                        pass
                    self.logger.info(f"{u_id} ids data deleted successfully...")
                else:
                    is_executable=True
            else:
                is_executable = True

            if is_executable:
                if not os.path.exists(file_path):
                    try:
                        with open(file_path,"w",encoding="utf-8")as fp:
                            json.dump(json_dic, fp, indent=4)
                            self.logger.info(f"File write Successfully...")
                    except:
                        os.remove(file_path)
                        self.logger.info(f"{file} file deleted...")

                try:
                    result=json_dic['listing']['data']
                except:
                    result=json_dic['listing_data']['listing_data']

                try:
                    total_page=json_dic['listing']['pagination']['total_pages']
                except:
                    total_page=json_dic['listing_data']['pagination']['total_pages']

                profile_list=[]
                if result:
                    for result_dic in result:
                        p_url="https://www.tradeindia.com"+result_dic['profile_url']
                        profile_list.append((p_url,category,current_page,))

                    query=f"insert ignore into {self.name}(URL,CATEGORY,PAGE_NO) values(%s,%s,%s)"
                    page_query=f"insert ignore into {self.product_link}(URL,CATEGORY,PAGE_NO,FILE_NAME,FOLDER_PATH,STATUS) values(%s,%s,%s,%s,%s,%s)"
                    page_value=(url,category,current_page,file,folder_path,"Done")
                    cursor.executemany(query,profile_list)
                    cursor.execute(page_query,page_value)
                    con.commit()
                    self.logger.info(f"Page :{current_page} all {len(result)} Records Inserted successfully..")

                    page_insert_value=[]
                    for p_no in range(2,total_page+1):
                        page_url=url.replace("page=1",f"page={p_no}")
                        page_insert_value.append((page_url,category,p_no))
                    page_query = f"insert ignore into {self.product_link}(URL,CATEGORY,PAGE_NO) values(%s,%s,%s)"
                    cursor.executemany(page_query,page_insert_value)
                    con.commit()
                    self.logger.info(f"All Pages of Category {category} Inserted successfully..")

                    update_query=f"update {final_link_table} set status='Done',Data_count='{total_result}' where id={u_id}"
                    cursor.execute(update_query)
                    self.logger.info(f"{final_link_table} ID's :{u_id} updated successfully...")
                    con.commit()
                else:

                    self.logger.info(f"Result Not Found -200 status: {response.status} for {response.url}")
                    update_query = f"update {final_link_table} set status='Result Not Found' where id={u_id}"
                    cursor.execute(update_query)
                    self.logger.info(f"{final_link_table} ID's :{u_id} updated successfully...")
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
    execute(f"scrapy crawl trade_india_link_profile_link".split())
