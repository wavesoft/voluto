################################################################
# Voluto - Volunteering Computing Administration & Organization
# Copyright (C) 2015 Ioannis Charalampidis
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
################################################################

# Prepare project paths
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ETC_DIR = os.path.join( BASE_DIR, "etc" )

# Import voluto configuration from 'etc' folder
sys.path.insert(0, ETC_DIR)
import etc.voluto as VOLUTO_CONFIG

############################################
### Imported settings from voluto config ###
############################################

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+o+k68t&k^h1o-8z!q(-omm!bs7qhskkb04je4bl5isxt$*y6w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = VOLUTO_CONFIG.DEBUG
ALLOWED_HOSTS = VOLUTO_CONFIG.ALLOWED_HOSTS

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = VOLUTO_CONFIG.DATABASES 


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = VOLUTO_CONFIG.STATIC_URL
STATIC_ROOT = VOLUTO_CONFIG.STATIC_ROOT

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = VOLUTO_CONFIG.LANGUAGE_CODE
TIME_ZONE = VOLUTO_CONFIG.TIME_ZONE

# Temporary directories

TEMP_DIR = VOLUTO_CONFIG.TEMP_DIR
FILE_UPLOAD_TEMP_DIR = os.path.join( TEMP_DIR, "upload" )
PROJECT_TEMP_DIR = os.path.join( TEMP_DIR, "projects" )

##########################################
### Non-editable project configuration ###
##########################################

# Application definition

INSTALLED_APPS = (

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'widget_tweaks',

    'voluto.ui',
    'voluto.projects',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'voluto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'voluto.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

USE_I18N = True
USE_L10N = True
USE_TZ = True
