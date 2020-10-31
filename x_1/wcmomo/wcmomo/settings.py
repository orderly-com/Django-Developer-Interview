"""
Django settings for wcmomo project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""


from pathlib import Path
# Michael
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # -> projname/projname/


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xu0-97+jb@nv2%vcz)v6ev)b7rydi@&6n-ukx0he^l2!%i*e&0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [
    # Michael
    # '*',
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # addons.....................
    'app.apps.AppConfig',
    'django_q',
    'rangefilter',
]


# for django_q:
Q_CLUSTER = {
    'name': 'dq',
    # 'workers': 2,
    # 'daemonize_workers': True,
    # 'recycle': 500,
    # 'max_rss': None,
    'timeout': 300,
    # 'ack_failures': False,
    'max_attempts': 0,
    'retry': 310,
    # 'compress': False,
    # 'save_limit': 250,
    # Guard loop sleep in seconds, must be greater than 0 and less than 60.
    # 'guard_cycle': 1,
    # 'sync': False,

    # Defaults to workers**2.
    # can help balance the workload and the memory overhead of each individual cluster
    'queue_limit': 5,
    # 'label': 'Django Q',
    'catch_up': False,  # !!!!

    'orm': 'default',
    'cpu_affinity': 2,
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wcmomo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Michael
            BASE_DIR / 'templates',
        ],
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


WSGI_APPLICATION = 'wcmomo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# PGDB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jg1',
        'USER': 'jg1',
        'PASSWORD': 'jg1',
        'HOST': 'localhost',
        'POST': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/


# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hant'


# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Taipei'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'


# Michael
LOGIN_REDIRECT_URL = '/'  # after login, redirect


# Michael
STATICFILES_DIRS = [
    BASE_DIR / STATIC_URL,  # os.path.join(BASE_DIR, "static"),
]
