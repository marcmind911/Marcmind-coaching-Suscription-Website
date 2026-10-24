import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-development-key")
DEBUG = (
    os.environ.get("DEBUG", "False").lower() == "true"
    and os.environ.get("VERCEL") != "1"
)
configured_hosts = os.environ.get("ALLOWED_HOSTS", "marcmind.com,www.marcmind.com").split(",")
vercel_hostname = os.environ.get("VERCEL_URL", "").strip()
ALLOWED_HOSTS = [host.strip() for host in configured_hosts if host.strip()]
if vercel_hostname:
    ALLOWED_HOSTS.append(vercel_hostname)
if os.environ.get("VERCEL") == "1":
    ALLOWED_HOSTS.append(".vercel.app")
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "core"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASE_URL_VARIABLES = (
    "DATA_DATABASE_URL",
    "DATA_POSTGRES_PRISMA_URL",
    "DATA_POSTGRES_URL",
    "DATA_POSTGRES_URL_NON_POOLING",
    "DATABASE_URL",
)
DATABASES = None

for variable_name in DATABASE_URL_VARIABLES:
    database_url = os.environ.get(variable_name, "").strip()
    if not database_url:
        continue

    database_config = dj_database_url.parse(
        database_url,
        conn_max_age=600,
        conn_health_checks=True,
    )
    if database_config["ENGINE"] == "django.db.backends.postgresql":
        DATABASES = {"default": database_config}
        break

# Neon integrations may expose connection fields instead of a single URL.
# Build the URL at runtime so Django can boot in every Vercel environment.
if DATABASES is None:
    database_host = (
        os.environ.get("DATA_PGHOST")
        or os.environ.get("DATA_PGHOST_UNPOOLED")
        or os.environ.get("DB_HOST")
    )
    database_name = (
        os.environ.get("DATA_PGDATABASE")
        or os.environ.get("DATA_POSTGRES_DATABASE")
        or os.environ.get("DB_NAME")
    )
    database_user = os.environ.get("DATA_PGUSER") or os.environ.get("DB_USER")
    database_password = os.environ.get("DATA_PGPASSWORD") or os.environ.get("DB_PASSWORD")

    if all((database_host, database_name, database_user, database_password)):
        database_url = (
            f"postgresql://{quote_plus(database_user)}:{quote_plus(database_password)}"
            f"@{database_host}/{quote_plus(database_name)}?sslmode=require"
        )
        DATABASES = {
            "default": dj_database_url.parse(
                database_url,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }

if DATABASES is None:
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured(
        "A PostgreSQL database URL is required. Configure DATABASE_URL "
        "or DATA_DATABASE_URL with your Neon connection string."
    )


AUTH_PASSWORD_VALIDATORS = [{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}, {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}, {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"}, {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE = "en"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend",)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "hello@example.com")

# Prefer the explicitly configured live key in production, while retaining the
# standard key name as a fallback for existing environments.
STRIPE_SECRET_KEY = (
    os.environ.get("STRIPE_LIVE_SECRET_KEY")
    or os.environ.get("STRIPE_SECRET_KEY")
    or os.environ.get("STRIPE_TEST_SECRET_KEY")
    or ""
).strip()

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
CSRF_TRUSTED_ORIGINS = [
    "https://marcmind.com",
    "https://www.marcmind.com",
    "https://*.vercel.app",
]
