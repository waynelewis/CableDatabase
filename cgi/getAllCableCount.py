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
		count = list()
		for c in allCables:
			if c[0] in allData[k]:
				count.append(dict(val = len(allData[k][c[0]])))
			else:
				count.append(dict(val = 0))
		dataList.append(dict(label = k, count = count))
			
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