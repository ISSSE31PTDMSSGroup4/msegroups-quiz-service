import boto3
from moto import mock_dynamodb
import subprocess
import time
import signal
import os
import pytest
import psutil
import docker
from config import TestingConfig
 

from flask import Flask

# from utils.dynamodb_handler import CLIENT_NAME

@pytest.fixture
def client(monkeypatch):
    print("setting environment")
    monkeypatch.setenv("ENVIRONMENT", "testing") # config.py

    from app import app
    yield app.test_client()

@pytest.fixture(scope='session', autouse=True)
def create_quiz_table(client):
    # Start DynamoDB Local
    # dynamodb_local_process = subprocess.Popen(
    #     ["java", "-Djava.library.path=tests\dynamodb\DynamoDBLocal_lib", "-jar", "tests\dynamodb\DynamoDBLocal.jar", "-sharedDb","-port", "5051"]
    # )

    client = docker.from_env()
    dynamodb_container = client.containers.run(
        "amazon/dynamodb-local", # Dockerfile provided by AWS
        detach=True,
        ports={f"{TestingConfig.DYNAMODB_LOCAL_PORT}/tcp": TestingConfig.DYNAMODB_LOCAL_PORT},
        remove=True,
    )

    # print('creating')
    # for proc in psutil.process_iter():
    #     try:
    #         pinfo = proc.as_dict(attrs=['pid', 'name'])
    #         if pinfo['pid'] == 8000:
    #             return True
    #         else:
    #             continue
    #     finally: 
    #         continue
    
    # print('created')

    # Wait for DynamoDB Local to start
    # while dynamodb_local_process.poll() is None:
    #     print(dynamodb_local_process.poll())
    #     time.sleep(1)
    
    # print(dynamodb_local_process.poll())

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

# @pytest.fixture(scope='session', autouse=True)
# def create_quiz_table():
#     with mock_dynamodb():
#         dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
#         table = dynamodb.create_table(
#             TableName="QuizTest",
#             KeySchema=[{
#                 'AttributeName' : 'username', # Partition Key
#                 'KeyType' : 'HASH'
#             },
#             {
#                 'AttributeName' : 'quiz_id', # Sort Key
#                 'KeyType' : 'HASH'
#             }],
#             AttributeDefinitions=[{
#                 'AttributeName' : 'username',
#                 'AttributeType' : 'S'
#             },
#             {
#                 'AttributeName' : 'quiz_id',
#                 'AttributeType' : 'S'
#             }],
#             ProvisionedThroughput={
#                 'ReadCapacityUnits' : 1,
#                 'WriteCapacityUnits' : 1
#             },
#             GlobalSecondaryIndexes=[{
#                 'IndexName' : 'quiz_id-index',
#                 'KeySchema' : [{ 
#                     'AttributeName' : 'quiz_id', # Index
#                     'KeyType' : 'HASH'
#                 }],
#                 'Projection' : {
#                     'ProjectionType': 'ALL'
#                 },
#                 'ProvisionedThroughput' : {
#                     'ReadCapacityUnits' : 1,
#                     'WriteCapacityUnits' : 1
#                 }
#             }],
#         )
#         return table