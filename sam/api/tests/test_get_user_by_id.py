import os
from moto import mock_dynamodb2
import boto3
import pytest


@mock_dynamodb2
def test_get_user_by_id():
    """ Tests the get_user_by_id API's Lambda function """

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

    # Put mock item into table
    table.put_item( Item = {"github_username": os.environ['userName']})

    # Import get_user_by_id Lambda function
    from ..get_user_by_id.get_user_by_id import lambda_handler

    # Create mock event to test the Lambda with
    event = {'queryStringParameters': {'username': os.environ['userName']}}

    # Call the imported Lambda function with the mock event & null context
    # and put it into the 'response' object
    response = lambda_handler(event, 0)

    # Print Lambda response
    print("TEST - Response returned by Lambda: ", response)

    # Assert response from Lambda is correct
    assert response['statusCode'] == 200
    assert response['body'] == '{"github_username": "%s"}' %(os.environ['userName'])

def setup_env_variables():
    """Mocked AWS Credentials for moto."""

    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ['databaseName'] = 'Users'
    os.environ['userName'] = 'johndoe'