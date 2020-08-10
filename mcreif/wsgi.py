# This file contains the WSGI configuration required to serve up your
# web application at http://pruebamcreif.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Django project

import os
import sys
from dj_static import Cling

# add your project directory to the sys.path
project_home = '/home/amzrecov/amzrecovery3'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'mcreif.settings'


# serve django via WSGI
from django.core.wsgi import get_wsgi_application
application = Cling(get_wsgi_application())

