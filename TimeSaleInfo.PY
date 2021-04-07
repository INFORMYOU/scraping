#Step 0. 필요한 모듈과 라이브러리를 로딩합니다.
import requests # Python에서 HTTP 요청을 보내는 모듈
from bs4 import BeautifulSoup # 데이터 파싱
import re
import datetime
import time
import pymysql



def get_timeSaleInfo():

    #Step 1. 네이버 hotDeal page html data 가져오기
    url = 'https://shopping.naver.com/hotdeal/p/index.nhn'
    req = requests.get(url)
    html = req.text

    #Step 2. timesale section 정보만 가져오기
    soup = BeautifulSoup(html, 'html.parser')
    timesale_info = soup.find("div", {"id": "timesale_wrap"})

    #Step 3. 현재 진행중인 Deal의 필요정보 추출
    deal_num = len(timesale_info.find_all('span', class_="time_info last"))
    
    products = []
    for i in range(deal_num):
        title = timesale_info.find_all('p', class_="dsc")[i].get_text().strip()
        price = timesale_info.find_all('strong')[i].get_text().strip()[:-1].replace(",","")
        views = timesale_info.find_all('em', class_="cnt")[i].get_text().strip().replace(",","")
        try : 
            url = re.search(r"https://smartstore.naver.com/main/products/\d+",str(timesale_info.find_all('a')[i])).group()
        except : 
            url = re.search(r"https://shopping.naver.com/outlink/itemdetail/\d+",str(timesale_info.find_all('a')[i])).group()

        product = [now, title, price, views, url]
        products.append(product)
    
    return insert_data(products)



def insert_data(products_info):

    # connection information
    conn = pymysql.connect(
        host = 'localhost', 
        user = 'root', 
        password = 'root1234',
        db = 'naver_hotdeal', 
        charset ='utf8'
    )

    # create cursor
    curs = conn.cursor()

    # create sql and commit
    for product in products_info:
        sql = "INSERT INTO views_tb VALUES('"  + product[0] + "','" + product[1] + "','" + product[2] + "','" + product[3] + "','" + product[4] + "');"
        print(sql)
        print("====================")
        curs.execute(sql)
        conn.commit()
    
    # close connection
    conn.close()



if __name__ == "__main__":

    while True:
        now = str(datetime.datetime.now())[0:-7]
 
        if now[-12:-10] in ['00', '15', '30', '45']:
            get_timeSaleInfo()

        time.sleep(898)

        # # test용
        # if now[-5:-3] in ['22', '24']:
        #     get_timeSaleInfo()

        # time.sleep(60)