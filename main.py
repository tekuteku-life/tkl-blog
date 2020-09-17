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
sys.stdin =  open(sys.stdin.fileno(),  'r', encoding='UTF-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='UTF-8')
sys.stderr = open(sys.stderr.fileno(), 'w', encoding='UTF-8')
import cgitb
cgitb.enable()

import conf
from accessarticle import AccessArticle


#============================================================
# Generate article part
#============================================================
def gen_article(article):
    for data in article.read_all():
        print("""
            <a href="./?id={0}">{1}</a><br>
            {4}
            <br>
            at {2}, by {3}
            <hr>
        """.format(data["id"], data["title"], data["date"], data["author"], data["content"]) )


#============================================================
# Main
#============================================================
def main():
    article = AccessArticle()

    print("Content-type: text/html; charset=UTF-8;")
    print()
    print("""
        <html>
            <head><title>てくてくらいふ</title></head>
            <body>
                ここは、雑記ブログです。<br>
                当面の目標は、勉強を兼ねて一からブログを「作る」を目標にしています。<br>
                <hr>
    """)

    gen_article(article)

    print("""
            <a href="https://twitter.com/tekutekulife0">Twitter</a><br>

                <footer>
                    Copyright 2020 tekuteku.life
                </footer>
            </body>
        </html>
    """)


if __name__ == "__main__":
    main()
