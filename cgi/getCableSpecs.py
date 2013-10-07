#!/usr/bin/env python

import cgitb, cgi, sys, time
cgitb.enable()

import pystache

from CableDatabase import library as cdblib


def main():
	
	# Get the CGI information for the source
	# Exit the script if that information is not good. 
	form = cgi.FieldStorage()
	id = form.getvalue('id')
	if id is not None:
		mimeType,data = cdblib.getCableSpecSheet(id)
		if mimeType is not None:
			print "Content-type: {0}\n\n".format(mimeType);
			print data
			return
	
	print "Content-type: text/html\n\n";
	renderer = pystache.Renderer()
	print renderer.render_path('error.mustache', {'footer' : time.asctime(time.localtime()),
	                                              'title'  : "Error",
	                                              'body'   :  "Cannot find SPEC sheet for {0}".format(id)})
		
if __name__ == "__main__":
	main()