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
  A Lambda function used by the APIs from 100daysofcloud.com to get all users OR as per the limit supplied in query params

  Parameters: event["queryStringParameters"]["limit"] (int): 100daysofcloud github username

  Returns: Returns all the users from 100daysofcloud (OR returns based on limits supplied in query params)

  """

  # Set up table object
  table = dynamodb.Table(os.environ['databaseName'])

  # Check if limit field is in the body of the request
  # If empty, scan the whole table
  set_limit=False
  if "queryStringParameters" in event:
    if "limit" in event["queryStringParameters"]:
      #capture requested limit count 
      set_limit=True
      limit = int(event["queryStringParameters"]['limit'])

  # Scan the table with the limit
  if set_limit:
    table_response = table.scan(Limit=limit)
  # Scan the table without the limit
  else:
    table_response = table.scan()

  #print(table_response)

  if "Items" not in table_response:
    print("ERROR: Items not found in table!")
    status_code = 404
    responseBody = "ERROR: users not found!"

  else:
    # Put dynamodb response into variable
    status_code = 200
    responseBody = json.dumps(table_response["Items"], use_decimal=True)

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
        
    