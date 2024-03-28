import pymysql
import time
import requests

try:
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='qal,1',
        db='kakaofund_db',
        charset='utf8'
    )
    print("데이터베이스 연결 성공")
    
    # 커서 생성
    cur = conn.cursor()

except pymysql.MySQLError as e:
    print("데이터베이스 연결 실패:", e)

# mainCategory = {
#   '95' : '뷰티',
#   '96' : '패션',
#   '93' : '식품',
#   '94' : '리빙/도서',
#   '99' : '레저/스포츠',
#   '98' : '유아동/반려',
#   '97' : '디지털/가전',
# }

# subCategory = {
#     '95': {'177': '향수', '178': '바디', '179': '스킨케어', '181': '메이크업', '184': '헤어/미용', '182': '남성화장품'},
#     '96': {'167': '주얼리', '211': '파자마', '171': '브랜드 가방/지갑', '170': '브랜드의류', '172': '브랜드신발', '173': '언더웨어', '213': '디자이너 브랜드', '169': '브랜드잡화', '168': '브랜드시계'},
#     '93': {'203': '과일/견과/채소', '202': '축산/수산', '206': '쌀/반찬/김치', '204': '건강식품', '205': '다이어트/이너뷰티', '102': '가공/보양식', '320': '케이크', '103': '디저트', '101': '유제품/아이스크림', '188': '커피/차/음료', '207': '전통주'},
#     '94': {'110': '주방/수입주방', '111': '캔들디퓨저 인센스', '109': '식물/꽃배달', '185': '침구/패브릭', '113': '조명/무드등', '114': '인테리어', '115': '생필품', '116': '수납/생활', '112': '가구/DIY', '286': '팬시/문구/취미', '284': '도서/음반', '225': '명품리빙', '318': '리빙편집샵'},
#     '99': {'235': '글로벌 브랜드 본사', '118': '스포츠의류', '119': '스포츠슈즈', '120': '스포츠잡화', '124': '요가/헬스/수영', '122': '레저/캠핑', '121': '등산/아웃도어', '197': '차량용품', '312': '여행용품', '311': '차량용 방향제', '310': '골프선물', '123': '골프/테니스'},
#     '98': {'136': '신생아/베이비패션', '138': '키즈패션', '144': '임신/출산/육아', '139': '장난감/인형', '140': '캐릭터샵', '141': '유아교육/도서', '142': '기저귀/물티슈', '143': '분유/이유식/간식', '313': '강아지 간식/용품', '314': '고양이 간식/용품', '315': '기타 소동물용품'},
#     '97': {'222': '프리미엄 가전', '198': '케이스', '157': '모바일 액세서리', '156': '미니가전', '164': '건강용품/가전', '158': '디지털/음향기기', '163': '계절가전', '160': '생활가전', '159': '주방가전', '161': '미용가전', '290': '카메라'}
# }

# def getMainCategoryInfos():
#   for [mainId , mainTitle] in mainCategory.items():
#     # 부모 카테고리 아이디(string), 부모 카테고리 타이틀(string) 
#     print(mainId, mainTitle)
#     cur.execute("INSERT INTO `category` (category_id, `name`, created_at, updated_at, parent_id) VALUES (%s, %s, NOW(), NOW(), NULL);", (mainId, mainTitle))
#   conn.commit()

# def getSubCategoryInfos():
#   for [mainId, sub] in subCategory.items():
#     for [subId, subTitle] in sub.items():
#       # 부모 카테고리 아이디(string), 자식 카테고리 아이디(string), 자식 카테고리 타이틀(string) 
#       print(mainId, subId, subTitle)
#       cur.execute("INSERT INTO `category` (category_id, `name`, created_at, updated_at, parent_id) VALUES (%s, %s, NOW(), NOW(), %s);",(subId, subTitle,mainId))
#   conn.commit()
def getCategoryInfos():
  url = "https://gift.kakao.com/a/v1/display-category/BASIC/home"
  response = requests.get(url)
  time.sleep(0.01)
  if response.status_code == 200:
      data = response.json()
      categories = data.get('categories', [])
      for category_item in categories:
          category = category_item.get('category', {})
          print(f"Category ID: {category.get('id')}, Name: {category.get('name')}")
          cur.execute("INSERT INTO category (category_id, `name`, created_at, updated_at, parent_id) VALUES (%s, %s, NOW(), NOW(),NULL);",(category.get('id'), category.get('name')))
          
          sub_categories = category_item.get('subCategories', [])
          
          for sub_category in sub_categories:
            print(f"  SubCategory ID: {sub_category.get('id')}, Name: {sub_category.get('name')}, Parent ID: {category.get('id')}")
            cur.execute("INSERT INTO `category` (category_id, `name`, created_at, updated_at, parent_id) VALUES (%s, %s, NOW(), NOW(), %s);",(sub_category.get('id'), sub_category.get('name'),category.get('id')))
  else:
      print("Failed to retrieve data")
  conn.commit()
  conn.close()