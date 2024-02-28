## 초기 세팅

1. 크롬 드라이버 다운로드
   루트 파일에 있는 chromedriver.exe 파일은 윈도우 64 버전입니다.

2. 필요한 패키지 설치

   ```powershell
   pip install selenium
   pip install beautifulsoup4
   pip install pymysql
   ```

3. 데이터 베이스 연결
   데이터 베이스 연결이라고 주석처리 된 부분이 있을텐데 이 부분에 host, user, password, db 관련 정보들 넣어주시면됩니다.
   바로 코드 실행하면 데이터베이스 연결 실패로 오류날거에요
   그냥 프린트문만 확인하고 싶으시다면 데이터 베이스 관련 코드 주석하시고 돌려보시면 데이터 어떻게 찍히는지 확인 하실수 있습니다.
   `conn = pymysql.connect(host='127.0.0.1', user='root', password='0000', db='soloDB', charset='utf8')`

## 백엔드분들이 해주셔야 할 부분

`readBrandData.py` 파일과 `readBrandData.py` 파일을 보시면 `print`문이 있을텐데 그 부분이 필요한 데이터들을 문자열로 뽑아놓은거에요.
확인해 보시고 필요한 데이터인 부분들은 `쿼리문 작성` 이라고 되어있는 주석 참고하셔서 `insert` 해주시면 됩니다.
`cur.execute()` 함수 내부에 예시로 몇 개 적어놨으니 참고해주세요!
중간에 `select` 해주셔야 할 부분도 있으니 주석 확인 부탁드려요!
추가로 필요한 정보가 있으시다면 멘션 주세요! 수정해서 푸시하겠습니다.
