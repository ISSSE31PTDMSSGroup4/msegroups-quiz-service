import os

class Config(object):
    DEBUG = False

class ProductionConfig(Config):
    TESTING               = False
    AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    DYNAMODB_ENDPOINT_URL = None  # For production, use the actual DynamoDB endpoint URL

class TestingConfig(Config):
    TESTING               = True
    AWS_ACCESS_KEY_ID     = None
    AWS_SECRET_ACCESS_KEY = None
    DYNAMODB_LOCAL_PORT   = 8000 # fixed port used by dynamodb-local [Dockerfile provided by AWS]
    DYNAMODB_ENDPOINT_URL = f'http://localhost:{DYNAMODB_LOCAL_PORT}'  # Local DynamoDB for testing

config = {
    'testing': TestingConfig,
    'production': ProductionConfig
}

def get_config(env):
    return config.get(env)