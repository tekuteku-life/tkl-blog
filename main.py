#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

#============================================================
# Copyright 2020 tekuteku.life
#============================================================


#============================================================
# Import & default setting
#============================================================
# import cgi
import io
import sys
sys.dont_write_bytecode = True
sys.stdin =  open(sys.stdin.fileno(),  'r', encoding='UTF-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='UTF-8')
sys.stderr = open(sys.stderr.fileno(), 'w', encoding='UTF-8')
# import cgitb
# cgitb.enable()
import re
from datetime import datetime

import conf
from accessarticle import AccessArticle
from accessauthor import AccessAuthor


#============================================================
# Generate article part
#============================================================
def gen_article(article):

	acc_author = AccessAuthor()

	for data in article.read_all():
		content = re.sub("\r\n|\r|\n", "<br>", data["content"])
		dt = datetime.fromtimestamp(float(data["date"]))
		date = dt.strftime('%Y/%m/%d %H:%M:%S')
		
		print("""
			<a href="./?id={0}">{1}</a><br>
			{4}
			<br>
			at {2}, by {3}
			<hr>
		""".format(data["id"], data["title"], date, acc_author.id2name(data["author"]), content) )


#============================================================
# Main
#============================================================
def main():
	article = AccessArticle()

	print("Content-type: text/html; charset=UTF-8;")
	print()
	print("""
		<html>
			<head>
				<title>てくてくらいふ</title>
				{google_tracking_tag}
			</head>
			<body>
				ここは、雑記ブログです。<br>
				当面の目標は、勉強を兼ねて一からブログを「作る」を目標にしています。<br>
				生々しい制作の過程をGithubのcommitから感じ取って頂けると幸いです…ｗ<br>
				<hr>
	""".format(google_tracking_tag = conf.google_tracking_tag))

	gen_article(article)

	print("""
			<a href="https://twitter.com/tekutekulife0">Twitter</a><br>
			<a href="https://github.com/tekuteku-life/">Github</a><br>

				<footer>
					Copyright 2020 tekuteku.life
				</footer>
			</body>
		</html>
	""")


if __name__ == "__main__":
	main()
