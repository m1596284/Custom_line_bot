# -*- coding: UTF-8 -*-
import datetime
from pathlib import Path
from sqlite_CRUD import Database
from time import sleep
import requests
from bs4 import BeautifulSoup, element
import re
from lxml import etree
from py_logging import py_logger, close_log, remove_old_log

base_dir = Path(__file__).parent.parent
py_name = Path(__file__).stem

def collect_hometown():
    db_path = f"{base_dir}/db.sqlite3"
    db = Database(db_path = f"{db_path}")
    table = "IU_line_bot_hometown_day_info_table"
    db.use_table(table)
    header_hometown = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",}
    main_url= "https://072727770.weebly.com/"
    r = requests.get(url=main_url, headers=header_hometown)
    soup = BeautifulSoup(r.text, 'html.parser')
    working_shift_num = soup.find_all('div',class_="wsite-section-elements")
    working_shift = working_shift_num[1].find('div', class_="paragraph")
    working_shift_num_list = []
    hometown_day_info_text = ""
    for thing in working_shift:
        if type(thing) == element.NavigableString:
            temp_text = str(thing).replace("\u200b","")+"\n"
            hometown_day_info_text =f"{hometown_day_info_text}{temp_text}"
            working_shift_num_list.append(str(thing).replace("\u200b",""))
    db.update(id=0,day_info=hometown_day_info_text)

    table = "IU_line_bot_hometown_info_table"
    db.use_table(table)
    db.delete_all()
    main_page = etree.HTML(r.text)
    day_page = main_page.xpath('//*[@id="wsite-content"]/div[1]/div/div/div/div/div/strong[1]/font/a[1]')[0].get('href')
    noon_page = main_page.xpath('//*[@id="wsite-content"]/div[1]/div/div/div/div/div/strong[1]/font/a[3]')[0].get('href')
    night_page = main_page.xpath('//*[@id="wsite-content"]/div[1]/div/div/div/div/div/strong[1]/font/a[5]')[0].get('href')
    new_page = main_page.xpath('//*[@id="wsite-content"]/div[1]/div/div/div/div/div/strong[2]/font/strong/font/a')[0].get('href')
    shift_page_url = []
    shift_page_url.append(day_page)
    shift_page_url.append(noon_page)
    shift_page_url.append(night_page)
    shift_page_url.append(new_page)
    for num, url in enumerate(shift_page_url):
        if url.find("https://072727770.weebly.com") == -1:
            shift_page_url[num] = f"https://072727770.weebly.com{url}"
    for num, shift_page in enumerate(shift_page_url):
        if num == 0:
            shift = "早班"
        elif num ==1:
            shift = "中班"
        elif num ==2:
            shift = "晚班"
        else:
            shift = "新進"
        r = requests.get(url=shift_page)
        sub_page = etree.HTML(r.text)
        img_xpath = sub_page.xpath('//img[@src]')
        img_list = []
        for thing in img_xpath:
            img_list.append(thing.get('src'))
        img_list = img_list[2:]
        soup = BeautifulSoup(r.text,'html.parser')
        strr = re.sub('[A-Za-z]', "", str(soup))
        strr = re.sub('[,<>/="#:;🔻_]', "", strr)
        card_count = strr.count("美容師：")
        card_list = []
        start = 0
        for item in range(card_count):
            card_list.append(strr[strr.find("美容師：",start):strr.find("\n",strr.find("美容師：",start))].replace("\u200b",""))
            start = strr.find("美容師：",start)+4
        for num, item in enumerate(card_list):
            id_num = item[item.find("美容師")+4:item.find("上班時段")].replace("233","").replace(" ","")
            working_time = item[item.find("上班時段")+5:item.find("身體密碼")].replace("233","").replace("5","").replace(" ","")
            body_language = item[item.find("身體密碼")+5:item.find("身體密碼")+10]
            body_language = f"{body_language[:3]}/{body_language[3:]}"
            introduction = re.sub('[0-9]', "", item[item.find("身體密碼")+10:]).replace(" ","").replace("()","")
            url = f"https://072727770.weebly.com{img_list[num]}"
            id_num = id_num
            time = "None"
            working = working_time
            body = body_language
            info = introduction
            log.info(f"{id_num}: {body_language}")
            db.create(url=url,shift=shift,id_num=id_num,time=time,working=working,body=body,info=info)
    db.close()

if __name__ == "__main__":
    start_hour = 6
    start_min = 0
    while True:
        now = datetime.datetime.now()
        remove_old_log(log_path=f"{base_dir}/log",file_name=py_name)
        log = py_logger("w",level="INFO",log_path=f"{base_dir}/log",file_name="hometown")
        log.info(f"{Path(__file__)}")
        if now.hour == start_hour and now.minute == start_min:
            collect_hometown()
        close_log(log)
        sleep(60)
