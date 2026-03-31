import pymysql
from datetime import datetime

today = datetime.today().strftime("%d%m%Y")
#
# con=pymysql.connect(host="localhost",user="root",password='Paresh@123',
#                                  database="Trade_India_Company_Data")


con=pymysql.connect(host="localhost",user="root",password='Paresh@123',
                                 database="Tradeindia_data")

cursor=con.cursor()

link_table=f"trade_india_link"

final_link_table=f"final_trade_india_link"

page_table=f"trade_india_product_pages"

profile_table=f"trade_india_link_profile_link"

profile_data=f"profile_data_{today}"



folder_path=rf"D:\NIRAJ\Trade_India"

product_page_save_path=rf"D:\NIRAJ\Trade_India_product_page_new"

profile_page_save=rf"D:\NIRAJ\Trade_India_profile_page"