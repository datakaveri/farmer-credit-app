import json, requests

# necessary file reads
config_file_name = "config/config.json"

with open(config_file_name, 'r') as fp:
    config = json.load(fp)

url = 'http://127.0.0.1:11111/process_app'

response = requests.post(url, data=json.dumps(config))

print("response status:", response.status_code)
with open('farm_credit_output_compare.json','w') as f:
    json.dump(json.loads(response.text), f) 
