import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///stocks.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    CACHE_TYPE = 'RedisCache'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY',"your_jwt_secret_key")
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL',"redis://localhost:6379/0")
    result_backend = os.getenv('result_backend',"redis://localhost:6379/1")
    JWT_BLOCKLIST_SERVER = os.getenv('JWT_BLOCKLIST_SERVER',"localhost")

    
    