import boto3
import json
import base64

rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    try:
        print("Event:", json.dumps(event))
        body = json.loads(event['body'])

        if 'image' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing image field'})
            }

        image_bytes = base64.b64decode(body['image'])

        response = rekognition.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,
            MinConfidence=75
        )

        labels = [
            {"Name": label["Name"], "Confidence": round(label["Confidence"], 2)}
            for label in response['Labels']
        ]

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps({'labels': labels})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

