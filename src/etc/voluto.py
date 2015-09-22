
# Prepare project paths
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ETC_DIR = os.path.dirname(os.path.abspath(__file__))

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
# Webserver Configuration
# ========================

# Where the static files should be deployed
# (Expect files to be overwritten there)
STATIC_ROOT = os.path.join( BASE_DIR, "static" )

# The URL of the above folder, as exposed by your webserver
STATIC_URL = '/static/'

# ========================
# Local information
# ========================

# Default language to use
LANGUAGE_CODE = 'en-us'

# Server's timezone
TIME_ZONE = 'UTC'
