import time
import requests
import random
import math
from datetime import datetime
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pymysql

try:
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='qal,1',
        db='kakaofund_db',
        charset='utf8'
    )
    print("데이터베이스 연결 성공")
    cur = conn.cursor()

except pymysql.MySQLError as e:
    print("데이터베이스 연결 실패:", e)

##Selenium 브라우저 옵션 설정
options = Options()
options.headless = True  # 브라우저 창을 띄우지 않고 실행

driver = webdriver.Chrome(options=options)

session = requests.Session()
retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

def insert_product(product_id,category_id,brand):
    url = f"https://gift.kakao.com/a/product-detail/v2/products/{product_id}"
    response = session.get(url,timeout=5)
    if response.status_code == 200:
        data = response.json()
        itemDetails = data.get('itemDetails', {})
        item = itemDetails.get('item', {})
    
        
        wish_count = random.randint(0, 100000)
        order_count = random.randint(0, 100000)
        
        cur.execute("""
            INSERT IGNORE INTO product (
                product_id, created_at, updated_at, name, price, type, photo, category_id, 
                brand_id, product_detail_id, wish_count, order_count, brand_name
            ) VALUES (%s, NOW(), NOW(), %s, %s, %s, %s, %s, %s, NULL, %s, %s, %s)
            """, (
                product_id, item.get('name'), item.get('basicPrice'), item.get('itemType'),
                item.get('imageUrl'), category_id, brand.get('id'), 
                wish_count, order_count, brand.get('name')
            ))
        # item.get('catalogId')의 결과가 실제 카테고리와 일치하지 않는 값이라 insert문 실패
        
        conn.commit() 
        print(f"Product {product_id} inserted successfully.")
    else:
        print(f"Failed to get product details for {product_id}")

def getProductInfo():
    cur.execute("SELECT category_id, parent_id FROM category WHERE parent_id is NOT NULL")
    indexs=cur.fetchall()
    for category_id,parent_id in indexs:
        print(category_id,parent_id)
        ###
        driver.get(f"https://gift.kakao.com/brand/category/{parent_id}/subcategory/{category_id}")
        time.sleep(1)
        
        total_count = driver.find_element(By.CSS_SELECTOR, "ul.list_srchtab > li:nth-child(2) span.num_g").text
        
        count=int(total_count.replace(",", ""))
        repeat_count = math.ceil(count / 100)
        for i in range(1, repeat_count + 1):
            try:
                url = f"https://gift.kakao.com/a/v1/display-category/BASIC/products?sortProperty=SCORE&lDisplayCategoryId={parent_id}&mDisplayCategoryId={category_id}&page={i}&size=100"
                response=session.get(url,timeout=10)
                if(response.status_code == 200):
                    data = response.json()  # 응답을 JSON 형태로 변환
                    products = data.get('products', {})
                    contents = products.get('contents', [])
                    for item in contents:
                        product_id=item.get('id')
                        brand=item.get('brand')
                        cur.execute("INSERT IGNORE INTO brand (brand_id,name, icon_photo, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())",
                                    (brand.get('id'),brand.get('name'), brand.get('imageUrl')))     
                        insert_product(product_id,category_id,brand)
                else:
                    print("Product not found")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                
            
            
