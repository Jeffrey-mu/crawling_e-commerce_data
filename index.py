import json
import requests
import time
import time
import random
import csv
from bs4 import BeautifulSoup
from db import execute_query, execute_insert
# https://cd.jd.com/recommend?callback=handleComboCallback&methods=accessories&p=103003&sku=xxxxxx&cat=670%2C671%2C673&lid=1&uuid=16840284928081471928824&pin=jd_4be2a6b043e8e&ck=pin%2CipLocation%2Catw%2Caview&lim=5&cuuid=16840284928081471928824&csid=122270672.8.16840284928081471928824%7C2.1684050176&_=1684050222579

types = ['电脑']

def get_goods_info():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Cookie': '__jdv=76161171|direct|-|none|-|1684028492808; __jdu=16840284928081471928824; areaId=1; PCSYCityID=CN_110000_110100_0; shshshfpa=8498cfd5-bde9-6448-4b4a-4ecdf214646c-1684028494; shshshfpx=8498cfd5-bde9-6448-4b4a-4ecdf214646c-1684028494; shshshfpb=lB1z_CazuYIRbMMJUYMscQg; TrackID=12OrxpC0FefkI8ux_VzaFDnNr60KjbHRRPBCOnLp2PbRv5-v6rsWwoVq_otRPvyY53ksd5ttyGDcKiJnqR7d0tYrXjZdn-TFDqcJC1KWG9yowpcJrYOU2VfAhgmEXbqbf; flash=2_BdrgoJwM3DXQcBMmBYtxNqtdxPKxBtZwRAsdyYpObE3zwy4Kbcr6_RfJnbRugaD4hQO3Cz8kw2AU07SuMQtUmuZW5N-WWMfUbYzpAxpMs0D*; pinId=WjYHIpHkMCvY1q6CDOJDhrV9-x-f3wj7; pin=jd_4be2a6b043e8e; unick=%E4%BA%8C%E7%8B%97%E5%AD%90%E7%9A%84%E4%BC%9F%E5%A4%A7%E5%A4%8D%E5%85%B4; ceshi3.com=103; _tp=wpGdEbqXvtPL3qwAweA%2F1uspT36tXjVUJ%2FziK2P0mHQ%3D; _pst=jd_4be2a6b043e8e; user-key=8b95cd14-d17c-421d-ac03-5e505526ac0a; cn=10; thor=9CC505825F98C118013CDEBA600C8B61B51E691F135784C8270F4471CD993C334508DC7B67A1E9FB6D848221C248E04AFFBA5621A2CBE0CD8BAFFEC361D96B489E1263DF520F65BBDF04F9ED219F01DEAF9ED84DFFF70CF67ED31F5B1470FF38CE3B75A43BAB739285548C732376EE83811DBD5365E139817CBD117F3BF3ABC1D5BB3C9B2F45F87A28389F1E36A5681A825C87122EE377FFD9C720D4053B2470; 3AB9D23F7A4B3CSS=jdd03TNIIBNFLFWNQ4WX4XMPQWD7FRSCY7HNUVWFEOJJJH5LC4QOKVMBNIN7POPGVNDGVTKW5GE2H6RHBUKT7HA7SCJB5OQAAAAMIC73UPCIAAAAACH7XLIJDNFQ4EEX; _gia_d=1; jsavif=1; __jda=122270672.16840284928081471928824.1684028493.1684028493.1684028493.1; __jdc=122270672; shshshsID=754b51afc1484b4544f2d8bd67e7d7d7_5_1684029269980; 3AB9D23F7A4B3C9B=TNIIBNFLFWNQ4WX4XMPQWD7FRSCY7HNUVWFEOJJJH5LC4QOKVMBNIN7POPGVNDGVTKW5GE2H6RHBUKT7HA7SCJB5OQ; token=0219a9c46aa3c0284bfc0a8d0dfb1f20,3,935571; __tk=56d0bdb787078f1cf854dc7d1bb1839a,3,935571; __jdb=122270672.9.16840284928081471928824|1.1684028493; jsavif=1; ipLoc-djd=1-2805-55650-0'
    }

    def job(number):
        sleep_time = random.uniform(0, 2)
        time.sleep(sleep_time)
        url = f"https://item.jd.com/{number[0]}.html"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        color = ''
        if len(soup.select('#choose-attr-1 .selected')) > 0:
            color = soup.select(
                '#choose-attr-1 .selected')[0]['data-value']
        color2 = ''
        if len(soup.select('#choose-attr-2 .selected')) > 0:
            color2 = soup.select(
                '#choose-attr-2 .selected')[0]['data-value']
        img = ''
        if len(soup.select('#spec-n1 #spec-img')) > 0:
            img = soup.select('#spec-n1 #spec-img')[0]
            img = img['data-origin']
        brand = ''
        if len(soup.select('#parameter-brand li')) > 0:
            brand = soup.select('#parameter-brand li')[0]
            brand = brand['title']

        product_list = soup.find_all(class_='parameter2')
        info = ""
        for product in product_list:
            li_elements = product.find_all('li')
            for li in li_elements:
                info += li.text + '&'
        print(
            f"{number[0]},{number[1]},{info},http:{img},{color},{color2},{brand}")
        with open(f'./data/goods_numbers{type}.csv', 'a+', encoding='utf-8') as f:
            f.write(f"{number[0]},{number[1]},{info},http:{img},{color},{color2},{brand}".replace(
                '\n', '') + '\n')

    for type in types:
        with open(f'./id/{type}.csv', 'r') as f:
            reader = csv.reader(f)
            # 将数据转换为列表
            numbers = list(reader)
            for number in numbers:
                try:
                    job(number)
                except ZeroDivisionError as e:
                    continue


