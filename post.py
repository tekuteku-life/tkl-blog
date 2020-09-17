#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

#============================================================
# Copyright 2020 tekuteku.life
#============================================================

#============================================================
# Import & default setting
#============================================================
import cgi
import io
import sys
sys.dont_write_bytecode = True
sys.stdin =  open(sys.stdin.fileno(),  'r', encoding='UTF-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='UTF-8')
sys.stderr = open(sys.stderr.fileno(), 'w', encoding='UTF-8')
import cgitb
cgitb.enable()
import os
import time
import html

import conf
from accessarticle import AccessArticle
from error import error


#============================================================
# Authentication
#============================================================
def auth_check(passwd):
	return (passwd == conf.admin_passwd)


#============================================================
# Post data check
#============================================================
def is_valid_post(form_data):
	title = form_data.getvalue("title")
	content = form_data.getvalue("content")
	author = form_data.getvalue("author")

	if title == None or title == "":
		return False
	if content == None or content == "":
		return False
	if author == None or author == "":
		return False
	
	return True

#============================================================
# Post article
#============================================================
def post_article(form_data):
	if auth_check(form_data.getvalue("passwd")) == False:
		error("Admin password is incorrect")
		return
	
	if not is_valid_post(form_data):
		error("Posted data is invalid")
		return

	date = time.time()
	id = int(int(form_data.getvalue("author")) << 56 | int(date*100))
	title = html.unescape(form_data.getvalue("title"))
	author = form_data.getvalue("author")
	content = html.unescape(form_data.getvalue("content"))

	article = AccessArticle()
	article.add({
		"id" : id,
		"title" : title,
		"date" : date,
		"author" : author,
		"content" : content
	})

	print("Content-type: text/html; charset=UTF-8;")
	print()
	print("""
		<html>
			<head><title>Posted!</title></head>
			<body>
				<h1>Posted!</h1>
				id: {id}<br>
				title: {title}<br>
				date: {date}<br>
				author: {author}<br>
				content: {content}<br>
	""".format(
		id = id,
		title = title,
		date = date,
		author = author,
		content = content
	))


#============================================================
# Main
#============================================================
def main():
	form_data = cgi.FieldStorage()

	mode = form_data.getvalue("mode")
	if mode == "post":
		post_article(form_data)
	else:
		my_file_name = os.path.basename(__file__)
		print("Content-type: text\html; charset=UTF-8")
		print()
		print("""
			<html>
				<head><title>POST</title></head>
				<body>
					<form action="{my_file_name}" method="post">
						<input type="hidden" name="mode" value="post">
						Title: <input type="text" name="title"><br>
						Author: <input type="text" name="author"><br>
						Content: <textarea name="content" width="100" height="200"></textarea><br>
						Password: <input type="password" name="passwd"><br>
						<input type="submit" value="Post"><br>
					</form>
				</body>
			</html>
		""".format(my_file_name=my_file_name))


if __name__ == "__main__":
	main()