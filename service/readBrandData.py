## https://googlechromelabs.github.io/chrome-for-testing/#stable
from selenium import webdriver
from bs4 import BeautifulSoup
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import pymysql

# # 데이터베이스 연결
# conn = pymysql.connect(host='127.0.0.1', user='root', password='0000', db='soloDB', charset='utf8')
# cur = conn.cursor()


##Chrome WebDriver 경로 설정
webdriver_path = './chromedriver.exe'

##Selenium 브라우저 옵션 설정
options = Options()
options.headless = True  # 브라우저 창을 띄우지 않고 실행

# Selenium WebDriver 설정
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=options)

mainCategory = {
  '95' : '뷰티',
  '96' : '패션',
  '93' : '식품',
  '94' : '리빙/도서',
  '99' : '레저/스포츠',
  '98' : '유아동/반려',
  '97' : '디지털/가전',
}

subCategory = {
    '95': {'177': '향수', '178': '바디', '179': '스킨케어', '181': '메이크업', '184': '헤어/미용', '182': '남성화장품'},
    '96': {'167': '주얼리', '211': '파자마', '171': '브랜드 가방/지갑', '170': '브랜드의류', '172': '브랜드신발', '173': '언더웨어', '213': '디자이너 브랜드', '169': '브랜드잡화', '168': '브랜드시계'},
    '93': {'203': '과일/견과/채소', '202': '축산/수산', '206': '쌀/반찬/김치', '204': '건강식품', '205': '다이어트/이너뷰티', '102': '가공/보양식', '320': '케이크', '103': '디저트', '101': '유제품/아이스크림', '188': '커피/차/음료', '207': '전통주'},
    '94': {'110': '주방/수입주방', '111': '캔들디퓨저 인센스', '109': '식물/꽃배달', '185': '침구/패브릭', '113': '조명/무드등', '114': '인테리어', '115': '생필품', '116': '수납/생활', '112': '가구/DIY', '286': '팬시/문구/취미', '284': '도서/음반', '225': '명품리빙', '318': '리빙편집샵'},
    '99': {'235': '글로벌 브랜드 본사', '118': '스포츠의류', '119': '스포츠슈즈', '120': '스포츠잡화', '124': '요가/헬스/수영', '122': '레저/캠핑', '121': '등산/아웃도어', '197': '차량용품', '312': '여행용품', '311': '차량용 방향제', '310': '골프선물', '123': '골프/테니스'},
    '98': {'136': '신생아/베이비패션', '138': '키즈패션', '144': '임신/출산/육아', '139': '장난감/인형', '140': '캐릭터샵', '141': '유아교육/도서', '142': '기저귀/물티슈', '143': '분유/이유식/간식', '313': '강아지 간식/용품', '314': '고양이 간식/용품', '315': '기타 소동물용품'},
    '97': {'222': '프리미엄 가전', '198': '케이스', '157': '모바일 액세서리', '156': '미니가전', '164': '건강용품/가전', '158': '디지털/음향기기', '163': '계절가전', '160': '생활가전', '159': '주방가전', '161': '미용가전', '290': '카메라'}
}


# 카테고리 정보
CATEGORY = {
  # 뷰티
  # 향수 | 바디 | 스킨케어 | 메이크업 | 헤어/미용 | 남성화장품
  '95' : ['177', '178', '179', '181', '184', '182'],
  # 패션
  # 주얼리 | 파자마 | 브랜드 가방/지갑 | 브랜드의류 | 브랜드신발 | 언더웨어 | 디자이너 브랜드 | 브랜드잡화 | 브랜드시계
  '96' : ['167', '211', '171', '170', '172', '173', '213', '169', '168'],
  # 식품
  # 과일/견과/채소 | 축산/수산 | 쌀/반찬/김치 | 건강식품 | 다이어트/이너뷰티 | 가공/보양식 | 케이크 | 디저트 | 유제품/아이스크림 | 커피/차/음료 | 전통주 
  '93' : ['203', '202', '206', '204', '205', '102', '320', '103', '101', '188', '207'],
  # 리빙/도서
  # 주방/수입주방 | 캔들디퓨저 인센스 | 식물/꽃배달 | 침구/패브릭 | 조명/무드등 | 인테리어 | 생필품 | 수납/생활 | 가구/DIY | 팬시/문구/취미 | 도서/음반 | 명품리빙 | 리빙편집샵
  '94' : ['110', '111', '109', '185', '113', '114', '115', '116', '112', '286', '284', '225', '318'], 
  # 레저/스포츠
  # 글로벌 브랜드 본사 | 스포츠의류 | 스포츠슈즈 | 스포츠잡화 | 요가/헬스/수영 | 레저/캠핑 | 등산/아웃도어 | 차량용품 | 여행용품 | 차량용 방향제 | 골프선물 | 골프/테니스
  '99' : ['235', '118', '119', '120', '124', '122', '121', '197', '312', '311', '310', '123'],
  # 유아동/반려
  # 신생아/베이비패션 | 키즈패션 | 임신/출산/육아 | 장난감/인형 | 캐릭터샵 | 유아교육/도서 | 기저귀/물티슈 | 분유/이유식/간식 | 강아지 간식/용품 | 고양이 간식/용품 | 기타 소동물용품
  '98' : ['136', '138', '144', '139', '140', '141', '142', '143', '313', '314', '315'],
  # 디지털/가전
  # 프리미엄 가전 | 케이스 | 모바일 액세서리 | 미니가전 | 건강용품/가전 | 디지털/음향기기 | 계절가전 | 생활가전 | 주방가전 | 미용가전 | 카메라
  '97' : ['222', '198', '157', '156', '164', '158', '163', '160', '159', '161', '290']
}

def getCategoryUrls():
  URLS = []

  for main in CATEGORY:
    print(main)
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