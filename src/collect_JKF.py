# -*- coding: UTF-8 -*-
import datetime
from pathlib import Path
from sqlite_CRUD import Database
from time import sleep
import requests
from bs4 import BeautifulSoup
from py_logging import py_logger, close_log, remove_old_log

base_dir = Path(__file__).parent.parent
py_name = Path(__file__).stem
db_path = f"{base_dir}/db.sqlite3"
headers_JKF = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',}
table_dict = {
    "IU_line_bot_oo_table":522,
    "IU_line_bot_mm_table":574,
    "IU_line_bot_cc_table":640,
    "IU_line_bot_pp_table":525,
}
start_hour = 1
start_min = 10

def collect_JKF():
    for table in table_dict:
        log.info(f"{table} is running")
        fid = table_dict[table]
        db = Database(db_path = f"{db_path}")
        # db.sql_do(f"DROP TABLE {table};")
        # title_type_dict = {
        #     "id":"integer",
        #     "package":"text",
        #     "url":"text",
        #     "package_name":"text",
        # }
        db.use_table(table)
        # db.create_table(table,title_type_dict)
        # db.delete_all()
        # db.create(id=0,package=0,url=1,package_name=1)
        db_table_package_name = db.read_all()
        package_name_list =[]
        for row in db_table_package_name:
            package_name_list.append(row["package_name"])
            # print(row["package_name"])
            package = int(row["package"])+1
            id = int(row["id"])+1
        log.info(f"row in {table} {len(package_name_list)}")
        # id = 1
        # package = 1
        try:
            for main_page in range(1,20):
                main_url = f"https://www.jkforum.net/forum.php?mod=forumdisplay&fid={fid}&typeid=&orderby=dateline&typeid=&filter=author&orderby=dateline&page={main_page}"
                log.info(main_url)
                r_main = requests.get(main_url, headers=headers_JKF)
                soup = BeautifulSoup(r_main.text, 'html.parser')
                sub_urls = soup.find_all('a',class_="z", href=True)
                for sub_page in sub_urls:
                    sub_title = sub_page.get('title').replace("'","")
                    log.info(sub_title)
                    if sub_title not in package_name_list:
                        sub_url = f"https://www.jkforum.net/{sub_page.get('href')}"
                        r_sub = requests.get(sub_url, headers=headers_JKF)
                        soup = BeautifulSoup(r_sub.text, 'html.parser')
                        pic_urls = soup.find_all('img',class_="zoom")
                        # if fid == 640:
                        #     pic_urls = pic_urls[:3]
                        if len(pic_urls) >= 10:
                            pic_urls = pic_urls[:10]
                        for pic_url in pic_urls:
                            if str(pic_url.get('zoomfile')) != "None":
                                db.create(id=id,package=package,url=str(pic_url.get('zoomfile')),package_name=str(sub_title))
                                id = id + 1
                            else:
                                log.info(str(pic_url.get('zoomfile')))
                            # log.info(str(pic_url.get('zoomfile')))
                        package = package + 1
                        # sleep(5)
                # sleep(5)
        except Exception as e:
            log.info(e)
        db.close()
    log.info("finish")

if __name__ == "__main__":
    while True:
        now = datetime.datetime.now()
        remove_old_log(log_path=f"{base_dir}/log",file_name=py_name)
        log = py_logger("a", level="INFO", log_path=f"{base_dir}/log",file_name=py_name)
        log.info(f"{Path(__file__)}")
        if now.hour == start_hour and now.minute == start_min:
            collect_JKF()
        close_log(log)
        sleep(60)
