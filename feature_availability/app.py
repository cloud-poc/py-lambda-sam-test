import json
import boto3
import os

def lambda_handler(event, context):
    """Sample pure Lambda function
        Parameters
        ----------
        event: dict, required
            API Gateway Lambda Proxy Input Format
            Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
        context: object, required
            Lambda Context runtime methods and attributes
            Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
        Returns
        ------
        API Gateway Lambda Proxy Output Format: dict
            Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    # extract entity from request path
    entity = event["pathParameters"]["entity"]

    # obtain dynamo table name from environment variables
    tableName = os.environ["FA_TABLE_NAME"]

    #construct dynamodb request
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(tableName)

    requestKey = {
        "entity": entity
    }
    try:
        response = table.get_item(Key = requestKey)
        return {
            "statusCode": 200,
            "body": json.dumps(response["Item"]),
            "headers": {"Content-Type":"application/json"}
        }
    except KeyError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "internal server error"
            }),
            "headers": {"Content-Type": "application/json"}
        }
