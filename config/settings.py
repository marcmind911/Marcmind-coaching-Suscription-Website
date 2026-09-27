import os
from pathlib import Path

from dotenv import load_dotenv
import dj_database_url


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# ENVIRONMENT VARIABLES
# =========================================================

load_dotenv(BASE_DIR / ".env")


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "unsafe-development-key"
)

DEBUG = (
    os.environ.get("DEBUG", "False").lower() == "true"
    and os.environ.get("VERCEL") != "1"
)


# =========================================================
# ALLOWED HOSTS
# =========================================================

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "marcmind.com,www.marcmind.com,.vercel.app,localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]


# =========================================================
# INSTALLED APPS
# =========================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "core",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise for static files
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = "config.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# DATABASE
# =========================================================

DATABASE_URL = next(
    (
        os.environ.get(name, "").strip()
        for name in (
            "DATA_DATABASE_URL",
            "DATA_POSTGRES_PRISMA_URL",
            "DATA_POSTGRES_URL",
            "DATA_POSTGRES_URL_NON_POOLING",
            "DATABASE_URL",
        )
        if os.environ.get(name, "").strip()
    ),
    "",
)


if DATABASE_URL:

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }

    if DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql":

        from django.core.exceptions import ImproperlyConfigured

        raise ImproperlyConfigured(
            "The configured database must be PostgreSQL."
        )


elif os.environ.get("DJANGO_USE_SQLITE", "").lower() == "true":

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


else:

    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured(
        "A PostgreSQL DATABASE_URL is required in production. "
        "Configure DATABASE_URL or DATA_DATABASE_URL."
    )


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# WhiteNoise
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# LOGIN / LOGOUT
# =========================================================

LOGIN_REDIRECT_URL = "home"

LOGOUT_REDIRECT_URL = "home"


# =========================================================
# EMAIL
# =========================================================

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "hello@example.com",
)


# =========================================================
# STRIPE
# =========================================================

STRIPE_SECRET_KEY = os.environ.get(
    "STRIPE_SECRET_KEY",
    ""
).strip()


STRIPE_WEBHOOK_SECRET = os.environ.get(
    "STRIPE_WEBHOOK_SECRET",
    ""
).strip()


# =========================================================
# PAYSTACK
# =========================================================

PAYSTACK_SECRET_KEY = os.environ.get(
    "PAYSTACK_SECRET_KEY",
    ""
).strip()


# =========================================================
# WHATSAPP
# =========================================================

WHATSAPP_NUMBER = os.environ.get(
    "WHATSAPP_NUMBER",
    ""
).strip()


# =========================================================
# SITE URL
# =========================================================

SITE_URL = os.environ.get(
    "SITE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


# =========================================================
# CSRF
# =========================================================

CSRF_TRUSTED_ORIGINS = [
    "https://marcmind.com",
    "https://www.marcmind.com",
]


# =========================================================
# HTTPS / SECURITY
# =========================================================

if not DEBUG:

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )


# =========================================================
# CLICKJACKING PROTECTION
# =========================================================

X_FRAME_OPTIONS = "DENY"
