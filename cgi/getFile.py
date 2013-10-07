#!/usr/bin/env python

import cgitb, cgi, sys, time
cgitb.enable()

from CableDatabase import library as cdblib

def main():
	
	# Get the CGI information for the source
	# Exit the script if that information is not good. 
	form = cgi.FieldStorage()
	id = form.getvalue('id')
	if id is None:
		print "Content-type: text/html\n\n";
		raise Exception
		
	mimeType,data = cdblib.getCableSpecSheet(id)
	#if data is None:
	#	print "Content-type: text/html\n\n";
	#		raise Exception
		
	print "Content-type: {0}\n\n".format(mimeType);
	print data
		
if __name__ == "__main__":
	main()