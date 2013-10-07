#!/usr/bin/env python

import cgitb, cgi, sys
cgitb.enable()

from CableDatabase import library as cdblib
import pystache

def makeDict(options):
	op = filter(None, options)
	l = [{'options' : a[0]} for a in op]
	return l

def main():
	
	# Setup the renderer to make the html list
	
	searchRows = list()
	for col,name in zip(cdblib.dbColumns, cdblib.columnNames):
		searchRow = dict()
		searchRow['sourceOptions'] = makeDict(cdblib.getAllAndSort('cableDatabase',col))
		searchRow['name'] = col
		searchRow['title'] = name
		searchRows.append(searchRow)
	
	renderer = pystache.Renderer()
	data = renderer.render_path('searchForm.mustache', {'searchRows' : searchRows,
		                                                'title' : 'Search Cable Database'})
	print data
if __name__ == "__main__":
	print "Content-type: text/html\n\n";
	main()