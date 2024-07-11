# -*- coding: utf-8 -*-
# 2022_0422 v3
import sqlite3
from pathlib import Path
from py_logging import py_logger, get_logger, remove_old_log, close_log

# this for sub module
log = get_logger()

class Database:
	def __init__(self, **kwargs):
		self.db_path = kwargs.get('db_path')
		self.conn = sqlite3.connect(self.db_path)
		log.debug(f"Connect database: {self.db_path}")

	def use_table(self,table_name):
		"""Choose which table to be used

		Args:
			table_name (str): The table name in database
		"""
		self.table = table_name

	def sql_do(self, sql, *params):
		"""Do a specific sql

		Args:
			sql (str): string in sql format
		"""		
		self.conn.execute(sql, params)
		self.conn.commit()

	def create_table(self,table_name,table_dict):
		"""Create table

		Args:
			table_name (str): table name
			table_dict (dict): keyword:value are title:type of columns to create table
		
		Sample:
			table_dict = {
				"id":"integer",
				"name":"text",
				"url":"text",
			}
		"""
		sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
		for thing in table_dict:
			sql = f"{sql}{thing} {table_dict[thing]},"
		sql = f"{sql[:-1]});"
		# sql sample: "CREATE TABLE IF NOT EXISTS test_table (id integer,name text,url text);"
		self.conn.execute(sql)
		log.debug(f"Create table: {sql}")

	def create(self, data_dict={}, **kwargs):
		"""Create new data

		Args:
			data_dict (dict, optional): The dict include data. Defaults to {}.

		Method 1: use kwarg
			db.create(id = id_counter, name = name, url = url)

		Method 2: use dict
			db.create(data_dict)
		"""
		cols = f""
		values = f""
		if data_dict != {}:
			for thing in data_dict:
				cols = f"{cols}{thing},"
				values = f"{values}'{data_dict[thing]}',"
			sql = f"INSERT INTO {self.table} ({cols[:-1]}) VALUES ({values[:-1]});"
		else:
			for thing in kwargs:
				cols = f"{cols}{thing},"
				values = f"{values}'{kwargs[thing]}',"
			sql = f"INSERT INTO {self.table} ({cols[:-1]}) VALUES ({values[:-1]});"
		# sql sample: "INSERT INTO test_table (id,name,url) VALUES ('0','test_1','https://test_1.com');"
		self.conn.execute(sql)
		self.conn.commit()
		log.debug(f"Create data: {sql}")
	
	def read_all(self, enable_row_factory=False):
		"""Read all columns from table

		Args:
			enable_row_factory (bool, optional): set data type as 'tuple' or 'sqlite3.row'. Defaults to False('tuple').

		Returns:
			list: list of 'tuple' or 'sqlite3.row'
		"""
		if enable_row_factory == True:
			self.conn.row_factory = sqlite3.Row
		sql = f"SELECT rowid, * FROM {self.table};"
		cursor = self.conn.execute(sql)
		log.debug(f"Read all: {sql}")
		return cursor.fetchall()
		
		# sample:
		# all_sqlite3_Row_list = db.read_all(enable_row_factory=True)
		# db_id_dict = {}
		# for thing in all_sqlite3_Row_list:
		# 	db_id_dict[f"{thing['id']}"] = thing['name']
		

	def read_column(self, column, enable_row_factory=False):
		"""Read specific column from table

		Args:
			column (str): the column to read
			enable_row_factory (bool, optional): set data type as 'tuple' or 'sqlite3.row'. Defaults to False('tuple').

		Returns:
			list: list of 'tuple' or 'sqlite3.row'
		"""		
		if enable_row_factory == True:
			self.conn.row_factory = sqlite3.Row
		sql = f"SELECT {column} FROM {self.table};"
		cursor = self.conn.execute(sql)
		log.debug(f"Read column '{column}': {sql}")
		return cursor.fetchall()
		# sample:
		# db_url_list = db.read_column("url")

	def read(self, where="None", enable_row_factory=False):
		"""Read all columns for a condition

		Args:
			where (str, optional): the condition. Defaults to "None".
			enable_row_factory (bool, optional): set data type as 'tuple' or 'sqlite3.row'. Defaults to False('tuple').

		Returns:
			list: list of 'tuple' or 'sqlite3.row'
		"""
		if enable_row_factory == True:
			self.conn.row_factory = sqlite3.Row
		if where != "None":	
			sql = f"SELECT * FROM {self.table} WHERE {where};"
			cursor = self.conn.execute(sql)
			log.debug(f"Read where '{where}': {sql}")
			return cursor.fetchall()
		# sample:
		# db_id_list = db.read(where="id = 2")

	def update(self, data_dict = {}, where="None", **kwargs):
		"""Update table with data

		Args:
			data_dict (dict, optional): use dict to update data_update. Defaults to {}.
			where (str, optional): condition to find the row to update, update all rows if it is "None". Defaults to "None".
		"""		
		values = f""
		if data_dict != {}:
			for thing in data_dict:
				values = f"{values}{thing}='{data_dict[thing]}',"
		else:
			for thing in kwargs:
				values = f"{values}{thing}='{kwargs[thing]}',"
		if where == "None":
			sql = f"UPDATE {self.table} SET {values[:-1]};"
		else:
			sql = f"UPDATE {self.table} SET {values[:-1]} WHERE {where};"
		#sql sample: UPDATE test_table SET id='71',name='test_1',url='https://test_1.com' WHERE id = 67;
		self.conn.execute(sql)
		self.conn.commit()
		log.debug(f"Update data: {sql}")
		# smaple:
		# db.update(id = id_counter, name = name, url = url, where ="id = 67")
		# dict_1 = {
		# 	"id":f"{db.count('id')}",
		# 	"name":"test_1",
		# 	"url":"https://test_1.com",
		# }
		# db.update(dict_1, where ="id = 68")	

	def delete_all(self):
		sql = f"DELETE FROM {self.table};"
		self.conn.execute(sql)
		self.conn.commit()
		log.debug(f"Delete all: {sql}")
		
	def delete(self, where = "None"):
		"""Delete specific row

		Args:
			where (str, optional): condition for the row. Defaults to "None".
		"""		
		if where != "None":
			sql = f"DELETE FROM {self.table} WHERE {where};"
			self.conn.execute(sql)
			self.conn.commit()
			log.debug(f"Delete where '{where}': {sql}")
		# sample:
		# db.delete(where = "id = 71")

	def count(self, remove_duplicate=False, column="None",  where = "None"):
		"""Count table with condition

		Args:
			remove_duplicate (bool, optional): to remove duplicate rows. Defaults to False.
			column (str, optional): specific column to count. Defaults to "None".
			where (str, optional): condition to count_condition. Defaults to "None".

		Returns:
			int: counting number
		"""		
		count_condition = f""
		if remove_duplicate:
			count_condition = f"{count_condition}DISTINCT "
		if column != "None":
			count_condition = f"{count_condition}{column}"
		else:
			count_condition = f"{count_condition}*"
		if where != "None":
			sql = f"SELECT count({count_condition}) FROM {self.table} WHERE {where};"
		else:
			sql = f"SELECT count({count_condition}) FROM {self.table};"
		counter = self.conn.execute(sql).fetchone()[0]
		log.debug(f"Count {count_condition} where '{where}': {sql}")
		return counter

	def close(self):
		self.conn.close()
		log.debug(f"Close connection: {self.db_path}")

if __name__ == "__main__": 

	# set path and name
	here_dir = Path(__file__).parent
	py_name = Path(__file__).stem
	log = py_logger("a",level="DEBUG", dir_path=f"{here_dir}/log",file_name=f"{py_name}")

	# set Database
	db_name = py_name
	db_path = f"{here_dir}/{db_name}.sqlite3"
	db = Database(db_path = f"{db_path}")
	table = "test_table"
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
	db.close()

	# close log
	close_log(log)
	
