import os
from exporters import csv
from pcpi import session_loader
from dotenv import load_dotenv

load_dotenv()

session = session_loader.load_config_env()
cspm_session = session.create_cspm_session()

payload = {
    "query": "config from cloud.resource where cloud.type = 'aws' and cloud.accountgroup = 'PCS AWS Accounts' AND api.name = 'aws-ec2-describe-instances' AND json.rule = state contains running and metadataOptions.httpEndpoint equals enabled and metadataOptions.httpTokens does not contain required addcolumn $.tags[?(@.key=='owner'||@.key=='Owner'||@.key=='team'||@.key=='Team'||@.key=='ManagedBy')].value $.tags[*]",
    #"timeRange": {
    #    "relativeTimeType": "BACKWARD",
    #    "type": "relative",
    #    "value": {
    #        "amount": 24,
    #        "unit": "hour"
    #    }
    #},
    "limit": 2000,
    "withResourceJson": False
}

cols=['']

response: dict = cspm_session.config_search_request(payload)

if not response.get('data'):
    print("Error: Response contained no data")
    exit(-1)

if len(response['data']['items']) == 0:
    print("No results")

csv.process(response)