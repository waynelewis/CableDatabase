#!/usr/bin/env python

import cgitb, cgi, sys, time
cgitb.enable()

from CableDatabase import library as cdblib
import pystache

def printTableData(keys):
	rows = cdblib.doCableSearch(keys)
	rdict = [dict(label = cdblib.makeCableLabel(row,'{A/B}'),
				  type = row[7] + '(' + row[16] + ')',
				  use = row[8],
				  source = row[9],
				  destination = row[10],
				  path = row[12],
				  drawing = row[11],
				  installed = row[13])
				  for row in rows]


	# Setup the renderer to make the html list
	renderer = pystache.Renderer()
	data = renderer.render_path('tableData.mustache', {'footer' : time.asctime(time.localtime()),
													   'title'  : 'Cable Data',
													   'sourceList' : rdict,
													   'idlist' : ",".join(["{0}".format(row[0]) for row in rows])})
	print data

def printPullSheet(keys):
	rows = cdblib.doCableSearch(keys)
	rdict = [dict(label = row[0] - 100000,
				  type = row[7] + '(' + row[16] + ')',
				  use = row[8],
				  source = row[9],
				  path = row[12],
				  destination = row[10])
				  for row in rows]

	# Setup the renderer to make the html list
	renderer = pystache.Renderer()
	data = renderer.render_path('pullsheet.mustache', {'title' : 'Cable Pullsheet',
													   'footer' : time.asctime(time.localtime()),
												       'sourceList' : rdict})
	print data

def main():
	# First see what we have to do depending on value of command button
	
	form = cgi.FieldStorage()
	cmd = form.getvalue("command")
	if cmd is None:
		raise Exception
		
	keys = dict()
	for col in cdblib.dbColumns:
		keys[col] = form.getvalue(col)
	
	if cmd == "Print Pull-sheet":
		printPullSheet(keys)
	elif cmd == "Display Cable Data":
		printTableData(keys)
		
if __name__ == "__main__":
	print "Content-type: text/html\n\n";	
	main()