def get_goods_coom():
    # result = execute_query('SELECT * FROM goods')
    with open('./id/2电脑.csv', newline='') as csvfile:
        result = csv.DictReader(csvfile)
        for item in result:
            print(item)
            for page in range(20):
                try:
                    url = f'https://sclub.jd.com/comment/productPageComments.action'
                    params = {
                        'productId': item['g_number'],
                        'functionId': 'pc_club_productPageComments',
                        'page': page,
                        'pageSize': 10,
                        'score': 0,
                        'sortType': 5,
                        'isShadowSku': 0,
                        'fold': 1
                    }

                    response = requests.post(url, params=params)
                    data = response.json()
                    comments = data['comments']
                    for comment in comments:
                        content = comment['content']
                        score = comment['score']
                        productSize = comment['productSize']
                        productColor = comment['productColor']
                        nickname = comment['nickname']
                        # sql = "INSERT INTO comment (c_number, c_comment, c_size, c_color, c_score, c_nickname) VALUES (%s, %s, %s, %s, %s, %s)"
                        # val = (int(item['g_number']), content, productSize, productColor, score, nickname)
                        val = f"{int(item['g_number'])},{content},{productSize},{productColor},{score},{nickname}"
                        with open(f'./comment/电脑.csv', 'a+', encoding='utf-8') as f:
                            f.write(val.replace('\n', '') + '\n')
                        # execute_insert(sql, val)
                except Exception as e:
                    break

def get_goods_numbers():
    for type in types:
        list_numbers = list()
        list_numbers.append(f"商品编号,价格")
        # urls = f'https://search.jd.com/Search?keyword={search_term}&wq={search_term}&pvid=65fab5df23b244b49632e0a1c23adc4e&psort=3&click=0'
        for index in range(100):
            print(index)
            urls = f'https://search.jd.com/Search?keyword={type}&wq={type}&pvid=65fab5df23b244b49632e0a1c23adc4e&click=0&page={index + 1}'
            response = requests.get(urls)
            soup = BeautifulSoup(response.text, 'html.parser')
            product_list = soup.find_all(id='J_goodsList')
            for product in product_list:
                li_elements = product.find_all(class_='gl-item')

                for li in li_elements:
                    p = li.select('.gl-i-wrap .p-price i')
                    list_numbers.append(f"{li['data-sku']},{p[0].text}")
                    print(f"{index}/{li['data-sku']},{p[0].text}")
        with open(f'./id/{type}.csv', 'a+', encoding='utf-8') as f:
            for l in list_numbers:
                f.write(l.replace('\n', '') + '\n')


get_goods_coom()
