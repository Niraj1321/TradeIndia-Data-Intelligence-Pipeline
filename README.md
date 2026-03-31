# 🕷️ TradeIndia Data Extraction Project

## 🌐 Site Overview

**TradeIndia ([https://www.tradeindia.com](https://www.tradeindia.com))** is one of India’s largest B2B marketplaces that connects:

* Manufacturers
* Suppliers
* Exporters
* Buyers
* Traders

The platform contains millions of business listings across multiple industries such as:

* Agriculture
* Chemicals
* Textiles
* Machinery
* Electronics
* Construction

Each company profile typically includes:

* Company details
* Contact information
* Business type (Supplier / Manufacturer / Buyer)
* Product catalog
* Certifications and trust badges

👉 This project extracts structured business intelligence data from TradeIndia at scale.

---

## 📌 Overview

This project is a **multi-stage scraping pipeline** built using Scrapy to extract:

* Suppliers
* Buyers
* Manufacturers
* Company details
* Product/service data

The system is designed for **large-scale, resumable data extraction** using a **database-driven architecture**.

---
# ⚠️ Challenges Faced
1. Data Visibility Limitation

        TradeIndia restricts the number of listings visible for a single category or subcategory.
        
        Large categories return incomplete data
        Not all profiles are accessible in one request
        
        Solution:
        Implemented a filter-based splitting strategy in trade_india_link_product_link.py:
        
        Applied filters like manufacturer, supplier, exporter, etc.
        Broke large categories into smaller segments
        Reinserted filtered URLs into the pipeline

2. Handling Large Data Volume

        Some categories contain 10,000+ to 20,000+ records, making extraction difficult.
        
        Solution:
        
        Used conditional logic to:
        Split data by filters
        Split by city or micro-categories when needed
        Controlled execution using database-driven workflow

3. Dynamic API & Response Variations

        TradeIndia returns data in different JSON structures:
        
        listing
        listing_data
        
        Solution:
        
        Implemented fallback parsing logic
        Handled both response formats safely

4. Anti-Scraping & Request Blocking
    
       Frequent requests may lead to:
    
       HTTP errors (403, 500)
       Timeouts
       Blocked responses
    
       Solution:
    
       Used custom headers & cookies
       Implemented retry/error handling
       Stored response status in database

5. Pagination Handling

        Listings are spread across multiple pages.
        
        Solution:
        
        Extracted total pages from API
        Dynamically generated page URLs
        Stored them in page_table for tracking

6. Data Duplication

        Repeated runs could insert duplicate records.
        
        Solution:
        
        Used INSERT IGNORE in database queries
        Added unique constraints where required

7. Resume & Recovery Handling

        Long-running scraping jobs can fail midway.
        
        Solution:
        
        Used STATUS field (PENDING, DONE, ERROR)
        Saved responses as local files
        Enabled resume from last processed step

8. Complex Nested Data Extraction

        Company profiles contain deeply nested JSON data.
        
        Solution:
        
        Parsed __NEXT_DATA__ JSON structure
        Extracted structured fields like:
        Company info
        Business details
        Product/service metadata

✅ Summary of Challenges

    The biggest challenge was handling data limitations and scale, which was solved using:
    
    filter-based splitting
    database-driven pipeline
    staged scraping architecture
-------------------------------------------------

# Architecture (Pipeline Flow)

```
Step 1 → Extract main categories
Step 2 → Extract subcategories
Step 3 → Generate listing & pagination links
Step 4 → Extract profile URLs
Step 5 → Extract full company data
```

---
# Important Note
      -Before run a script you can set the page save path inside db_config.py file also check the database configration.


# ⚙️ Requirements

## 🔹 Python

* Python 3.8+

## 🔹 Install Dependencies

```bash
pip install scrapy
pip install pymysql
pip install parsel
pip install twisted
```

---

# Project Structure

```text
tradeindia/
├── tradeindia/
│   ├── .idea/
│   ├── spiders/
│   │   ├── __init__.py
│   │   ├── extract_profile.bat
│   │   ├── extract_profile.py
│   │   ├── extract_profile_data.bat
│   │   ├── extract_profile_data.py
│   │   ├── final_trade_india_link.py
│   │   ├── product_link.bat
│   │   ├── trade_india_link.py
│   │   └── trade_india_link_product_link.py
│   ├── __init__.py
│   ├── database_backup.py
│   ├── db_config.py
│   ├── excel.py
│   ├── header_cookies.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── profile_data_15102025.xlsx
│   ├── README.md
│   └── settings.py
└── scrapy.cfg
```

## What Each File Does

### Root Files

#### `scrapy.cfg`

Scrapy project configuration file. It tells Scrapy where the project settings module is located.

---

### Main Package: `tradeindia/`

#### `__init__.py`

Marks the folder as a Python package.

#### `.idea/`

IDE project settings folder created by PyCharm.

---

### `spiders/` Folder

#### `spiders/__init__.py`

Marks the spiders folder as a Python package.

#### `trade_india_link.py`

Step 1 spider. Extracts first-level category links from TradeIndia seller pages and stores them in `trade_india_link` table.

#### `final_trade_india_link.py`

Step 2 spider. Reads first-level category links and extracts subcategory links into `final_trade_india_link` table.

#### `trade_india_link_product_link.py`

Step 3 spider. Reads subcategory links, generates listing/API page URLs, saves page data, and inserts profile listing links.

#### `extract_profile.py`

Step 4 spider. Reads page URLs from `trade_india_product_pages` and extracts company profile links into `trade_india_link_profile_link`.

#### `extract_profile_data.py`

Step 5 spider. Opens each company profile and extracts final business data such as company name, address, GST, business type, and product/service details.

#### `extract_profile.bat`

Windows batch file to run the `extract_profile.py` spider quickly.

#### `extract_profile_data.bat`

Windows batch file to run the `extract_profile_data.py` spider quickly.

#### `product_link.bat`

Windows batch file to run the product/profile listing spider.

---

### Configuration & Utility Files

#### `db_config.py`

Contains database connection details, shared cursor/connection objects, table names, and other common config values.

#### `header_cookies.py`

Stores request headers and cookies required to access TradeIndia pages and APIs properly.

#### `items.py`

Defines Scrapy item classes used to structure scraped data.

#### `middlewares.py`

Contains custom downloader or spider middlewares if used in the project.

#### `pipelines.py`

Processes scraped items before storing them, such as inserting records into the database or cleaning data.

#### `settings.py`

Main Scrapy settings file. Controls project behavior like pipelines, user-agent, concurrency, delays, logging, and more.

#### `database_backup.py`

Utility file used for database backup-related tasks.

#### `excel.py`

Utility script used to export or manage scraped data in Excel format.

---

### Output & Documentation

#### `profile_data_15102025.xlsx`

Generated Excel output file containing extracted profile data.

#### `README.md`

Project documentation file with setup, workflow, structure, and run instructions.

---

# 🗄️ Database Configuration

```python
link_table = "trade_india_link"
final_link_table = "final_trade_india_link"
page_table = "trade_india_product_pages"
profile_table = "trade_india_link_profile_link"
profile_data = f"profile_data_<today_date>"
```

---

# 🗃️ Tables & Purpose

## 1. trade_india_link

Stores main category links

## 2. final_trade_india_link

Stores subcategory links

## 3. trade_india_product_pages

Stores paginated listing/API URLs

## 4. trade_india_link_profile_link

Stores company profile URLs

## 5. profile_data_<today>

Final extracted dataset (company + product data)

---

#  How to Run

## Step 1: Extract Categories

```bash
scrapy crawl trade_india_link
```

## Step 2: Extract Subcategories

```bash
scrapy crawl final_trade_india_link
```

## Step 3: Generate Listing Pages

```bash
scrapy crawl trade_india_link_profile_link
```

## Step 4: Extract Profile Links

```bash
scrapy crawl extract_profile
```

## Step 5: Extract Final Data

```bash
scrapy crawl extract_profile_data -a start_id=1 -a end_id=1000000
```

---

# Final Output

Final data is stored in:

```
profile_data_<today>
```

Contains:

* Company details
* Contact info
* Business type
* Products/services

---

# 🌐 Data Source

* Website: [https://www.tradeindia.com](https://www.tradeindia.com)
* Extraction via:

  * HTML parsing
  * Internal APIs
  * Next.js JSON (**NEXT_DATA**)

---

# Notes

* Use valid headers & cookies
* Maintain STATUS fields (PENDING / DONE)
* Supports resume using saved files
* Ensure DB is running before execution

---

# Future Improvements

* Proxy rotation
* CAPTCHA handling
* Parallel scraping
* Data API layer

---

# Author

Niraj Chauhan

---

# Summary

A scalable pipeline to extract structured business data (suppliers, buyers, manufacturers, and products) from TradeIndia.
