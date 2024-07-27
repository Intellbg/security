import os
from dotenv import load_dotenv

# Uso de variables de entorno para el manejo de secretos
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "1"
MY_DOMAIN = os.getenv("DOMAIN")

RESET_TIME_CONS = 12

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")


INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "django_smtp_ssl",
    "api",
    "accounts",
    "checkpoint",
    "administrator",
)

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
)

ROOT_URLCONF = "django_project.urls"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework_datatables.renderers.DatatablesRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework_datatables.pagination.DatatablesPageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework_datatables.filters.DatatablesFilterBackend",
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_project.wsgi.application"


# Inclusión de funcionalidad para que la aplicación pueda consultar a replicas de la base de datos
# para proporcionar mayor disponibilidad
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "USER": os.getenv("DB_USERNAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
    },
    "replica": {
        "ENGINE": os.getenv("DB_ENGINE_R"),
        "NAME": os.getenv("DB_NAME_R"),
        "HOST": os.getenv("DB_HOST_R"),
        "PORT": os.getenv("DB_PORT_R"),
        "USER": os.getenv("DB_USERNAME_R"),
        "PASSWORD": os.getenv("DB_PASSWORD_R"),
    },
}
# DATABASE_ROUTERS = ["django_project.db.PrimaryReplicaRouter"]

# Inclusión de configuración de sesiones
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_L10N = True
USE_TZ = False
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "/static/"

TASTYPIE_DEFAULT_FORMATS = ["json"]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_USE_SSL = True
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


PUSHER_APP_ID = os.getenv("PUSHER_APP_ID")
PUSHER_KEY = os.getenv("PUSHER_KEY")
PUSHER_SECRET = os.getenv("PUSHER_SECRET")

# Configuración de loggers de auditoria para los distintos módulos
LOGGING = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "{asctime} {levelname} {module} {process} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
        "server": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": BASE_DIR + "/logs/server.log",
            "when": "midnight",
            "backupCount": 20,
            "formatter": "default",
        },
        "accounts": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": BASE_DIR + "/logs/accounts.log",
            "when": "midnight",
            "formatter": "default",
            "backupCount": 30,
        },
        "api": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": BASE_DIR + "/logs/api.log",
            "when": "midnight",
            "formatter": "default",
            "backupCount": 20,
        },
        "checkpoint": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": BASE_DIR + "/logs/checkpoint.log",
            "when": "midnight",
            "formatter": "default",
            "backupCount": 20,
        },
        "administrator": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": BASE_DIR + "/logs/administrator.log",
            "when": "midnight",
            "formatter": "default",
            "backupCount": 7,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "server": {
            "handlers": ["console", "server"],
            "propagate": True,
            "level": "INFO",
        },
        "administrator": {
            "handlers": ["console", "administrator"],
            "level": "INFO",
        },
        "checkpoint": {
            "handlers": ["console", "checkpoint"],
            "level": "INFO",
        },
        "api": {
            "handlers": ["console", "api"],
            "level": "INFO",
        },
        "accounts": {
            "handlers": ["console", "accounts"],
            "level": "INFO",
        },
    },
}

# Inclusión de políticas para contraseñas de usuarios
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 10,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
