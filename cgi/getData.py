#!/usr/bin/env python

import cgitb, cgi, sys, time
cgitb.enable()

from CableDatabase import library as cdblib

def doLabels(data, type):
	print 'Content-Type: application/csv; name="labels.csv"'
	print 'Content-Disposition: attachment; filename="labels.csv"'
	print
	if type == 'all':
		for row in data:
			print cdblib.makeCableLabel(row, "A") + "," + cdblib.makeCableLabel(row, "B")
	elif type == 'A':
		for row in data:
			print cdblib.makeCableLabel(row, "A")
	elif type == 'B':
		for row in data:
			print cdblib.makeCableLabel(row, "B")
			 
	
	
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
	
	if cmd == "Download Labels (all)":
		doLabels(data, 'all')
	elif cmd == "Download Labels (A)":
		doLabels(data, 'A')
	elif cmd == "Download Labels (B)":
		doLabels(data, 'B')
	elif cmd == "Download Table Data":
		doTableData(data)
	else:
		print 'Content-Type: text/plain\n\n'
		raise Exception
	
if __name__ == "__main__":
	main();