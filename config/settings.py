import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-development-key")
DEBUG = (
    os.environ.get("DEBUG", "False").lower() == "true"
    and os.environ.get("VERCEL") != "1"
)
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS","marcmind.com,www.marcmind.com").split(",")
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "core"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
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
        )
    }
    if DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql":
        from django.core.exceptions import ImproperlyConfigured

        raise ImproperlyConfigured("The configured database must be PostgreSQL.")
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
        "A PostgreSQL DATABASE_URL is required in production. Configure "
        "DATABASE_URL or DATA_DATABASE_URL for this deployment."
    )


AUTH_PASSWORD_VALIDATORS = [{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}, {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}, {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"}, {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE = "en"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "core"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend",)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "hello@example.com")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "").strip()

STRIPE_WEBHOOK_SECRET = os.environ.get(
    "STRIPE_WEBHOOK_SECRET", ""
)

PAYSTACK_SECRET_KEY = os.environ.get(
    "PAYSTACK_SECRET_KEY", ""
)

WHATSAPP_NUMBER = os.environ.get(
    "WHATSAPP_NUMBER", ""
)

SITE_URL = os.environ.get(
    "SITE_URL",
    "http://127.0.0.1:8000"
)
CSRF_TRUSTED_ORIGINS = ["https://marcmind.com","https://www.marcmind.com",  "https://*.vercel.app",]
