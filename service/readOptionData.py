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

def get_product_ids():
    cur.execute("SELECT product_id FROM product")
    ids=cur.fetchall()
    return  [int(item[0]) for item in ids]

def insert_option(name, product_id):
    try:
        cur.execute("INSERT INTO options (created_at, updated_at, name, product_id) VALUES (NOW(), NOW(), %s, %s)", (name, product_id))
        conn.commit()
        inserted_id = cur.lastrowid
        print(f"Option of {product_id} inserted successfully with ID {inserted_id}.")
        return inserted_id
    except pymysql.MySQLError as e:
        print(f"Failed to insert option for product ID {product_id}: {e}")
        conn.rollback()
        return None

def insert_option_detail(option_name, option_id):
    try:
        cur.execute("INSERT INTO option_detail (created_at, updated_at, name, option_id) VALUES (NOW(), NOW(), %s, %s)", (option_name, option_id))
        conn.commit()
        print(f"Option detail of {option_id} inserted successfully.")
    except pymysql.MySQLError as e:
        print(f"Failed to insert option detail for option ID {option_id}: {e}")
        conn.rollback()

    

def getOptionInfos():
    try:
        for product_id in get_product_ids():
            print(f"Product ID:{product_id}")
            url=f"https://gift.kakao.com/a/product-detail/v1/products/{product_id}/options"
            response = session.get(url,timeout=5)
            data = response.json()
            if(data.get('type')=='COMBINATION'):
                names=data.get('names',[])
                combination_options=data.get('combinationOptions',[])
                option_ids = {}
                for name in names:
                    option_id = insert_option(name, product_id)
                    option_ids[name] = option_id
                    
                for option in combination_options:
                    key = option.get('key')
                    value = option.get('value')
                    if key in option_ids:
                        insert_option_detail(value, option_ids[key])
                print('Insertion of option finished')
    except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            
            