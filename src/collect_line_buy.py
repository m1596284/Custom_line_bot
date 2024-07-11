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

# set path and name
base_dir = Path(__file__).parent.parent
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
	table = "IU_line_bot_line_buy_table"
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
	# db.delete_all()

	db.use_table("IU_line_bot_line_buy_topic_table")
	all_sqlite3_Row_list = db.read_all()
	db_topic_dict = {}
	for thing in all_sqlite3_Row_list:
		db_topic_dict[f"{thing['topic']}"] = thing["queryID"]
	log.info(db_topic_dict)

	for topic in db_topic_dict:
		main_url = f"https://buy.line.me/api/graphql?variables=%7B%22queryCodes%22%3A%5B{db_topic_dict[topic]}%5D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22cd76d273829df7c1b8c3bcf95da7eb087c5a52809d53d0c7295f867ba5fefe84%22%7D%7D"
		log.info(f"{topic}{main_url}")
		r = requests.get(main_url, headers=headers)
		result_dict = json.loads(r.text)
		db.use_table("IU_line_bot_line_buy_table")
		all_sqlite3_Row_list = db.read_column(column="url")
		db_url_list =[]
		for thing in all_sqlite3_Row_list:
			db_url_list.append(thing["url"])
		for thing in result_dict["data"]["merchantList"][0]["merchants"]:
			name=thing["name"].replace("'","_").replace('"',"_")
			shopId=thing["shopId"]
			point=thing["point"]["amount"]
			url=thing["url"]
			image_url=thing["imageUrl"]
			transfer_Url=thing["transferPageUrl"]
			log.info(f"name{name}")
			log.info(f"shopId{shopId}")
			log.info(f"point{point}")
			log.info(f"url{url}")
			log.info(f"image_url{image_url}")
			log.info(f"transfer_url{transfer_Url}")
			if url not in db_url_list:
				id_counter = db.count("id")+1
				db.create(id=id_counter,name=name,shopId=shopId,point=point,url=url,image_url=image_url,transfer_Url=transfer_Url)
				log.info(f"create")
			elif url in db_url_list:
				db.update(name=name,shopId=shopId,point=point,url=url,image_url=image_url,transfer_Url=transfer_Url,where=f"url = '{url}'")
				log.info(f"update")
	log.info("update finish")
	db.close()

def topic_checker():
	## set Database
	db_path = f"{base_dir}/db.sqlite3"
	db = Database(db_path = f"{db_path}")
	table = "IU_line_bot_line_buy_topic_table"
	title_type_dict = {
		"id":"integer",
		"topic":"text",
		"queryID":"text",
	}
	db.create_table(table,title_type_dict)
	db.use_table(table)
	# db.delete_all()
	all_sqlite3_Row_list = db.read_column(column="topic")
	db_topic_list =[]
	for thing in all_sqlite3_Row_list:
		db_topic_list.append(thing["topic"])

	for i in range(0,150):
		log.info(i)
		topic_url = f"https://buy.line.me/api/graphql?variables=%7B%22queryCodes%22%3A%5B{i}%5D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22cd76d273829df7c1b8c3bcf95da7eb087c5a52809d53d0c7295f867ba5fefe84%22%7D%7D"
		r = requests.get(topic_url, headers=headers)
		result_dict = json.loads(r.text)
		if result_dict.get('errors'):
			pass
		else:
			topic = result_dict["data"]["merchantList"][0]["classification"]["name"]
			queryID = i
			if topic not in db_topic_list:
				id_counter = db.count("id")+1
				db.create(id=id_counter,topic=topic,queryID=queryID)
			else:
				db.update(topic=topic,queryID=queryID,where=f"topic = '{topic}'")
	db.close()

if __name__ == "__main__":
	while True:
		try:
			now = datetime.datetime.now()
			remove_old_log(log_path=f"{base_dir}/log",file_name=py_name)
			log = py_logger("a", level="INFO", log_path=f"{base_dir}/log",file_name=py_name)
			log.info(f"{Path(__file__)}")
			if now.hour == start_hour and now.minute == start_min:
				topic_checker()
				collect()
			close_log(log)
			sleep(59)
		except:
			pass
	