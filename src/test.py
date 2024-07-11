# -*- coding: utf-8 -*-
import time
from time import sleep
import datetime
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from py_logging import py_logger,close_log, remove_old_log
from sqlite_CRUD import Database
from lxml import etree
from pytube import YouTube
import re

# set path and name
base_dir = Path(__file__).parent
here_dir = Path(__file__).parent
py_name = Path(__file__).stem
start_hour = 3
start_min = 30
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
}
def collect():
    ## set Database
    db_path = f"{base_dir}/db.sqlite3"
    db = Database(db_path = f"{db_path}")
    table = "IU_line_bot_shopback_table"
    title_type_dict = {
        "id":"integer",
        "name":"text",
        "shopId":"integer",
        "point":"real",
        "url":"text",
        "image_url":"text",
        "transfer_Url":"text",
    }
    db.create_table(table,title_type_dict)
    db.use_table(table)
    db.delete_all()

    headers_IG = {
        "cookie":"sessionid=1169657472%3AcAG6PSg6MB6DtF%3A29",
        "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }


    sub_page = f"https://www.instagram.com/p/CW-zbjlBlzU/"
    sub_page = f"https://www.instagram.com/p/CYjFJ-HhSuf/"
    # sub_page = f"https://www.instagram.com/p/CW5jQ0XD-fb/"
    sub_page = f"https://www.instagram.com/p/CY6E0_bPw7x/?utm_medium=share_sheet"
    sub_page = f"https://www.instagram.com/stories/lifechem.tw/2756113662948549900/"
    sub_page = f"https://www.instagram.com/tv/CY8SR7dJQQV/?utm_medium=share_sheet"
    in_out_checker = 0
    while in_out_checker < 20:
        log.info(f"in_out_checker{in_out_checker}")
        try:
            r = requests.get(sub_page,headers=headers_IG, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            if r.text.find("Login • Instagram") == -1:
                break
        except:
            in_out_checker += 1
    if in_out_checker < 20:
        r = requests.get(sub_page,headers=headers_IG).text

        ## find meida_count
        for thing in soup.find_all('script',type="text/javascript"):
            if len(thing.contents) > 0 and len(re.findall(r"\"https://instagram(.*?)\"",thing.contents[0])) > 2: 
                media_info = str(thing.contents[0].replace("\\u0026","&"))
                # log.info(str(thing.contents[0]).replace("\\u0026","&"))
                break
        picture_num = media_info.count('"media_type":1')
        video_num = media_info.count('"media_type":2')
        media_num = video_num + picture_num
        log.info(f"picture_num\t{picture_num}")
        log.info(f"video_num\t{video_num}")
        log.info(f"media_num\t{media_num}")

        # ## reply picture
        # ### reply multiple picture
        # if picture_num > 1:
        #     picture_list = []
        #     start = 0
        #     for _ in range(picture_num):
        #         start = media_info.find('"url":"https',media_info.find('"media_type":1',start))+7
        #         end = media_info.find('"',start)
        #         # log.info(media_info[start:end])
        #         picture_list.append(media_info[start:end])
            
        # ### reply single picture
        # elif picture_num == 1:
        #     start = media_info.find('"url":"https',media_info.find('"media_type":1'))+7
        #     end = media_info.find('"',start)
        #     log.info(media_info[start:end])
        
        # ## push video
        # video_list = []
        # start = 0
        # for _ in range(video_num):
        #     start = media_info.find('"url":"https',media_info.find('"media_type":2',start))+7
        #     end = media_info.find('"',start)
        #     log.info(f"start {start}")
        #     log.info(f"end {end}")
        #     log.info(media_info[start:end])
        #     start = media_info.find('"url":"https',media_info.find('video_versions',end))+7
        #     end = media_info.find('"',start)
        #     log.info(f"start {start}")
        #     log.info(f"end {end}")
        #     log.info(media_info[start:end])
        #     video_list.append(media_info[start:end])
        ### video thumbnail

            # log.info(len(thing.contents))
            # log.info(type(str(thing.contents[0])))
            # json_tag = json.loads(thing.contents[0])
            # pattern = re.findall(r"\"https://instagram(.*?)\"",thing.contents[0])
            # log.info(len(pattern))
            # for item in pattern:
            #     item = f"https://instagram{item}".replace("\\u0026","&")
            #     log.info(item)
            # log.info(type(thing.contents))
        # if "candidates" in thing.script:
        #     log.info(thing)
    # log.info(len(soup.find_all('div',class_="store-wrapper")))
    # result_dict = json.loads(r.text)
    # all_sqlite3_Row_list = db.read_column(column="url")
    # db_url_list =[]
    # for thing in all_sqlite3_Row_list:
    #     db_url_list.append(thing["url"])
    # for thing in result_dict["data"]["merchantList"][0]["merchants"]:
    #     name=thing["name"].replace("'","_").replace('"',"_")
    #     shopId=thing["shopId"]
    #     point=thing["point"]["amount"]
    #     url=thing["url"]
    #     image_url=thing["imageUrl"]
    #     transfer_Url=thing["transferPageUrl"]
    #     log.info(f"name{name}")
    #     log.info(f"shopId{shopId}")
    #     log.info(f"point{point}")
    #     log.info(f"url{url}")
    #     log.info(f"image_url{image_url}")
    #     log.info(f"transfer_url{transfer_Url}")
    #     if url not in db_url_list:
    #         id_counter = db.count("id")+1
    #         db.create(id=id_counter,name=name,shopId=shopId,point=point,url=url,image_url=image_url,transfer_Url=transfer_Url)
    #         log.info(f"create")
    #     elif url in db_url_list:
    #         db.update(name=name,shopId=shopId,point=point,url=url,image_url=image_url,transfer_Url=transfer_Url,where=f"url = '{url}'")
    #         log.info(f"update")
    # log.info("update finish")
    db.close()

if __name__ == "__main__":
    # while True:
    # try:
    now = datetime.datetime.now()
    remove_old_log(dir_path=f"{base_dir}/log",file_name=py_name)
    log = py_logger("w", level="INFO", dir_path=f"{base_dir}/log",file_name=py_name)
    log.info(f"{Path(__file__)}")
    # if now.hour == start_hour and now.minute == start_min:
    collect()
    close_log(log)
    # sleep(59)
    # except:
    #     pass
    