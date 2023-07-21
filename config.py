import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["your-email@example.com"]

    CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    CLOUDFLARE_ACCESS_KEY_ID = os.environ.get("CLOUDFLARE_ACCESS_KEY_ID")
    CLOUDFLARE_SECRET_ACCESS_KEY = os.environ.get("CLOUDFLARE_SECRET_ACCESS_KEY")
    CLOUDFLARE_R2_BUCKET_NAME = os.environ.get("BUCKET_NAME")

