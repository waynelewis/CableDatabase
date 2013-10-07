#!/usr/bin/env python

import cgitb, cgi, sys, time
cgitb.enable()

from CableDatabase import library as cdblib
import pystache

def printTableData(keys):
	rows = cdblib.getAllData(keys)
	rdict = [dict(label = cdblib.makeCableLabel(row,'{A..B}'),
				  type = row[4] + '(' + row[5] + ')',
				  use = row[6],
				  source = row[7],
				  destination = row[8],
				  path = row[9],
				  drawing = row[10],
				  installed = row[11])
				  for row in rows]

	# Setup the renderer to make the html list
	renderer = pystache.Renderer()
	data = renderer.render_path('tableData.mustache', {'footer' : time.asctime(time.localtime()),
													   'title'  : 'Cable Data',
												       'sourceList' : rdict})
	print data

def printPullSheet(keys):
	rows = cdblib.getPullSheetData(keys)
	rdict = [dict(label = row[0] - 100000,
				  type = row[4] + '(' + row[5] + ')',
				  use = row[6],
				  source = row[7],
				  path = row[8],
				  destination = row[9])
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


