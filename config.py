#                                  .o88o.  o8o
#                                  888 `"  `"'
#  .ooooo.   .ooooo.  ooo. .oo.   o888oo  oooo   .oooooooo     oo.ooooo.  oooo    ooo
# d88' `"Y8 d88' `88b `888P"Y88b   888    `888  888' `88b       888' `88b  `88.  .8'
# 888       888   888  888   888   888     888  888   888       888   888   `88..8'
# 888   .o8 888   888  888   888   888     888  `88bod8P'  .o.  888   888    `888'
# `Y8bod8P' `Y8bod8P' o888o o888o o888o   o888o `8oooooo.  Y8P  888bod8P'     .8'
#                                               d"     YD       888       .o..P'
#                                               "Y88888P'      o888o      `Y8P'

import os

# Set absolute path of project directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN  = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'changeme'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'development.db')


# Configuration dictionary, provides easy access to different configurations
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
