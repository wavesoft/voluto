
# Prepare project paths
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ETC_DIR = os.path.join( BASE_DIR, "etc" )

# ========================
# Production Configuration
# ========================

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
ALLOWED_HOSTS = [ '127.0.0.1', 'localhost' ]

# ========================
# Database Configuration
# ========================

# Have a look here for more details:
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ETC_DIR, 'db.sqlite3'),
    }
}

# ========================
# Interop Configuration
# ========================

# URL to the Celery broker to use for interoperation
# with the other distributed components
INTEROP_BROKER = 'amqp://guest@localhost//'

# The shared folder with other components
INTEROP_SHARED_DIR = os.path.join( os.path.join( BASE_DIR, "temp" ), "shared" )

# ========================
# File Management
# ========================

# Scratch space where intermediate files are placed
TEMP_DIR = os.path.join( BASE_DIR, "temp" )

# ========================
# Webserver Configuration
# ========================

# Where the static files should be deployed
# (Expect files to be overwritten there)
STATIC_ROOT = os.path.join( BASE_DIR, "static" )

# The URL of the above folder, as exposed by your webserver
STATIC_URL = '/static/'

# ========================
# Locale configuration
# ========================

# Default language to use
LANGUAGE_CODE = 'en-us'

# Server's timezone
TIME_ZONE = 'UTC'
