class Config:
    SECRET_KEY = "@lex.com2004Ricardious"


class DevelopmentConfig(Config):
    DEBUG = True


config = {"development": DevelopmentConfig}
