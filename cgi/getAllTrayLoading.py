#!/usr/bin/env python

import cgitb, cgi, sys, time
cgitb.enable()

from CableDatabase import library as cdblib
import pystache

def main():
	
	alldata = cdblib.getAllTrayLoadings()
	
	divToShow = ['A','B','C','D','E','F']
	
	divList = [dict(divN=div) for div in divToShow]
	
	rdict = []
	for data in alldata:
		nPercentLoading = data[2]
		nCables = data[3]
		
		tClass = list()
		pVal = list()
		nVal = list()
		
		for div in divToShow:
		
			if not div in nPercentLoading:	
				pVal.append("0.00%")
				nPercentLoading[div] = 0.0
			else:
				pVal.append("{0:.1f}%".format(nPercentLoading[div] * 100))
		
			if nPercentLoading[div] > 0.5:
				tClass.append('style=background-color:#ff7d7d')
			elif (nPercentLoading[div] >= 0.4) and (nPercentLoading[div] <=0.5):
				tClass.append('style=background-color:#ffe4b3')
			elif nPercentLoading[div] < 0.4:
				tClass.append('')

			if not div in nCables:
				nVal.append("0")
			else:
				nVal.append("{0}".format(nCables[div]))

		d = dict(label = data[0],
				 loading = [dict(val=a,fmt=b) for a,b in zip(pVal,tClass)],
				 nCables = [dict(val=a,fmt=b) for a,b in zip(nVal,tClass)])
		rdict.append(d)
		
	renderer = pystache.Renderer()
	footer = time.asctime(time.localtime())
	data = renderer.render_path('trayLoading.mustache', {'title' : 'Cable Tray Loading',
											             'footer' : footer, 
											             'nDiv' : len(divList),
											             'divList' : divList,
														 'data' : rdict})
	print data


if __name__ == "__main__":
	print "Content-type: text/html\n\n";	
	main()