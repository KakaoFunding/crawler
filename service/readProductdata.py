## https://googlechromelabs.github.io/chrome-for-testing/#stable
from selenium import webdriver
from bs4 import BeautifulSoup
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import pymysql

# 데이터베이스 연결
conn = pymysql.connect(host='127.0.0.1', user='root', password='0000', db='soloDB', charset='utf8')
cur = conn.cursor()

##Chrome WebDriver 경로 설정
webdriver_path = './chromedriver.exe'

##Selenium 브라우저 옵션 설정
options = Options()
options.headless = True  # 브라우저 창을 띄우지 않고 실행

# Selenium WebDriver 설정
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=options)


def getProductInfo():

  # 쿼리문 작성
  # 브랜드 아이디만 빼오는 쿼리문
  # brand_Ids = ()'12345', '12345') 이런식으로 데이터 뽑아져야됨
  cur.execute("SELECT brandId FROM tablename")
  brand_Ids = cur.fetchall()

  for brand_Id in brand_Ids :
    url = f"https://gift.kakao.com/brand/{brand_Id}"
    driver.get(url)
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 상품 링크 불변객체 생성
    product_urls = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, 'a[href*="/product/"]')]

    # 상품 URL 리스트를 순회
    for product_url in product_urls:
        driver.get(product_url)
        time.sleep(1)


        # 쿼리문 작성
        # 예시
        print("상품 ID:", product_url.split('/product/')[1])
        cur.execute("INSERT INTO tablename (컬럼이름) VLAUES (%s)", (product_url.split('/product/')[1]))

        title = driver.find_element(By.CSS_SELECTOR, 'h2.tit_subject').text
        
        print("타이틀:", title)

        if price_elements := driver.find_elements(By.CLASS_NAME, 'price_area'):
            print("가격:", price_elements[0].text)

        # 썸네일
        thumbnail_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.nav_photo img')
        for thumbnail in thumbnail_elements:
            print("썸네일 URL: " + thumbnail.get_attribute('src'))

        # 옵션 버튼을 처리
        option_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.btn_option')
        for index in range(len(option_buttons)):
            option_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.btn_option')  # 새로운 페이지에서 옵션 버튼 재찾기
            option_button = option_buttons[index]
            option_button.click()
            time.sleep(0.1)

            option_name = option_button.find_element(By.TAG_NAME, 'strong').text
            print(f"옵션 {index + 1}:", option_name)

            # 옵션 상세 정보 처리
            clickable_details = []  # 클릭 가능한 옵션 상세를 저장할 리스트
            option_details = driver.find_elements(By.XPATH, f"//div[contains(@class, 'wrap_option')][{index + 1}]//ul/li")
            for detail_index, detail in enumerate(option_details):
                detail_label = detail.find_element(By.CLASS_NAME, 'lab_check').text
                print(detail_label)
                
                # 품절 표시(span.txt_soldout)가 없는 옵션 상세를 리스트에 추가
                sold_out = detail.find_elements(By.CSS_SELECTOR, 'span.txt_soldout')
                if not sold_out:
                    clickable_details.append(detail)

            # 클릭 가능한 옵션 상세 중 하나를 선택하여 클릭
            if clickable_details:
                clickable_details[0].find_element(By.CLASS_NAME, 'inp_check').click()
                time.sleep(0.1)

  conn.commit()
  conn.close()

  driver.quit()