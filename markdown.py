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
	return "<{hx} id=\"{txt}\">{txt}</{hx}>\n".format(hx=hx, txt=m.group(2))
def md_func_hx(t):
	return re.sub(r"(#{1,6})[ \t]+([^\n]+?)(?:\n|$)", __md_func_hx, t)


#============================================================
# Translation bold, italic, line-through
#============================================================
def md_func_decoration(t):
	t = re.sub(r"(\s|^)~~~([^\n]+?)~~~(\s|$)", r"\1" + "<span class=\"md_line_through\">" + r"\2" + "</span>" + r"\3", t)
	t = re.sub(r"(\s|^)\*\*\*([^\n]+?)\*\*\*(\s|$)", r"\1" + "<span class=\"md_bold md_italic\">" + r"\2" + "</span>" + r"\3", t)
	t = re.sub(r"(\s|^)\*\*([^\n]+?)\*\*(\s|$)", r"\1" + "<span class=\"md_bold\">" + r"\2" + "</span>" + r"\3", t)
	t = re.sub(r"(\s|^)\*([^\*\n]+?)\*(\s|$)", r"\1" + "<span class=\"md_italic\">" + r"\2" + "</span>" + r"\3", t)
	return t


#============================================================
# Translation line
#============================================================
def md_func_line(t):
	return re.sub(r"(?:[\*~-] *){3}\n", "<hr>\n", t)


#============================================================
# Translation inner list
#============================================================
def __md_func_list(t, tag_name, mark):
	HEAD_TAG = "<{}>\n".format(tag_name)
	FOOT_TAG = "</{}>\n".format(tag_name)
	r = ""
	ins_head = False
	prev_sp_cnt = 0
	list_dep = 0
	for l in t.split("\n"):
		m = re.search(r"^([ \t]*)" + mark + r"[ \t]+(.+)", l)
		sp_cnt = 0
		if m:
			if ins_head == False:
				ins_head = True
				r = r + HEAD_TAG
			else:
				r = r + "</li>\n"
				sp_cnt = m.group(1).count(" ") or m.group(1).count("\t")*4
				if sp_cnt > prev_sp_cnt:
					list_dep = list_dep + 1
					r = r + HEAD_TAG
			
			if sp_cnt < prev_sp_cnt:
				list_dep = list_dep - 1
				r = r + FOOT_TAG
			
			r = r + "<li>" + m.group(2)

			prev_sp_cnt = sp_cnt
		else:
			m = re.search(r"^([ \t]+)", l)
			if m:
				sp_cnt = m.group(1).count(" ") or m.group(1).count("\t")*4
			if sp_cnt == 0:
				if (list_dep > 0 or prev_sp_cnt != 0):
					while list_dep > 0:
						list_dep = list_dep - 1
						r = r + "</li>\n"
						r = r + FOOT_TAG
					r = r + FOOT_TAG
					prev_sp_cnt = 0
					ins_head = False
			
			r = r + l
		
		r = r + "\n"

	return r


#============================================================
# Translation dot list
#============================================================
def md_func_dotlist(t):
	return __md_func_list(t, "ul", r"\*")


#============================================================
# Translation number list
#============================================================
def md_func_numlist(t):
	return __md_func_list(t, "ol", r"\d+\.")


#============================================================
# Translation quotation
#============================================================
def md_func_quotation(t):
	HEAD_TAG = "<blockquote>\n"
	FOOT_TAG = "</blockquote>\n"
	r = ""
	ins_head = False
	prev_sp_cnt = 0
	quote_dep = 0
	for l in t.split("\n"):
		m = re.search(r"^[ \t]*(>+)(?:[ \t]+(.+))?", l)
		sp_cnt = 0
		if m:
			if ins_head == False:
				ins_head = True
				r = r + HEAD_TAG
			else:
				sp_cnt = m.group(1).count(">")
				if sp_cnt > prev_sp_cnt:
					quote_dep = quote_dep + 1
					r = r + HEAD_TAG

			if sp_cnt < prev_sp_cnt:
				quote_dep = quote_dep - 1
				r = r + FOOT_TAG
			
			if m.group(2):
				r = r + m.group(2)

			prev_sp_cnt = sp_cnt
		else:
			if quote_dep > 0 or prev_sp_cnt != 0:
				while quote_dep > 0:
					quote_dep = quote_dep - 1
					r = r + FOOT_TAG
				r = r + FOOT_TAG
				prev_sp_cnt = 0
				ins_head = False
			
			r = r + l
		
		r = r + "\n"

	return r


