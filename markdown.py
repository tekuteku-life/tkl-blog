#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

#============================================================
# Copyright 2020 tekuteku.life
#============================================================


#============================================================
# Import & default setting
#============================================================
import re


#============================================================
# Translation H1, H2, H3, H4, H5, H6
#============================================================
def __md_func_hx(m):
	hx = "h" + str(m.group(1).count("#"))
	return "<{hx} id=\"{txt}\">{txt}</{hx}>".format(hx=hx, txt=m.group(2))
def md_func_hx(t):
	return re.sub(r"(#{1,6})[ \t]+([^\n]+?)(?:\n|$)", __md_func_hx, t)


#============================================================
# Translation bold, italic, line-through
#============================================================
def md_func_decoration(t):
	t = re.sub(r"(\s|^)~~~([^\n]+?)~~~(\s|$)", r"\1" + " <span class=\"md_line_through\">" + r"\2" + "</span> " + r"\3", t)
	t = re.sub(r"(\s|^)\*\*\*([^\n]+?)\*\*\*(\s|$)", r"\1" + " <span class=\"md_bold md_italic\">" + r"\2" + "</span> " + r"\3", t)
	t = re.sub(r"(\s|^)\*\*([^\n]+?)\*\*(\s|$)", r"\1" + " <span class=\"md_bold\">" + r"\2" + "</span> " + r"\3", t)
	t = re.sub(r"(\s|^)\*([^\*\n]+?)\*(\s|$)", r"\1" + " <span class=\"md_italic\">" + r"\2" + "</span> " + r"\3", t)
	return t


#============================================================
# Translation line
#============================================================
def md_func_line(t):
	return re.sub(r"(?:[\*~-] *){3}\n", "<hr>", t)


#============================================================
# Translation dot list
#============================================================
def md_func_dotlist(t):
	r = ""
	blk = False
	lst = False
	prev_sp_cnt = 0
	list_dep = 0
	for l in t.split("\n"):
		m = re.search(r"([ \t]*)\*[ \t]+(.+)", l)
		sp_cnt = 0
		if m:
			sp_cnt = m.group(1).count(" ") or m.group(1).count("\t")
			if blk or sp_cnt > prev_sp_cnt:
				lst = True
				list_dep = list_dep + 1
				r = r + "<ul>"

			if sp_cnt < prev_sp_cnt:
				list_dep = list_dep - 1
				r = r + "</ul>"
				
			r = r + "<li>" + m.group(2) + "</li>"

			prev_sp_cnt = sp_cnt
		else:
			if lst or prev_sp_cnt != 0:
				lst = False
				while list_dep > 0:
					list_dep = list_dep - 1
					r = r + "</ul>"
				prev_sp_cnt = 0
				r = r + "\n\n"
			else:
				r = r + l + "\n"
		
		if l == "":
			blk = True
		elif blk > 0:
			blk = False

	return r


#============================================================
# Translation number list
#============================================================
def md_func_numlist(t):
	r = ""
	blk = False
	lst = False
	prev_sp_cnt = 0
	list_dep = 0
	for l in t.split("\n"):
		m = re.search(r"([ \t]*)\d+\.[ \t]+(.+)", l)
		sp_cnt = 0
		if m:
			sp_cnt = m.group(1).count(" ") or m.group(1).count("\t")
			if blk or sp_cnt > prev_sp_cnt:
				lst = True
				list_dep = list_dep + 1
				r = r + "<ol>"

			if sp_cnt < prev_sp_cnt:
				list_dep = list_dep - 1
				r = r + "</ol>"
				
			r = r + "<li>" + m.group(2) + "</li>"

			prev_sp_cnt = sp_cnt
		else:
			if lst or prev_sp_cnt != 0:
				lst = False
				while list_dep > 0:
					list_dep = list_dep - 1
					r = r + "</ol>"
				prev_sp_cnt = 0
				r = r + "\n"
			else:
				r = r + l + "\n"
		
		if l == "":
			blk = True
		elif blk > 0:
			blk = False

	return r


#============================================================
# Translation pre-text
#============================================================
def md_func_pretext(t):
	return re.sub(r"```\n*((?:.|\s)+?)\n*```", r"<pre>\1</pre>", t)


#============================================================
# Translation anchor
#============================================================
def md_func_anchor(t):
	return re.sub(r"(?:\s|^)\[([^\]]+)\]\(([^\)]+?)\)(?:\s|$)", "<a href=\"" + r"\2" + "\" target=\"_blank\">" + r"\1" + "</a>", t)


#============================================================
# Markdown translation
#============================================================
def translate_markdown(t):
	t = re.sub("\r\n|\r|\n", "\n", t)

	t = md_func_dotlist(t)
	t = md_func_numlist(t)

	t = md_func_hx(t)
	t = md_func_decoration(t)
	t = md_func_line(t)
	t = md_func_pretext(t)
	t = md_func_anchor(t)
	
	t = re.sub("\n", "<br>", t)

	t = re.sub(r"<hr>\s*(?:<br>){2,}", r"<hr>", t)
	t = re.sub(r"(</[ou]l>)\s*(?:<br>){2,}", r"\1<br>", t)

	return t