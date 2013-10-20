import pystache
import os

mksChan   = {'A' : 1, 'A1' : 1, 'A2' : 2,
			     'B' : 3, 'B1' : 3, 'B2' : 4,
			     'C' : 4, 'C1' : 4, 'C2' : 5}
			   
mksRelays = {'A'  : [1,2,3,4],
				 'A1' : [1,2],
				 'A2' : [3,4],
				 'B'  : [5,6,7,8],
				 'B1' : [5,6],
				 'B2' : [7,8],
				 'C'  : [9,10,11,12],
				 'C1' : [9,10],
				 'C2' : [11,12]}

gammaChan  = { '1' : 1 , '2' : 1, '3' : 2, '4' : 2}

gammaRelays = {'1' : [1,2,3,4], '2' : [1,2,3,4],
	           '3' : [5,6,7,8], '4' : [5,6,7,8]}

chanDict =  {'mksvgc'    : mksChan,
			 'gammaipc'  : gammaChan}
			
relayDict = {'mksvgc'    : mksRelays,
	         'gammaipc'  : gammaRelays}

def render(template, ofile, dictionary):
	"""Render using mustache the dictionary from a template file"""
	renderer = pystache.Renderer()
	templateFile = os.path.join(os.path.abspath(os.path.dirname(__file__)),'templates/{0}'.format(template))
	data = renderer.render_path(templateFile, dictionary)
	f = open(ofile, 'w')
	f.write(data)
	f.close()
	
def makeArchiverDict(sys, rows, name, signals):
	"""Make dictionary to add to archiver"""
	pvs = list()
	for row in rows:
		if row[2]:
			for signal in signals:
				pv = dict(pv=sys + '{' + row[2] + '}' + signal)
				pvs.append(pv)
			
	return [dict(name = name, channels = pvs)]

def makeSimpleDictionary(sys,rows, ports, source = False, unique = False):
	"""Make Dictionary from all devices in list"""

	devices = list()	
	deviceList = list()
	for row in rows:
		if source:
			d = row[1].split('-')[0]
		else:
			d = row[2]
			
		if d:
			d = '{' + d + '}'
			if not (unique and (d in deviceList)):
				dev = dict()
				dev['sys']  = sys
				dev['dev']  = d
				dev['port'] = ports['{' + row[1].split('-')[0] + '}']
				devices.append(dev)
				deviceList.append(d)
	return devices

def makeVacuumDictionary(vtype, sys,rows,ports):
	"""Make Dictionary for substitution file"""
	gauges = list()
	relays = list()
	for row in rows:
		# Each row is a CC Gauge
		# First do the actual Gauge
		
		if (row[1] is not '') and (row[2] is not ''):
			gauge = dict()
			gauge['sys'] = sys
			gauge['dev'] = '{' + row[2] + '}'
			gauge['chan'] = chanDict[vtype][row[1].split('-')[1]]
			gauge['cntl'] = '{' + row[1].split('-')[0] + '}'
			gauge['port'] = ports[gauge['cntl']]
			gauges.append(gauge)
			
			# Now set the relay
			for spnum in relayDict[vtype][row[1].split('-')[1]]:
				relay = gauge.copy()
				relay['spnum'] = spnum
				relays.append(relay)
			
	return gauges, relays
	
