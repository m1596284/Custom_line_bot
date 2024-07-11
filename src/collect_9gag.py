# -*- coding: UTF-8 -*-
import datetime
from pathlib import Path
from sqlite_CRUD import Database
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from py_logging import py_logger, close_log, remove_old_log
import re

base_dir = Path(__file__).parent.parent
py_name = Path(__file__).stem
db_path = f"{base_dir}/db.sqlite3"
headers_9gag = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',}
table_dict = {
    "IU_line_bot_ngag_girl_table":"girl",
    "IU_line_bot_ngag_funny_table":"funny",
    "IU_line_bot_ngag_nsfw_table":"nsfw",
}
start_hour = 1
start_min = 30

def collect_9gag():
    for table in table_dict:
        log.info(f"{table} is running")
        ngag_tag = table_dict[table]
        db = Database(db_path = f"{db_path}")
        # table = "ngag_girl"
        db.use_table(table)
        title_type_dict = {
            "id":"integer",
            "article_id":"text",
            "article_title":"text",
            "article_type":"text",
        }
        db.create_table(table,title_type_dict)
        # db.delete_all()
        db_table_all = db.read_all()
        db_article_id = []
        id = 0
        for row in db_table_all:
            db_article_id.append(row["article_id"])
            id = int(row["id"])+1
        print(f"ddd{id}")
        if len(db_article_id) == 0:
            db.create(id=0,article_id=0,article_title=1,article_type=1)
            id = 1
        log.info(f"row in {table} {len(db_article_id)}")
        file_path = Path(__file__).parent
        chrome_path = f"{file_path}/driver/chromedriver"
        driver = webdriver.Chrome(executable_path=chrome_path)
        driver.maximize_window()
        driver.get(f"https://9gag.com/{ngag_tag}/hot")
        driver.refresh()
        article_id_list = []
        article_title_list = []
        article_type_list = []
        for i in range(1,10):
            log.info(i)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            articles = soup.find_all('article',id=re.compile("jsid-post-"))
            for thing in articles:
                try:
                    article_title = thing.header.h1.text
                    article_title = article_title.replace("'","")
                except:
                    article_title = "None"
                article_id = thing.get("id").replace("jsid-post-","")
                if article_title != "None":
                    if article_id not in db_article_id:
                        if article_id not in article_id_list:
                            r = requests.get(f"https://img-9gag-fun.9cache.com/photo/{article_id}_460s.jpg", headers=headers_9gag)
                            if r.text.find("404") == -1:
                                article_title_list.append(article_title)
                                article_id_list.append(article_id)
                                r = requests.get(f"https://img-9gag-fun.9cache.com/photo/{article_id}_460sv.mp4", headers=headers_9gag)
                                if r.text.find("404") == -1:
                                    article_type_list.append("mp4")
                                else:
                                    article_type_list.append("jpg")
                # log.info(article_title)
                # log.info(article_id)
            log.info(len(article_title_list))
            log.info(len(article_id_list))
            log.info(len(article_type_list))

            # log.info(ngag_picture)
            driver.execute_script("window.scrollBy(1000,1000);")
            driver.execute_script("window.scrollBy(-200,-200);")
            sleep(2)
        for num, item in enumerate(article_id_list):
            db.create(id=id,article_id=article_id_list[num],article_title=article_title_list[num],article_type=article_type_list[num])
            id = id +1
        driver.close()

if __name__ == "__main__":
    while True:
        now = datetime.datetime.now()
        remove_old_log(log_path=f"{base_dir}/log",file_name=py_name)
        log = py_logger("a", level="INFO", log_path=f"{base_dir}/log",file_name=py_name)
        log.info(f"{Path(__file__)}")
        if now.hour == start_hour and now.minute == start_min:
            collect_9gag()
        close_log(log)
        sleep(60)