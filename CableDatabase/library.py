#!/usr/bin/env python

import MySQLdb as mdb
import math

### Here are the database parameters ###

dbHost = 'localhost'
dbUsers = 'root'
dbPassword = ''
dbName = 'NSLS2CableDatabase'

dbColumns = ['branch', 'vacuumSection', 'nemonic', 'sourceID', 'destinationId', 'cableType', 'cableUse']
columnNames =  ['Branch', 'Vacuum Section', 'Nemonic', 'Source ID', 'Destination ID', 'Cable Type', 'Cable Use']

### End database parameters ###

def connectToDatabase():
    """Connect to SQL database and return connection object"""
    try:
        con = mdb.connect(dbHost, dbUsers,dbPassword,dbName, 3306); 
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        return None
    return con

def makeCableLabel(data, end):
    """Make cable label from initial data

    Assumes that data is in form

    0 : ID
    1 : Branch
    2 : Source ID
    3 : Destination ID

    end is the string to terminate, such as 'A'
    """
    return "23ID:%d-%s-%s-%s-%s" % (data[1], data[0], data[2], data[3], end)

def getCableSpecSheet(id):
	"""Return PDF file of cable spec sheet"""
	db =connectToDatabase()
	cur = db.cursor()
	cur.execute("SELECT a.mimetype,a.data from Files a, CableTypes b WHERE b.cableType = '{0}' AND a.id = b.specFile".format(id))
	rows = cur.fetchone()
	if rows is None:
		return None, None	
	return rows

def getSourceConnectionList(source):
    """Get source connection list from database and return rows"""
    db=connectToDatabase()
    cur = db.cursor()
    cur.execute("SELECT a.id,a.branch,a.sourceID,a.destinationID,a.cableType,b.cableLongName,a.cableUse,a.sourceConnection,a.destinationConnection FROM CableDatabase a, CableTypes b WHERE a.sourceID = \"%s\" AND a.cableType = b.cableType" % source)
    rows = cur.fetchall()
    db.close()
    return rows
    
def getPullSheetData(keys):
	"""Get Pullsheet Data from search made up of keys"""
	rows = doCableSearch(['a.sourceID, a.cablePath, a.destinationID'], keys)
	return rows
	
def getAllData(keys):
	"""Get all columns of use from the database"""
	rows = doCableSearch(['a.sourceID, a.destinationID, a.cablePath, a.cableDwgNo, a.cableInstalled'], keys)
	return rows
	
def getData(ids):
	"""Get all data based on list of ids"""
	db = connectToDatabase()
	cur = db.cursor()
	cmd = "SELECT id,branch,sourceID,destinationID FROM CableDatabase WHERE id in ({0})".format(",".join(ids))
	cur.execute(cmd)
	rows = cur.fetchall()
	cur.close()
	db.close()
	return rows
	
def doCableSearch(returned, keys):
	"""Do search of cable database and return ids of results"""
	db = connectToDatabase()
	cur = db.cursor()
	cmd = "SELECT a.id,a.branch,a.sourceID,a.destinationID,a.cableType,b.cableLongName,a.cableUse,{0} FROM CableDatabase a, CableTypes b WHERE a.cableType = b.cableType ".format(",".join(returned))
	
	s = []
	for key,arg in keys.items():
		if arg is not None:
			if type(arg) is not list:
				a = ["'" + arg + "'"]
			else:
				a = ["'" + aa + "'" for aa in arg]
			c = 'a.%s in (' % key
			c += ",".join(a)
			c += ")"
			s.append(c)
	if len(s):
		cmd += " AND " + " AND ".join(s)
		
	cur.execute(cmd)
	rows = cur.fetchall()
	cur.close()
	db.close()
	return rows


def getAllAndSort(table, field):
	"""Return all the unique values from a field"""
	db = connectToDatabase()
	cur = db.cursor()
	cur.execute("SELECT DISTINCT({0}) AS {0} FROM {1} ORDER BY {0};".format(field, table))
	rows = cur.fetchall()
	cur.close()
	db.close()
	return rows

def getAllTrayLoadings():
	db =connectToDatabase()
	cur = db.cursor()
	cur.execute("SELECT id from CableTrays")
	rows = cur.fetchall()
	
	allrtn = []
	for row in rows:
		rtn = calculateTrayLoading(row[0])
		if rtn is not None:
			allrtn.append([row[0]] + list(rtn))
	return allrtn
	
def calculateTrayLoading(trayTag):
	"""Calculate the tray loading"""
	# To calculate the tray loading for a given tray we first do
	# a regex on the database to get the number of cables.
	
	db =connectToDatabase()
	cur = db.cursor()
	rexp = "'[[:<:]]{0}[A-Z][[:>:]]|[[:<:]]{0}[[:>:]]'".format(trayTag)
		 	
	cur.execute("SELECT a.id, b.cableDiameter, b.defaultDivider, a.cablePath, a.sourceID, a.destinationID from CableDatabase a, CableTypes b where a.cableType = b.cableType and (a.cablePath REGEXP {0} OR a.destinationID = {0});".format(trayTag))
	rows = cur.fetchall()
	
	if rows is None:
		return None
		
	loading = dict()
	count = dict()
	noneCount = 0;
	
	for row in rows:
		div = row[2]
		dia = row[1]
		if dia is None:
			noneCount += 1;
			continue
		dia = math.pi * math.pow((row[1]/2.0),2)
		if div in loading:
			loading[div] += dia
			count[div] += 1
		else:
			loading[div] = dia
			count[div] = 1
	
	#for row in rows:
	#	print row	
		
	# Now get divider schedule

	if len(loading) == 0:
		return None
	
	cmd = "SELECT " + ",".join(["div{0}Size".format(a) for a in loading.keys()]) + " FROM CableTrays WHERE id = {0}".format(trayTag)

	cur.execute(cmd)
	trow = cur.fetchall()[0] # Use first row, there is only one!
	
	# Now go through all the dividers that we have and get the areas to calculate
	# percentage fill
	
	area = dict()
	percentFill = dict()
	for a,b in zip(loading.keys(), trow):
		area[a] = b
		percentFill[a] = loading[a] / area[a]
	
	return (loading, percentFill, count, noneCount)
