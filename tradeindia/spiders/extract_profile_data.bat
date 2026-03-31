taskkill /F /IM python.exe /T

start "1" scrapy crawl extract_profile_data -a start_id=950004 -a end_id=1000000

start "2" scrapy crawl extract_profile_data -a start_id=1000001 -a end_id=2000000

start "3" scrapy crawl extract_profile_data -a start_id=2000001 -a end_id=3000000

start "4" scrapy crawl extract_profile_data -a start_id=3000001 -a end_id=4000000

start "5" scrapy crawl extract_profile_data -a start_id=4000001 -a end_id=5000000

start "6" scrapy crawl extract_profile_data -a start_id=5000001 -a end_id=6000000

start "7" scrapy crawl extract_profile_data -a start_id=6000001 -a end_id=7000000

