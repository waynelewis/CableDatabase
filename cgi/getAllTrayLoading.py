#!/usr/bin/env python

import cgitb, cgi, sys, time
cgitb.enable()

from CableDatabase import library as cdblib
import pystache

def main():
	
	alldata = cdblib.getAllTrayLoadings()
	
	rdict = []
	for data in alldata:
		nPercentLoading = data[2]
		colour = dict()
		percentLoading = dict()
		for div in ['A','B','C','D']:
			if not div in nPercentLoading:	
				percentLoading[div] = "0.00%"
				nPercentLoading[div] = 0.0
			else:
				percentLoading[div] = "{0:.1f}%".format(nPercentLoading[div] * 100)
		
			if nPercentLoading[div] > 0.5:
				colour[div] = "red"
			elif (nPercentLoading[div] >= 0.4) and (nPercentLoading[div] <=0.5):
				colour[div] = "#ffcc00"
			elif nPercentLoading[div] < 0.4:
				colour[div] = "#33cc00"

		d = dict(label = data[0],
				 A = percentLoading['A'],
				 B = percentLoading['B'],
				 C = percentLoading['C'],
				 D = percentLoading['D'],
				 Acolour = colour['A'],
				 Bcolour = colour['B'],
				 Ccolour = colour['C'],
				 Dcolour = colour['D'])
		rdict.append(d)
		
	renderer = pystache.Renderer()
	footer = time.asctime(time.localtime())
	data = renderer.render_path('trayLoading.mustache', {'title' : 'Cable Tray Loading',
											             'footer' : footer, 
														 'loadingList' : rdict})	
	print data


if __name__ == "__main__":
	print "Content-type: text/html\n\n";	
	main()