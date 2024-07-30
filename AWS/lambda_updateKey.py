import json
import boto3
import hashlib
import requests

def lambda_handler(event, context):
    rds = boto3.client('rds-data')
    database = 'TimeSeriesDB'
    resourceArn = 'arn:aws:timestream:us-east-2:010928184835:database/TimeSeriesDB'
    secretArn = 'arn:aws:secretsmanager:us-east-2:010928184835:secret:RDSSecret-p9BRKu'

    query = "SELECT InstanceID, SecretKey FROM Instances"
    instances = rds.execute_statement(
        secretArn=secretArn,
        database=database,
        resourceArn=resourceArn,
        sql=query
    )['records']

    for instance in instances:
        instance_id = instance[0]['stringValue']
        stored_secret_key = instance[1]['stringValue']
        new_secret_key = hashlib.sha256(stored_secret_key.encode()).hexdigest()

        # Update secret key on EC2 instance
        ec2_ip = get_ec2_ip(instance_id)
        api_url = f"http://3.15.142.113/update_secret_key"
        payload = {
            "old_secret_key": stored_secret_key,
            "new_secret_key": new_secret_key
        }
        response = requests.post(f"http://3.15.142.113/update_secret_key", json=payload)

        if response.status_code == 200:
            # Update secret key in RDS
            update_query = f"UPDATE Instances SET SecretKey='{new_secret_key}' WHERE InstanceID='{instance_id}'"
            rds.execute_statement(
                secretArn=secretArn,
                database=database,
                resourceArn=resourceArn,
                sql=update_query
            )

    return {'status': 'success'}

def get_ec2_ip(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(InstanceIds=[instance_id])
    ip_address = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    return ip_address
    pass

