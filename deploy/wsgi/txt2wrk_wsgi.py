SITE_DIR = '/var/www/www.txt2wrk.net/src/txt2wrk'
import site
site.addsitedir(SITE_DIR)

import os
import sys
sys.path.append(SITE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'txt2wrk.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


