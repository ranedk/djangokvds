from path import path

APP_DIR = path(__file__).parent.abspath()

import sys
sys.path.append(APP_DIR.joinpath("python_modules").abspath())
sys.path.append(APP_DIR.joinpath("../python_modules/").abspath())

from dutils.common_settings import *

DEBUG = True
# DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Asia/Kolkata'

LANGUAGE_CODE = 'en-us'
SITE_ID = 1
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ke(_qq(&o&)eazut2ems(+bnhx#pe*-96h&0a9+(n*lezoei7x'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'kvds.utils.SimpleExceptionHandler',
)

ROOT_URLCONF = 'kvds.urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'kvds.app',
)

try:
    from local_settings import *
except ImportError: pass

