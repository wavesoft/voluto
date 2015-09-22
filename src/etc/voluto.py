
# Prepare project paths
import os
ETC_DIR = os.path.dirname(os.path.abspath(__file__))

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ETC_DIR, 'db.sqlite3'),
    }
}
