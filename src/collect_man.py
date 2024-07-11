# -*- coding: utf-8 -*-
# 2022_0609 v3
from gettext import find
import time
import datetime
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from py_logging import py_logger,close_log, remove_old_log
from sqlite_CRUD import Database

def test_main():
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
	}

	id = 0
	package_num = 0
	if id == 0:
		data = {
			"id":0,
			"package":1,
			"url":1,
			"package_name":1,
		}
		db.create(data)
		id = id + 1
	for i in range(1,500):
		main_url = f"https://unsplash.com/napi/search/photos?query=muscle%20man&per_page=20&page={i}&xp="
		r = requests.get(main_url, headers=headers)
		r_json = r.json()
		log.info(len(r_json["results"]))
		log.info(type(r_json["results"]))
		for i2 in range(0,20):
			log.info(i2)
			log.info(r_json["results"][i2]["urls"]["regular"])
			pic_url = r_json["results"][i2]["urls"]["regular"]
			package_num = package_num + 1
			data = {
				"id":id,
				"package":package_num,
				"url":pic_url,
				"package_name":str(id),
			}
			db.create(data)
			id = id + 1

if __name__ == "__main__":
	# set path and name
	here_dir = Path(__file__).parent.parent
	py_name = Path(__file__).stem

	# set logger
	remove_old_log(log_path=f"{here_dir}/log",file_name=py_name)
	log = py_logger("w", level="INFO", log_path=f"{here_dir}/log",file_name=py_name)

	# set Database
	db_name = py_name
	db_path = f"{here_dir}/db.sqlite3"
	db = Database(db_path = f"{db_path}")
	table = "IU_line_bot_man_table"
	table_dict = {
		"id":"integer",
		"package":"text",
		"url":"text",
		"package_name":"text",
	}
	db.create_table(table,table_dict)
	db.use_table(table)
	db.delete_all()
	
	# start test
	test_main()

	# close database
	db.close()

	# close log
	close_log(log)
	