#!/usr/bin/env python

from distutils.core import setup
import glob
import os

cgidir = '/var/www/CableDatabase'
cssdir = os.path.join(cgidir, 'css')
imgdir = os.path.join(cgidir, 'images')
#cgidir = '/Users/wilkins/Sites/CableDatabase'
cgifiles  = glob.glob('cgi/*.py') 
cgifiles += glob.glob('cgi/templates/*.mustache')
cssfiles = glob.glob('cgi/css/*.css') 
imgfiles = glob.glob('cgi/images/*.png')

setup(name='CableDatabase',
      version       ='0.1',
      description   ='NSLS-II Cable Database Utilities',
      author        ='Stuart Wilkins',
      author_email  ='swilkins@bnl.gov',
      url           ='',
      packages      =['CableDatabase'],
      package_data  ={'CableDatabase' : ['templates/*']},
      data_files    =[(cgidir, cgifiles),
			(imgdir, imgfiles),
			(cssdir, cssfiles)],
      scripts       =['scripts/cdb_make_files', 
      			      'scripts/cdb_import_data']
     )
