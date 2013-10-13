#!/usr/bin/env python

import cgitb, cgi, sys, time, urllib
cgitb.enable()

import pystache

from CableDatabase import library as cdblib

def main():
	# Get the CGI information for the source
	# Exit the script if that information is not good. 
	form = cgi.FieldStorage()
	src = urllib.unquote(form.getvalue('source'))
	if src is None:
		raise Exception

	# Get the source list data from the database
	rows = cdblib.getSourceConnectionList(src)
	if rows is None:
		raise Exception

	# transpose the data
	rdict = [dict(label = cdblib.makeCableLabel(row, "A"),
				  type = row[4],
				  longType = row[5],
				  use = row[6],
				  sourceconn = row[7],
				  destconn = row[8])
			 for row in rows]

	# Setup the renderer to make the html list
	renderer = pystache.Renderer()
	
	footer = time.asctime(time.localtime())
	title = 'Source Connection List for {0}'.format(src)
	
	data = renderer.render_path('getSourceList.mustache', 
						        {'source' : src,
								 'footer' : footer,
								 'title'  : title,
				 				 'sourceList' : rdict})	
	print data
	
if __name__ == "__main__":
	print "Content-type: text/html\n\n";	
	main()