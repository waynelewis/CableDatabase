#!/usr/bin/env python

from distutils.core import setup
import glob

#cgidir = '/var/www/CableDatabase'
cgidir = '/Users/wilkins/Sites/CableDatabase'
cgifiles  = glob.glob('cgi/*.py') 
cgifiles += glob.glob('cgi/css/*.css') 
cgifiles += glob.glob('cgi/templates/*.mustache')

setup(name='CableDatabase',
      version       ='0.1',
      description   ='NSLS-II Cable Database Utilities',
      author        ='Stuart Wilkins',
      author_email  ='swilkins@bnl.gov',
      url           ='',
      packages      =['CableDatabase'],
      package_data  ={'CableDatabase' : ['templates/*']},
      data_files    =[(cgidir, cgifiles)],
      scripts       =['scripts/cdb_make_files', 
      			      'scripts/cdb_import_data']
     )
