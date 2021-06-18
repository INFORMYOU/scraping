#Step 0. 필요한 모듈과 라이브러리를 로딩합니다.
import pymysql
import requests # Python에서 HTTP 요청을 보내는 모듈
from bs4 import BeautifulSoup # 데이터 파싱
import time
import math

# get url addresses of recent deals from the views_tb table.
def read_url():

    #Step 1. connection information
    conn = pymysql.connect(
        host = 'localhost', 
        user = 'root', 
        password = 'root1234',
        db = 'naver_hotdeal', 
        charset ='utf8'
    )

    #Step 2. create cursor
    curs = conn.cursor()

    #Step 3.get recent deal's url list
    sql = 'select url from views_tb order by time desc limit 20;'
    curs.execute(sql)
    duplicated_urls = curs.fetchall()

    urls = []
    for url in duplicated_urls:
        if url not in urls:
            urls.append(url)

    #Step 4. close connection
    conn.close()

    # #Step 5. get each deal address
    for i in urls :
        url = str(i)[2:-3]
        get_detailDealInfo(url)


# get each deal's detail info
def get_detailDealInfo(URL) :
    
    #Step 1. 각 딜의 html data 가져오기
    req = requests.get(URL)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    #Step 2. 각 딜의 필요정보 추출
    
    # 기본 상품 정보
    title  = soup.find('div', class_='CxNYUPvHfB').get_text()
    thumbnail = soup.find('img', class_='_2P2SMyOjl6')['data-src']
    discount_rate = soup.find('span', class_='_1G-IvlyANt').get_text()[0:-3]
    original_price = soup.find_all('span', class_='_1LY7DqCnwR')[0].get_text().replace(",","")
    sale_price = soup.find_all('span', class_='_1LY7DqCnwR')[1].get_text().replace(",","")
    delivery = soup.find('div', class_='pTaPzv0i6H').get_text().replace('택배배송', '택배배송 ')
    try :
        delivery_condition = soup.find('p', class_='_1JN0qDXZim').get_text()
    except :
        delivery_condition = 'No Condition'
    
    # 리뷰
    num_reviews = soup.find_all('strong', class_='_2pgHN-ntx6')[0].get_text().replace(",","")
    review_greade = soup.find_all('strong', class_='_2pgHN-ntx6')[1].get_text()[0:-2]

    detail_info = [title, thumbnail, discount_rate, original_price, sale_price, delivery, delivery_condition, num_reviews, review_greade]

    return insert_data(detail_info)


def insert_data(detail_info):
 
    #Step 1. connection information
    conn = pymysql.connect(
        host = 'localhost', 
        user = 'root', 
        password = 'root1234',
        db = 'naver_hotdeal', 
        charset ='utf8'
    )

    #Step 2. create cursor
    curs = conn.cursor()

    #Step 3. create sql and commit
    sql = "INSERT INTO detailInfo_tb VALUES('"  + detail_info[0] + "','" + detail_info[1] + "','" + detail_info[2] + "','" + detail_info[3] + "','" + detail_info[4] + "','" + detail_info[5] + "','" + detail_info[6] + "','" +  detail_info[7] +  "','" + detail_info[8]+ "');"
    print(sql)
    print("====================")
    curs.execute(sql)
    conn.commit()
    
    #Step 4. close connection
    conn.close()


if __name__ == "__main__":
    
    read_url()