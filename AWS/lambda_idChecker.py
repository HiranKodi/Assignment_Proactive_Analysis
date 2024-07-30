import json
import boto3

def lambda_handler(event, context):
    rds = boto3.client('rds-data')
    database = 'TimeSeriesDB'
    resourceArn = 'arn:aws:timestream:us-east-2:010928184835:database/TimeSeriesDB'
    secretArn = 'arn:aws:secretsmanager:us-east-2:010928184835:secret:RDSSecret-p9BRKu'

    instance_id = event['id']
    ip_address = event['ip']
    flag = event['flag']

    if flag == 'new':
        query = f"INSERT INTO Instances (InstanceID, IPAddress) VALUES ('{instance_id}', '{ip_address}')"
    elif flag == 'update':
        query = f"UPDATE Instances SET IPAddress='{ip_address}' WHERE InstanceID='{instance_id}'"
    else:
        return {'status': 'error', 'message': 'Invalid flag'}

    try:
        rds.execute_statement(
            secretArn=secretArn,
            database=database,
            resourceArn=resourceArn,
            sql=query
        )
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
