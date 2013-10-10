#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import markup

import cgitb, cgi
cgitb.enable()





if __name__ == "__main__":
    db = connectToDatabase()
    getSourceConnectionList(db, "RG:C1")
    

