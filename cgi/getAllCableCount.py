#!/usr/bin/env python

import cgitb, cgi, sys, time
cgitb.enable()

from CableDatabase import library as cdblib
import pystache

def main():
	
	allData = cdblib.getAllCableCount()	
	allCables = cdblib.getAllCableTypes()
	
	dataList = list()
	for k in allData: # Over all tray segments
		dataList.append(dict(label = k, count = [dict(val = len(allData[k][c[0]])) for c in allCables]))
			
	renderer = pystache.Renderer()
	footer = time.asctime(time.localtime())
	html = renderer.render_path('trayCableCount.mustache', {'title'     : 'Cable Tray Count',
											                'footer'    : footer, 
											                'nCables'   : len(allData),
											                'cableList' : [dict(id = a[0], desc = a[1]) for a in allCables],
											                'data'		: dataList})
	print html


if __name__ == "__main__":
	print "Content-type: text/html\n\n";	
	main()