#============================================================
# Translation pre-text
#============================================================
def md_func_pretext(t):
	return re.sub(r"(\s|^)```\n*((?:.|\s)+?)\n*```(\s|$)", r"\1<pre>\2</pre>\3", t)


#============================================================
# Translation anchor
#============================================================
def md_func_anchor(t):
	t = re.sub(r"((?:[ \t]|^)?)\[([^\]]+)\]\((#[^\)]+?)\)((?:[ \t]|$)?)", r"\1" + "<a href=\"" + r"\3" + "\">" + r"\2" + "</a>" + r"\4", t)
	t = re.sub(r"((?:[ \t]|^)?)\[([^\]]+)\]\(([^\)]+?)\)((?:[ \t]|$)?)", r"\1" + "<a href=\"" + r"\3" + "\" target=\"_blank\">" + r"\2" + "</a>" + r"\4", t)
	return t


#============================================================
# Translation mark
#============================================================
def md_func_mark(t):
	return re.sub(r" `([^`]+)` ", " <mark>" + r"\1" + "</mark> ", t)


#============================================================
# Translation paragraph
#============================================================
def md_func_paragraph(t):
	ins_flg = False
	r = ""
	for l in t.split("\n"):
		if l != "":
			if ins_flg:
				ins_flg = False
				r = r + "</p>\n\n<p>\n" + l + "\n"
			else:
				r = r + l + "\n"
		else:
			ins_flg = True
	
	r = re.sub(r"^</p>\n", "", r)
	r = r + "</p>"

	return r


#============================================================
# Translation table
#============================================================
def __md_func_table(t):
	r = ""
	cells = []
	aligns = []

	# split cells
	for l in t.split("\n"):
		if l != "":
			cells.append([re.sub(r"^[ \t]+|[ \t]+$", "", c) for c in l.split("|") if c != ""])
	
	# parse align
	for al in cells[1]:
		m = re.search(r"-{3,}", al)
		if not m:
			return t
		
		lm = re.search(r"^:", al)
		rm = re.search(r":$", al)
		if lm and rm:
			aligns.append("center")
		elif rm:
			aligns.append("right")
		else:
			aligns.append("left")

	# make header
	r = "\n\n<table>\n<tr>\n"
	i = 0
	for c in cells[0]:
		r = r + "<th class=\"{}\">{}</th>".format(aligns[i], c)
		i = i + 1
	r = r + "</tr>"

	del cells[0:2]

	for row in cells:
		r = r + "<tr>\n"
		i = 0
		for c in row:
			r = r + "<td class=\"{}\">{}</td>".format(aligns[i], c)
			i = i + 1
		r = r + "\n</tr>\n"
	
	r = r + "</table>\n"
	
	return r
			
def md_func_table(t):
	tbl_buf = ""
	r = ""
	for l in t.split("\n"):
		m = re.search(r"^[ \t]*(?:\|[^\|]+)+\|[ \t]*$", l)
		if m:
			tbl_buf = tbl_buf + l + "\n"
		elif tbl_buf != "":
			r = r + __md_func_table(tbl_buf)
			tbl_buf = ""
		else:
			r = r + l + "\n"
	return r


#============================================================
# Markdown translation
#============================================================
def translate_markdown(t):
	t = re.sub("\r\n|\r|\n", "\n", t)

	t = md_func_quotation(t)
	t = md_func_mark(t)

	t = md_func_dotlist(t)
	t = md_func_numlist(t)

	t = md_func_hx(t)
	t = md_func_decoration(t)
	t = md_func_line(t)
	t = md_func_pretext(t)
	t = md_func_anchor(t)

	t = md_func_table(t)

	t = md_func_paragraph(t)
	
	t = re.sub("  \n", "<br>\n", t)

	return t