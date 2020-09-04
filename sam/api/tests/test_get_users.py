import os
from moto import mock_dynamodb2
import boto3
import pytest
import json

@mock_dynamodb2
def test_get_users():
    """ Tests the get_users API's Lambda function """

    # Set up mock env variables
    setup_env_variables()

    # Create mock DynamoDB object
    dynamodb = boto3.resource('dynamodb', region_name = os.environ['AWS_DEFAULT_REGION'])

    # Create mock DynamoDB table
    table = dynamodb.create_table(
        TableName = os.environ['databaseName'],
        KeySchema = [
            {
                'AttributeName': 'github_username',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'github_username',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Put mock items for users into table
    table.put_item( Item = {"github_username": os.environ['userName1']})
    table.put_item( Item = {"github_username": os.environ['userName2']})
    table.put_item( Item = {"github_username": os.environ['userName3']})
    table.put_item( Item = {"github_username": os.environ['userName4']})

    # Import get_users Lambda function
    from ..get_users.get_users import lambda_handler

    # Create mock event to test the Lambda with
    event = {'queryStringParameters': {'limit': os.environ['limit']}}

    # Call the imported Lambda function with the mock event & null context
    # and put it into the 'response' object
    response = lambda_handler(event, 0)

    # Print Lambda response
    print("TEST - Response returned by Lambda: ", response)

    # Assert response from Lambda is returned only for first 2 users in mock
    assert response['statusCode'] == 200
    assert len(json.loads(response['body']))==2 

    event = {}

    # Call the imported Lambda function with the no query Params & null context
    # and put it into the 'response' object
    response = lambda_handler(event, 0)

    # Print Lambda response
    print("Response returned by Lambda: ", response)

    # Assert response from Lambda is returned for all 4 users in mock
    assert response['statusCode'] == 200
    assert len(json.loads(response['body']))==4

def setup_env_variables():
    """Mocked AWS Credentials for moto."""

    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ['databaseName'] = 'Users'
    os.environ['userName1'] = 'johndoe'
    os.environ['userName2'] = 'joanna'
    os.environ['userName3'] = 'becky'
    os.environ['userName4'] = 'rahul'
    os.environ['limit'] = '2'
    