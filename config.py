import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add any other global configurations here


class DevelopmentConfig(Config):
    DEBUG = True
    # Add any development-specific configurations here


class ProductionConfig(Config):
    DEBUG = False
    # Add any production-specific configurations here
