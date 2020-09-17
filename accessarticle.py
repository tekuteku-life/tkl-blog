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


class AccessArticle:
	
	def __init__(self):
		self.con = MySQLdb.connect(
			user = conf.db_user,
			passwd = conf.db_pass,
			host = conf.db_server,
			db = conf.db_name,
			use_unicode=True,
			charset="utf8"
		)

	def add(self, data):
		cur = self.con.cursor()
		cur.execute(
			"insert into {} values (%s, %s, %s, %s, %s)".format(conf.db_article_tbl_name),
			(data["id"], data["title"], data["date"], data["author"], data["content"])
		)
		cur.close()
		self.con.commit()

	def read_all(self):
		cur = self.con.cursor()
		cur.execute("select * from {}".format(conf.db_article_tbl_name))
		return [ {"id": id, "title": title, "date": date, "author": author, "content": content} for id, title, date, author, content in cur.fetchall() ]
