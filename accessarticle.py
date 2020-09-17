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
            db = conf.db_name
        )
        self.cur = self.con.cursor()

    def read_all(self):
        self.cur.execute("select * from {}".format(conf.db_article_tbl_name))
        return [ {"id": id, "title": title, "date": date, "author": author, "content": content} for id, title, date, author, content in self.cur.fetchall() ]
