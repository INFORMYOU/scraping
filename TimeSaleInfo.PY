#Step 0. 필요한 모듈과 라이브러리를 로딩합니다.
import requests # Python에서 HTTP 요청을 보내는 모듈
from bs4 import BeautifulSoup # 데이터 파싱
import re

#Step 1. 네이버 hotDeal page html data 가져오기
url = 'https://shopping.naver.com/hotdeal/p/index.nhn'
req = requests.get(url)
html = req.text


#Step 2. 네이버 서버 시간 가져오기
request_headers = {
    'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'),
}
response = requests.get(url, headers=request_headers)
date = response.headers['date'][:-4]


#Step 3. timesale section 정보만 가져오기
soup = BeautifulSoup(html, 'html.parser')
timesale_info = soup.find("div", {"id": "timesale_wrap"})


#Step 4. 현재 진행중인 Deal의 필요정보 추출
deal_num = len(timesale_info.find_all('span', class_="time_info last"))
# print(deal_num)

for i in range(deal_num):
    title = timesale_info.find_all('p', class_="dsc")[i].get_text().strip()
    price = timesale_info.find_all('strong')[i].get_text().strip()[:-1].replace(",","")
    views = timesale_info.find_all('em', class_="cnt")[i].get_text().strip().replace(",","")

    try : 
        url = re.search(r"https://smartstore.naver.com/main/products/\d+",str(timesale_info.find_all('a')[i])).group()
    except : 
        url = re.search(r"https://shopping.naver.com/outlink/itemdetail/\d+",str(timesale_info.find_all('a')[i])).group()

    # print(date)
    # print(title)
    # print(price)
    # print(views)
    print(url)
    # print("========================================")