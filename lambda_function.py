import json
from main import app

def lambda_handler(event, context):
    # Extract the method and path from the event
    http_method = event.get('httpMethod', '')
    path = event.get('path', '/')
    
    # Get query parameters
    query_params = event.get('queryStringParameters', {})
    
    # Get headers
    headers = event.get('headers', {})
    
    # Mock the request for FastAPI
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    try:
        response = None
        
        if http_method == 'GET':
            response = client.get(path, params=query_params, headers=headers)
        elif http_method == 'POST':
            body = event.get('body')
            if body:
                try:
                    body = json.loads(body)
                except:
                    pass
            response = client.post(path, json=body, params=query_params, headers=headers)
        elif http_method == 'PUT':
            body = event.get('body')
            if body:
                try:
                    body = json.loads(body)
                except:
                    pass
            response = client.put(path, json=body, params=query_params, headers=headers)
        elif http_method == 'DELETE':
            response = client.delete(path, params=query_params, headers=headers)
        else:
            # Default to GET for unknown methods
            response = client.get(path, params=query_params, headers=headers)
            
        # Convert response to Lambda format
        return {
            'statusCode': response.status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': response.text
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }