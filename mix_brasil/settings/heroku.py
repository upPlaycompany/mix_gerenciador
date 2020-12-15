import environ


env = environ.ctx(
    DEBUG=(bool, False)
)

DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
