#!/bin/bash

# File paths for storing instance ID and secret key
INSTANCE_ID_FILE="/home/ec2-user/instance_id"
SECRET_KEY_FILE="/home/ec2-user/secret_key"

# URLs and database/table names for Timestream and Lambda
DB_URL="https://ingest-cell1.timestream.us-east-2.amazonaws.com"
DATABASE_NAME="TimeSeriesDB"
TABLE_NAME="TimeSeriesTable"
LAMBDA_URL="https://7udiugpzjb.execute-api.us-east-2.amazonaws.com/default/idChecker"

# Generate a 6-character hexadecimal ID if not already created
if [ ! -f "$INSTANCE_ID_FILE" ]; then
        INSTANCE_ID=$(openssl rand -hex 3)
        echo $INSTANCE_ID > $INSTANCE_ID_FILE
else
        INSTANCE_ID=$(cat INSTANCE_ID_FILE)
fi

# Fetch or create a secret key
if [ ! -f "$SECRET_KEY_FILE" ]; then
        SECRET_KEY=$(openssl rand -hex 3)
        echo $SECRET_KEY > $SECTRE_KEY_FILE
else
        SECRET_KEY=$(cat SECRET_KEY_FILE)
fi

# Register the instance with the Lambda function
curl -X POST $LAMBDA_URL -d "{\"id\":\"$INSTANCE_ID\", \"ip\":\"$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)\", \"flag\":\"new\"}"

# Continuously write timestamp and secret key hash to Timestream every 10 minutes
while true; do
        TIMESTAMP=$(date +%s)
        SECRET_KEY_HASH=$(echo -n $SECRET_KEY | sha256sum | awk '{print $1}')curl -X POST $DB_URL -d "{\"timestamp\": \"$TIMESTAMP\", \"secret_key_hash\": \"$SECRET_KEY_HASH\"}"
        sleep 600
done

python3 /home/ec2-user/app.py &