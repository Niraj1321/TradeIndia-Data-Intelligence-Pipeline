import os.path
from scrapy.cmdline import execute

import scrapy,json

from tradeindia.db_config import cursor,con, profile_table,profile_data,profile_page_save

from tradeindia.header_cookies import headers,cookies
from twisted.internet.error import TimeoutError, DNSLookupError, ConnectionRefusedError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError

class ExtractProfileDataSpider(scrapy.Spider):
    name = "extract_profile_data"
    allowed_domains = ["www.tradeindia.com"]
    start_urls = ["https://www.tradeindia.com/"]

    def __init__(self,start_id,end_id):
        self.folder_path = profile_page_save
        os.makedirs(self.folder_path,exist_ok=True)
        self.start_id=start_id
        self.end_id=end_id

        query=f"""
        CREATE TABLE IF NOT EXISTS {profile_data}(
        id int primary key auto_increment,
        Company_Name VARCHAR(255),
        Company_Logo TEXT,
        Company_Description TEXT,
        Address TEXT,
        City VARCHAR(100),
        State VARCHAR(100),
        Country_Name VARCHAR(100),
        Location TEXT,
        Gst_No VARCHAR(50),
        Annual_Turnover VARCHAR(100),
        Business_Type VARCHAR(255),
        Establishment INT,
        Employee_Count INT,
        Owner_Name VARCHAR(100),
        Certificate TEXT,
        Website TEXT,
        Service_meta_data TEXT
        );
        """
        cursor.execute(query)
        con.commit()
        self.logger.info(f"{profile_data} can be created sucessfully...")


    def start_requests(self):

        query = f"select * from {profile_table} where status='Pending' and id between {self.start_id} and {self.end_id}"
        # query = f"select * from {profile_table} where status='Redirect' limit 1"
        cursor.execute(query)
        all_data = cursor.fetchall()

        for data in all_data:

            u_id = data[0]


            url = data[1]
            category = data[2]


            new_folder_path = os.path.join(self.folder_path, category.replace('-', '_').replace('/', '_'))
            os.makedirs(new_folder_path, exist_ok=True)
            file_path = os.path.join(new_folder_path, f"{u_id}.txt")

            meta = {"u_id": u_id, "category": category, "page": u_id, "file_path": file_path,
                    "file": f"{u_id}.txt", "folder_path": new_folder_path}

            if os.path.exists(file_path):
                yield scrapy.FormRequest(f"file:///{file_path}", meta=meta, dont_filter=True)
            else:
                yield scrapy.Request(url, headers=headers, cookies=cookies, meta=meta, errback=self.handle_error,dont_filter=True)
            break

    def handle_error(self, failure):
        # Log all failures
        self.logger.error(repr(failure))
        request = failure.request
        u_id=request.meta.get('u_id')

        up_txt=None
        # Handle different error types
        if failure.check(HttpError):
            response = failure.value.response
            up_txt='HttpError'
            self.logger.error('HTTP error on %s: %s', response.url, response.status)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNS lookup failed on %s', request.url)
            up_txt = 'DNSLookupError'


        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('Timeout error on %s', request.url)
            up_txt = 'Timeout'

        else:
            self.logger.error('Unhandled failure: %s', failure)
            up_txt = 'Unhandled failure'

        cursor.execute(f"update {profile_table} set status='{up_txt}' where id={u_id}")
        con.commit()
        self.logger.info(f"{profile_data} can be update {up_txt} id's : {u_id}")

    def insert_data(self, item):
        keys = ", ".join(item.keys())
        placeholders = ", ".join(["%s"] * len(item))
        values = tuple(item.values())

        insert_query = f"""
                INSERT IGNORE INTO {profile_data} ({keys})
                VALUES ({placeholders})
            """

        try:
            cursor.execute(insert_query, values)
            con.commit()
            self.logger.info("Data inserted successfully.")
        except Exception as e:
            self.logger.error(f"Failed to insert data: {e}")

    def parse(self, response, **kwargs):
        if response.status == 200:
            u_id = response.meta['u_id']
            category = response.meta['category']
            file = response.meta['file']
            folder_path = response.meta['folder_path']
            file_path = response.meta['file_path']

            json_dic=json_txt=None


            try:
                json_txt=response.xpath('//script[@id="__NEXT_DATA__"]//text()').get()
                json_dic = json.loads(json_txt)
            except Exception as e:
                self.logger.info(f"Exception:{e}")


            if not os.path.exists(file_path):
                try:
                    with open(file_path, "w", encoding="utf-8") as fp:
                        fp.write(response.text)
                        self.logger.info(f"File write Successfully...")
                except:
                    os.remove(file_path)

                    self.logger.info(f"{file} file deleted...")

            item={}
            if json_txt:
                company_desc_path=json_dic['props']['pageProps']['initialState']['sellerProfile']['seller_profile']['seller_profile_res']

                try:
                    base_path=json_dic['props']['pageProps']['initialState']['sellerProfile']['seller_profile']['seller_profile_res']['company_details_data']
                    item['Company_Name'] = base_path.get('co_name', None)
                    if not item['Company_Name']:
                        item['Company_Name'] = base_path.get('initial_co_name', None)

                    item['City'] = base_path.get('city', None)
                    item['Country_Name'] = base_path.get('country_name', None)

                    item['Address'] = base_path.get('address', None)
                    item['Website'] = base_path.get('catalog_private_domain', None)

                    item['Gst_No'] = base_path.get('gst_no', None)
                    item['Owner_Name'] = base_path.get('owner_name', None)

                    item['Company_Logo'] = base_path.get('company_logo', None)

                    item['Location'] = base_path.get('map_url', None)

                    item['Certificate'] = base_path.get('trust_stamp_url', None)
                    if item['Certificate']:
                        item['Certificate'] = f"https://www.tradeindia.com" + item['Certificate']

                    item['Employee_Count'] = base_path.get('business_details', None).get('employees_count', None)

                    item['Annual_Turnover'] = base_path.get('business_details', None).get('annual_turnover', None)

                    item['Establishment'] = base_path.get('business_details', None).get('establishment', None)

                    business_type = base_path.get('business_details', None).get('business_type', None)

                    if business_type:
                        item['Business_Type'] = ' | '.join(business_type)

                    item['State'] = base_path.get('state', None)

                    item['Company_description'] = company_desc_path.get('seller_prof_metatags', None).get('description',
                                                                                                          None)

                    if not item['Company_description']:
                        item['Company_description'] = company_desc_path.get('og_metatags', None).get('description', None)

                    product_service_data = company_desc_path.get('product_services_data', None)

                    service_meta_data = []
                    for service_data in product_service_data:
                        category_name = service_data.get('cat_name', None)
                        category_img = service_data.get('cat_img_url', None)
                        p_data = []
                        for i in service_data['products']:
                            p_info = {
                                "Product_Name": i.get('prod_name', None),
                                "Product_image": f"https://www.tradeindia.com{i.get('prod_url', None)}",
                                "Product_url": f"https://www.tradeindia.com/{i.get('prod_img_url', None)}"
                            }

                            p_data.append(p_info)

                        service_json = {
                            "Category_Name": category_name,
                            "Category_Image": category_img,
                            "Product_List": p_data
                        }
                        service_meta_data.append(service_json)

                    item['Service_meta_data'] = json.dumps(service_meta_data)

                    self.insert_data(item)

                    u_query = f"update {profile_table} set STATUS='Done',FILE_NAME='{file}',FOLDER_PATH='{folder_path}',UNIQUE_ID='{u_id}' where id={u_id}"
                    cursor.execute(u_query)
                    con.commit()
                    self.logger.info(f"update {profile_table} ID's : {u_id} ...")
                except Exception as e:
                    self.logger.info(f" {u_id} Redirect Url...")
                    u_query = f"update {profile_table} set STATUS='Redirect' where id={u_id}"
                    cursor.execute(u_query)
                    con.commit()
                    self.logger.info(f"update {profile_table} Redirect Url -ID's : {u_id} ...")



if __name__ == '__main__':
    execute(f"scrapy crawl extract_profile_data -a start_id=2128918 -a end_id=3007016".split())



