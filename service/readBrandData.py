## https://googlechromelabs.github.io/chrome-for-testing/#stable
from selenium import webdriver
from bs4 import BeautifulSoup
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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

# 카테고리 정보
CATEGORY = {
  '95' : ['178','179'], # 뷰티
  '96' : ['211','212','170'], # 패션
  '93' : ['101', '207'], # 식품
  '94' : ['113','286','318'], # 리빙/도서
  '99' : ['120','312'], # 레저/스포츠
  '98' : ['226', '314'], # 유아동/반려
  '97' : ['222', '160']  # 디지털/가전
}

def getCategoryUrls():
  URLS = []

  for main in CATEGORY:
    for sub in CATEGORY[main]:
      url = "https://gift.kakao.com/brand/category/{}/subcategory/{}".format(main, sub)
      URLS.append(url)

  return URLS


def getBrandInfos():
  brandInfos = {}
  urls = getCategoryUrls()

  for url in urls :
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
  
    brandSoup = soup.select('a.link_brand')

    brands = []
    for i in brandSoup:
      href = i.get('href')
      brandId = href.split("/brand/")[1]
      img = i.select('img')[0]
      brandName = img.get('alt')
      brandImg = img.get('src')
    
      print("brandId : ", brandId)
      print("brandName : ", brandName)
      print("brandImg : ", brandImg)
      brandCategoryId = url.split('/')
      print("brandMainCategoryId, brandSubCategoryId : ", brandCategoryId[5], brandCategoryId[7])

      # 쿼리문 작성
      # 예시
      cur.execute("INSERT INTO tablename (컬럼이름) VLAUES (%s)", (brandId))

      brand = {'brandId' : brandId, 'brandName' : brandName, 'brandImg' : brandImg, 'brandCategory' : url}
      brands.append(brand)
      
    brandInfos[url] = brands
  
  conn.commit()
  conn.close()

  driver.quit()

  return brandInfos