import boto3
import pytest
import docker
from config import TestingConfig

import subprocess

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "testing") # config.py

    from app import app
    yield app.test_client()

@pytest.fixture(scope='session', autouse=True)
def create_quiz_table():
    client = docker.from_env()
    dynamodb_container = client.containers.run(
        "amazon/dynamodb-local", # Dockerfile provided by AWS
        detach=True,
        ports={f"{TestingConfig.DYNAMODB_LOCAL_PORT}/tcp": TestingConfig.DYNAMODB_LOCAL_PORT},
        remove=True,
    )

    # Start DynamoDB Local
    # subprocess.Popen(
    #     ["java", "-Djava.library.path=tests\dynamodb\DynamoDBLocal_lib", "-jar", "tests\dynamodb\DynamoDBLocal.jar", "-sharedDb","-port", "5051"]
    # )

    db_client = boto3.client('dynamodb',endpoint_url= TestingConfig.DYNAMODB_ENDPOINT_URL)
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
