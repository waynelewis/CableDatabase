#!/usr/bin/env python

import cgitb, cgi, sys, time
cgitb.enable()

from CableDatabase import library as cdblib

def doLabels(data):
	print 'Content-Type: application/csv; name="labels.csv"'
	print 'Content-Disposition: attachment; filename="labels.csv"'
	print
	for row in data:
		print cdblib.makeCableLabel(row, "A") + "," + cdblib.makeCableLabel(row, "B")
	
def doTableData(data):
	print 'Content-Type: application/csv; name="data.csv"'
	print 'Content-Disposition: attachment; filename="data.csv"'
	print
	for row in data:
		print ",".join([str(a) for a in row])

def main():
	form = cgi.FieldStorage()
	cmd = form.getvalue("command")
	ids = form.getvalue("idList")
	if cmd is None:
		raise Exception
	if ids is None:
		raise Exception
		
	ids = ids.split(",")
	data = cdblib.getData(ids)
	
	if cmd == "Download Labels":
		doLabels(data)
	elif cmd == "Download Table Data":
		doTableData(data)
	else:
		print 'Content-Type: text/plain\n\n'
		raise Exception
	
if __name__ == "__main__":
	main();