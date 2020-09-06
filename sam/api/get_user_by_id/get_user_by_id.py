import boto3
from botocore.exceptions import ClientError
import logging
import simplejson as json
import os 

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger()

# Set up dynamodb object
dynamodb = boto3.resource('dynamodb', region_name = os.environ['AWS_DEFAULT_REGION'])

def lambda_handler(event, context):
  """ 
  A Lambda function used by the APIs from 100daysofcloud.com to get user details by Id

  Parameters: event["queryStringParameters"]["username"] (string): 100daysofcloud github username

  Returns: Returns user details from 100daysofcloud account if user is valid.

  """

  # Set up table object
  table = dynamodb.Table(os.environ['databaseName'])

  # Check if username field is in the body of the request
  # If empty, return error message
  ### FIXME this returns a KeyError and results in an "internal server error"
  if "username" not in event["queryStringParameters"]:
    logger.info('Username in request found to be empty or non-existent')
    status_code = 404
    responseBody = "username field in the body of the request is missing"

  else:
    # Get github_username out of body of the request
    github_username = event["queryStringParameters"]['username']

    # Query the table with the primary key github_username
    table_response = table.get_item(
      Key={
        'github_username': github_username
      }
    )

    # print(table_response)

    if "Item" not in table_response:
      print("ERROR: Item not found in table!")
      status_code = 404
      responseBody = "ERROR: user not found!"

    else:
      # Put dynamodb response into variable
      status_code = 200
      responseBody = json.dumps(table_response["Item"], use_decimal=True)

    # Log response from DynamoDB
    logger.info(responseBody)

  return {
    "isBase64Encoded": False,
    "statusCode": status_code,
    "body": responseBody,
    "headers": {
        "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS" 
    }
  }
        
    