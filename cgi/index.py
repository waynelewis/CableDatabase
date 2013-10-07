#!/usr/bin/env python

import cgitb, cgi, sys, time
cgitb.enable()

import pystache

from CableDatabase import library as cdblib

def main():
	# Setup the renderer to make the html list
	renderer = pystache.Renderer()
	
	footer = time.asctime(time.localtime())
	title = 'Index'
	sources = [{'rack' : a[0]} for a in cdblib.getAllAndSort('CableDatabase', 'sourceID')]
	
	
	data = renderer.render_path('index.mustache', {'footer' : footer,
	                                               'title'  : title,
	                                               'sourceList' : sources})
	
	print "Content-type: text/html\n\n";
	print data
	
if __name__ == "__main__":
	main()
	