import boto3
import pytest
import docker
from config import TestingConfig

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    monkeypatch.setenv("ENVIRONMENT", "testing") # config.py

    from app import app
    yield app.test_client()

@pytest.fixture(scope='session', autouse=True)
def create_quiz_table(client):
    client = docker.from_env()
    dynamodb_container = client.containers.run(
        "amazon/dynamodb-local", # Dockerfile provided by AWS
        detach=True,
        ports={f"{TestingConfig.DYNAMODB_LOCAL_PORT}/tcp": TestingConfig.DYNAMODB_LOCAL_PORT},
        remove=True,
    )

    db_client = boto3.client('dynamodb',endpoint_url= TestingConfig.DYNAMODB_ENDPOINT_URL) # f'http://localhost:{TestingConfig.DYNAMODB_LOCAL_PORT}')
    table_schema = {
        'TableName':"Quiz",
        'KeySchema':[{
            'AttributeName' : 'username', # Partition Key
            'KeyType' : 'HASH'
        },
        {
            'AttributeName' : 'quiz_id', # Sort Key
            'KeyType' : 'RANGE'
        }],
        'AttributeDefinitions':[{
            'AttributeName' : 'username',
            'AttributeType' : 'S'
        },
        {
            'AttributeName' : 'quiz_id',
            'AttributeType' : 'S'
        }],
        'ProvisionedThroughput':{
            'ReadCapacityUnits' : 1,
            'WriteCapacityUnits' : 1
        },
        'GlobalSecondaryIndexes':[{
            'IndexName' : 'quiz_id-index',
            'KeySchema' : [{ 
                'AttributeName' : 'quiz_id', # Index
                'KeyType' : 'HASH'
            }],
            'Projection' : {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput' : {
                'ReadCapacityUnits' : 1,
                'WriteCapacityUnits' : 1
            }
        }],
    }
    table = db_client.create_table(**table_schema)
    yield table

    # Teardown: Stop DynamoDB Local Docker container
    dynamodb_container.stop()
