import environ


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env("SECRET_KEY")
"""$2y$12$QU2vB3P1xkNEncLIGfNVgOoICDg2cyWYQDtqCvKMDj.Y9CUHWgrIm possivel erro heroku config:set DISABLE_COLLECTSTATIC=1"""
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
