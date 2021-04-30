import pymysql

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

    #Step 3.get url info
    sql = 'select url from views_tb order by time desc limit 10;'
    curs.execute(sql)
    duplicated_urls = curs.fetchall()

    urls = []
    for url in duplicated_urls:
        if url not in urls:
            urls.append(url)

    #Step 4. close connection
    conn.close()

    return get_detailDealInfo(urls)


def get_detailDealInfo(urls):

    
    print(urls)
    print(type(urls))


if __name__ == "__main__":
    
    read_url()