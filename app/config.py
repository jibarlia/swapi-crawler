from environs import Env

env = Env()
env.read_env()

DATABASE_URL = env.str("DATABASE_URL")
DEBUG = env.bool("DEBUG", default=False)
APP_NAME = env.str("APP_NAME", default="public-api-crawler-template")