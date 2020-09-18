#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

#============================================================
# Copyright 2020 tekuteku.life
#============================================================


#============================================================
# Import & default setting
#============================================================
import conf
import MySQLdb


#============================================================
# Author accessor class
#============================================================
class AccessAuthor:
	
	def __init__(self):
		self.con = MySQLdb.connect(
			user = conf.db_user,
			passwd = conf.db_pass,
			host = conf.db_server,
			db = conf.db_name,
			use_unicode=True,
			charset="utf8"
		)

	def id2name(self, id):
		try:
			cur = self.con.cursor()
			cur.execute("select name from {} where id=%s".format(conf.db_author_tbl_name), str(id))
			return cur.fetchone()[0]
		except:
			return None

