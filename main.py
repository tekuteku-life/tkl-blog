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
# import cgitb
# cgitb.enable()
import re
from datetime import datetime

import conf
from accessarticle import AccessArticle
from accessauthor import AccessAuthor


#============================================================
# Print Header part
#============================================================]
def print_header():
	print("Content-type: text/html; charset=UTF-8;")
	print()
	print("""
		<!DOCTYPE html>
		<html lang="ja">
			<head>
				<title>てくてくらいふ</title>
				<meta name="viewport" content="width=device-width,initial-scale=1">
				<link rel="stylesheet" href="./css/main.css">
				<script type="text/javascript" src="./js/default.js"></script>
				<script type="text/javascript" src="./js/main.js"></script>
				{google_tracking_tag}
			</head>
			<body>
				<header>
					<h1><a href="https://tekuteku.life">てくてくらいふ</a></h1>
					<p class="page_description">
						7年ぶりぐらいのブランクを経て、久しぶりに自分のWebページを持ってみました。<br>
						当面の目標は、勉強を兼ねて一からブログを「作る」を目標にしています。<br>
						生々しい制作の過程をGithubのcommitから感じ取って頂けると幸いです…ｗ<br>
						日々の生活、子育て、カメラ、それとプログラミングについて、語れることを語れるだけ。<br>
					</p>
				</header>
	""".format(google_tracking_tag = conf.google_tracking_tag))


#============================================================
# Generate article part
#============================================================
def gen_article(article, args):

	acc_author = AccessAuthor()

	if args.getvalue("id"):
		data_list = article.read_by_id(args.getvalue("id"))
	else:
		data_list = article.read_all()

	for data in data_list:
		content = re.sub("\r\n|\r|\n", "<br>", data["content"])
		dt = datetime.fromtimestamp(float(data["date"]))
		date = dt.strftime('%Y/%m/%d %H:%M:%S')
		
		print("""
			<article>
				<h3 class="article_title"><a href="./?id={0}">{1}</a></h3>
				<div class="article_body">
					{4}
				</div>
				<footer class="article_footer">
					<div>at {2}, by {3}</div>
				</footer>
			</article>
		""".format(data["id"], data["title"], date, acc_author.id2name(data["author"]), content) )


#============================================================
# Print Footer part
#============================================================
def print_footer():
	print("""
				<footer>
				<p>
					<a href="https://twitter.com/tekutekulife0">Twitter</a><br>
					<a href="https://github.com/tekuteku-life/">Github</a><br>
				</p>

				<small class="copyright">Copyright 2020 tekuteku.life</small>
			</footer>
		</body>
	</html>
	""")

#============================================================
# Main
#============================================================
def main():
	args = cgi.FieldStorage()
	article = AccessArticle()

	print_header()
	gen_article(article, args)
	print_footer()


if __name__ == "__main__":
	main()
