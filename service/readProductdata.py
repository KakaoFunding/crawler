## https://googlechromelabs.github.io/chrome-for-testing/#stable
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import random
from datetime import datetime

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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


def get_random_brand_name(cur):
    cur.execute("SELECT name FROM brand ORDER BY RAND() LIMIT 1;")
    result = cur.fetchone()
    return result[0] if result else None

def insert_product(product_id):
    url = f"https://gift.kakao.com/a/product-detail/v2/products/{product_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        itemDetails = data.get('itemDetails', {})
        item = itemDetails.get('item', {})
        
        wish_count = random.randint(0, 100000)
        order_count = random.randint(0, 100000)
        
        brand_name = get_random_brand_name(cur)
        
        cur.execute("""
            INSERT INTO product (
                product_id, created_at, updated_at, name, price, type, photo, category_id, 
                brand_id, product_detail_id, wish_count, order_count, brand_name
            ) VALUES (%s, NOW(), NOW(), %s, %s, %s, %s, %s, %s, NULL, %s, %s, %s)
            """, (
                product_id, item.get('name'), item.get('basicPrice'), item.get('itemType'),
                item.get('imageUrl'), item.get('catalogId'), item.get('brandId'), 
                wish_count, order_count, brand_name
            ))
        # item.get('catalogId')의 결과가 실제 카테고리와 일치하지 않는 값이라 insert문 실패
        
        conn.commit() 
        print(f"Product {product_id} inserted successfully.")
    else:
        print(f"Failed to get product details for {product_id}")

def insert_option(name, product_id):
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO options (created_at, updated_at, name, product_id) 
            VALUES (NOW(), NOW(), %s, %s)
        """, (name, product_id))
        
        conn.commit()
        inserted_id = cur.lastrowid 
        
        return inserted_id
    except pymysql.MySQLError as e:
        print("Database error:", e)
        conn.rollback() 
        return None
    finally:
        cur.close()

def insert_option_detail(name, option_id, stock_quantity=None, additional_price=None):
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO option_detail (created_at, updated_at, name, stock_quantity, additional_price, option_id) 
            VALUES (NOW(), NOW(), %s, %s, %s, %s)
        """, (name, stock_quantity, additional_price, option_id))
        
        conn.commit()
        inserted_id = cur.lastrowid
        
        print(f"Inserted option detail ID: {inserted_id}")
        return inserted_id
    except pymysql.MySQLError as e:
        print("Database error:", e)
        conn.rollback()
        return None
    finally:
        cur.close()

def getProductInfo():
  cur.execute("SELECT brand_id, `name` FROM brand")
  brand = cur.fetchall()
  count=0
  for brand_Id,brand_name in brand :
    count+=1
    print('brand id: ', brand_Id)
    url = f"https://gift.kakao.com/brand/{brand_Id}"
    driver.get(url)
    time.sleep(1)
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    product_urls = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, 'a[href*="/product/"]')]

    item_cnt = 0
    for product_url in product_urls:
        if(item_cnt == 100) : break
        item_cnt += 1
        
        driver.get(product_url)
        print(product_url)
        time.sleep(2)

        product_id=product_url.split('/product/')[1]
        print("상품 ID:", product_id)
        insert_product(product_id)

        # # 썸네일
        # thumbnail_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.nav_photo img')
        # for thumbnail in thumbnail_elements:
        #     print("썸네일 URL: " + thumbnail.get_attribute('src'))


        # # 수정중
        # product_imgs = driver.find_elements(By.CLASS_NAME, "wrap_editor")
        # product_imgs = product_imgs[0].find_elements(By.TAG_NAME,  'div')
        # product_imgs = product_imgs[0].find_elements(By.TAG_NAME,  'img')
        
        # for product_img in product_imgs:
        #     print(product_img.get_attribute('data-resize-src'))
        #     print(product_img.get_attribute('data-img-order'))

    
        # # 옵션 버튼을 처리
        option_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.btn_option')
        for index in range(len(option_buttons)):
            option_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.btn_option')  # 새로운 페이지에서 옵션 버튼 재찾기
            option_button = option_buttons[index]
            option_button.click()
            time.sleep(0.1)

            option_name = option_button.find_element(By.TAG_NAME, 'strong').text
            print(f"옵션 {index + 1}:", option_name)
            options_id=insert_option(option_name,product_id)
            # 옵션 상세 정보 처리
            clickable_details = []  # 클릭 가능한 옵션 상세를 저장할 리스트
            option_details = driver.find_elements(By.XPATH, f"//div[contains(@class, 'wrap_option')][{index + 1}]//ul/li")
            for detail_index, detail in enumerate(option_details):
                detail_label = detail.find_element(By.CLASS_NAME, 'lab_check').text
                # 옵션 상세 이름
                print(detail_label)
                
                # 품절 표시(span.txt_soldout)가 없는 옵션 상세를 리스트에 추가
                sold_out = detail.find_elements(By.CSS_SELECTOR, 'span.txt_soldout')
                if not sold_out:
                    clickable_details.append(detail)

            # 클릭 가능한 옵션 상세 중 하나를 선택하여 클릭
            if clickable_details:
                clickable_details[0].find_element(By.CLASS_NAME, 'inp_check').click()
                time.sleep(0.1)

  print('product count: ',count)
  driver.quit()
