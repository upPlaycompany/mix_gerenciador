import environ

import mix_brasil.mix_brasil.settings.base

env = environ.Env(
    DEBUG=(bool, False)
)

DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {
    "default": env.db(),
}