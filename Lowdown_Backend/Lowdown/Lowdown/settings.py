"""
Django settings for Lowdown project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '29#&*@&+kg*%vbfweuzs)l8z+ph*3j3jtz3)rp#zb9e-mzb(_q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'Facebook_App',
    'fb_iframe',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'fb_iframe.middleware.FacebookMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.google.GoogleOAuth2',
   'social.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'Lowdown.urls'

WSGI_APPLICATION = 'Lowdown.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_FACEBOOK_KEY = '578996548904671'
SOCIAL_AUTH_FACEBOOK_SECRET = '0d30c8516c93306cc60d555052f77adc'

SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
    'user_friends',
    'user_birthday',
    'user_about_me',
    'user_photos',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (       
    os.path.join(BASE_DIR, 'Facebook_App/templates'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/ubuntu/Lowdown_Backend/Lowdown/django.log',
            'formatter': 'verbose'
        },
       'our_scripts': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/ubuntu/Lowdown_Backend/Lowdown/our_scripts.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['django'],
            'propagate': True,
            'level':'DEBUG',
        },
        'Facebook_App': {
            'handlers': ['our_scripts'],
            'level': 'DEBUG',
        },
    }
}

#Facebook Stuff
FACEBOOK_APPLICATION_ID = "578996548904671"
FACEBOOK_APPLICATION_SECRET_KEY = "0d30c8516c93306cc60d555052f77adc"
FACEBOOK_APPLICATION_NAMESPACE = "lowdown_quiz_app"