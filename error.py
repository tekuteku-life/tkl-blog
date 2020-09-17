#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

#============================================================
# Copyright 2020 tekuteku.life
#============================================================


#============================================================
# Error
#============================================================
def error(msg):
	print("Content-type: text/html; charset=UTF-8")
	print()
	print("""
		<html>
			<head>Error</head>
			<body>
				<h1>Error</h1>
				<p>
					{msg}
				</p>
			</body>
		</html>
	""".format(msg = msg))
