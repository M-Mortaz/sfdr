"""
Django settings for SFDR project.

Generated by "django-admin startproject" using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

from decouple import Config, RepositoryEnv

BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_FILE = BASE_DIR / "environments/development.env"
config = Config(RepositoryEnv(DOTENV_FILE))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", cast=str, default="changeme_asdkjfghjkasf54q543r6dfas*%sk")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    # Built-In apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Internal apps
    "apps.vendor",
    "apps.agent",
    "apps.order",
    "apps.trip",
    "apps.user",

    # Third party Apps
    'rest_framework',
    'corsheaders',
    'django_celery_beat',
    'drf_yasg',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "SFDR.urls"

WSGI_APPLICATION = "SFDR.wsgi.application"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MANIFEST_STRICT = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", cast=str, default="sfdr"),
        "USER": config("DB_USER", cast=str, default="sfdr"),
        "PASSWORD": config("DB_PASSWORD", cast=str, default="sfdr"),
        "HOST": config("DB_HOST", cast=str, default="localhost"),
        "PORT": config("DB_PORT", cast=int, default="5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []
AUTH_USER_MODEL = "user.User"
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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / STATIC_URL

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

RENEW_SHIPMENT_TIME_URI = "http://run.mocky.io/v3/122c2796-5df4-461c-ab75-87c1192b17f7"
RETRY_RENEW_SHIPMENT_TIME = 3
TIMEOUT_RENEW_SHIPMENT_TIME = 10  # in sec

LOGGING = {
    "disable_existing_loggers": False,
    "version": 1,
    "formatters": {
        "default": {
            "format": "{asctime} [{levelname}] {module} {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "logstash": {
            "level": "INFO",
            "class": "logstash.UDPLogstashHandler",
            "host": config("LOGSTASH_HOST", "localhost"),
            "port": config("LOGSTASH_UDP_PORT", 50_000, cast=int),
            "version": 1,  # Version of logstash event schema. Default value: 0 (for backward compatibility)
            "fqdn": False,  # Fully qualified domain name. Default value: false.
            "tags": None,  # list of tags like ["tag1", "tag2"]. Default: None.
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "logstash"],
            "level": "INFO"
        }
    }
}
