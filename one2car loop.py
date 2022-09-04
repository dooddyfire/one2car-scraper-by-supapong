import datetime
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
#Fix
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import requests 
from bs4 import BeautifulSoup 
import json

start_page = int(input("หน้าแรก : "))
end_page = int(input("หน้าสุดท้าย : "))

output_file = input("Output File : ")
driver = webdriver.Chrome(ChromeDriverManager().install())



car_name_lis = []
car_brand_lis = []
car_model_lis = []
car_url_lis = []
car_loc_lis = []
car_price_lis = []
car_hand_lis = []
car_mile_lis = []
car_gear_lis = []
car_max_mile_lis = []
car_min_mile_lis = []

for i in range(start_page,end_page+1):
  url = 'https://www.one2car.com/%E0%B8%A3%E0%B8%96-%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A-%E0%B8%82%E0%B8%B2%E0%B8%A2?page_size={}'.format(i)

  res = requests.get(url)
  soup = BeautifulSoup(res.content,'html.parser')
  res2 = soup.find_all('script')[2]
  print(res2.contents[0])
  print()
  json_object = json.loads(res2.contents[0])
  print(json_object)

  for i in json_object[1]['itemListElement']:

    item_url = i['item']['mainEntityOfPage'] 
    print(item_url)
    driver.get(item_url)



    soupx = BeautifulSoup(driver.page_source,'html.parser')
    owl_item = [ d.text for d in soupx.find_all('div',{'class':'owl-item'})]
    print(owl_item)
    car_hand = owl_item[0].strip().replace("สภาพ","").strip()
    car_mile = owl_item[2].strip().replace("เลขไมล์ (กม.)","").strip()
    car_gear = owl_item[5].strip().replace("ระบบเกียร์","").strip()
    try:
      car_max_mile = car_mile.split("-")[1]
      car_min_mile = car_mile.split("-")[0]
    except: 
      car_max_mile = " "
      car_min_mile = car_mile

    car_max_mile_lis.append(car_max_mile)
    car_min_mile_lis.append(car_min_mile)
    print(car_max_mile)
    print(car_min_mile)

    print(car_hand)
    print(car_mile)
    print(car_gear)

    car_hand_lis.append(car_hand)
    car_mile_lis.append(car_mile)
    car_gear_lis.append(car_gear)

    print(i['item'])
    car_brand = i['item']['brand']
    car_brand_lis.append(car_brand)
    car_model = i['item']['model'] 
    car_model_lis.append(car_model)
    car_name = i['item']['name']
    car_name_lis.append(car_name)
    car_url = i['item']['mainEntityOfPage']
    car_url_lis.append(car_url)
    car_loc = i['item']['offers']['seller']['homeLocation']['address']
    car_loc_lis.append(car_loc)
    car_price = i['item']['offers']['price']
    car_price_lis.append(car_price)
    print(car_brand)
    print(car_model) 
    print(car_name)
    print(car_url)
    print(car_loc)
    print(car_price)



driver.close()

df = pd.DataFrame()
df['ชื่อรถ'] = car_name_lis 
df['ปี'] = [ y[:4] for y in car_name_lis]
df['Brand'] = car_brand_lis
df['Model'] = car_model_lis 
df['Link'] = car_url_lis 
df['Location'] = car_loc_lis 
df['Price'] = car_price_lis
df['จำนวนไมล์'] = car_mile_lis 
df['จำนวนไมล์ต่ำสุด'] = car_min_mile_lis
df['จำนวนไมล์สูงสุด'] = car_max_mile_lis


df['ระบบเกียร์'] = car_gear_lis 
df['มือ'] = car_hand_lis
df.to_excel("{}.xlsx".format(output_file))
