#Need to install requests package for python
#easy_install requests
import json
import requests
import pandas as pd
from flatten_json import flatten


# Set the request parameters
url = 'https://{servicenow instance url}/api/now/table/incident?sysparm_limit=5'

# Eg. User name="admin", Password="admin" for this code sample.
user = ''
pwd = ''

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.get(url, auth=(user, pwd), headers=headers )

# Check for HTTP codes other than 200
if response.status_code != 200: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

# Put our response into a var
data = response.json()

# Write the results object into a json file
with open ('data.json', 'w') as f:
    json.dump(data['result'], f)

# Read the new json file
with open ('data.json', 'r') as read:
    json_list = json.load(read)

# Define the fields we need in our csv export
fields = ['number', 'short_description', 'priority']

# Create key to value relationships for our specified columns
json_list = [{k:d[k] for k in fields} for d in json_list]

# Flatten json dataframe
json_list_flattended = (flatten(d, '.') for d in json_list)
df = pd.DataFrame(json_list_flattended)

# Export pandas dataframe to csv. index=False removes row count from the export
export = df.to_csv('test.csv', index=False)