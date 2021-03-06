"""
Django settings for Lowdown project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# To get instance-specific configuration values.
import idconfig

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
    'django_mobile',
#    'fb_iframe',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'fb_iframe.middleware.FacebookMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
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
   'django_mobile.context_processors.flavour',
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

SOCIAL_AUTH_FACEBOOK_KEY = idconfig.FACEBOOK_APP_ID
SOCIAL_AUTH_FACEBOOK_SECRET = idconfig.FACEBOOK_APP_SECRET
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
    'user_about_me',
    'user_actions.books',
    'user_actions.music',
    'user_actions.news',
    'user_actions.fitness',
    'user_actions.video',
    'user_activities',
    'user_birthday',
    'user_education_history',
    'user_events',
    'user_friends',
    'user_games_activity',
    'user_groups',
    'user_hometown',
    'user_interests',
    'user_likes',
    'user_location',
    'user_photos',
    'user_relationship_details',
    'user_relationships',
    'user_religion_politics',
    'user_status',
    'user_tagged_places',
    'user_videos',
    'user_website',
    'user_work_history',
    # Extended
    'read_friendlists',
    #Publish actions
    'publish_actions',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/ubuntu/CS194Project/Lowdown_Backend/Lowdown/static/'

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
            'filename': idconfig.GIT_ROOT + 'Lowdown_Backend/Lowdown/django.log',
            'formatter': 'verbose'
        },
       'Facebook_App': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': idconfig.GIT_ROOT + 'Lowdown_Backend/Lowdown/lowdown.log',
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
            'handlers': ['Facebook_App'],
            'level': 'DEBUG',
        },
    }
}
