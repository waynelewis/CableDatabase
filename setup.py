#!/usr/bin/env python

from distutils.core import setup

#cgidir = '/var/www/CableDatabase'
cgidir = '/Users/wilkins/Sites/CableDatabase'

setup(name='CableDatabase',
      version='0.1',
      description='NSLS-II Cable Database Utilities',
      author='Stuart Wilkins',
      author_email='swilkins@bnl.gov',
      url='',
      packages=['CableDatabase'],
      data_files=[(cgidir, ['cgi/testcgi.py',
                            'cgi/getSourceList.py',
                            'cgi/searchForm.py',
                            'cgi/search.py',
                            'cgi/getAllTrayLoading.py',
                            'cgi/getFile.py',
                            'cgi/index.py',
                            'cgi/getCableSpecs.py',
                            'cgi/getData.py']),
                  (cgidir + '/css',['cgi/css/cdb.css']),
                  (cgidir + '/',  ['cgi/templates/getSourceList.mustache',
	      					       'cgi/templates/searchForm.mustache',
	      					       'cgi/templates/pullsheet.mustache',
	      					       'cgi/templates/tableData.mustache',
	      					       'cgi/templates/trayLoading.mustache',
	      					       'cgi/templates/header.mustache',
	      					       'cgi/templates/footer.mustache',
	      					       'cgi/templates/index.mustache',
	      					       'cgi/templates/error.mustache']),
                  (cgidir + '/images', ['cgi/images/nsls2logo.png'])]
     )
