#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import Crypto
from Crypto.PublicKey import RSA
import json
import requests
import _pickle as pickle
import urllib
import urllib.parse

def pull_compose_file(url, filename='docker-compose.yml'):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        with open(filename, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded content from '{url}' and saved to '{filename}'")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading content: {e}")

# Generate Public-Private Key Pair
def generate_and_save_key_pair():
    public_key_file='public_key.pem'
    private_key_file='private_key.pem'
    # Create 'keys' folder if it doesn't exist
    if not os.path.exists('keys'):
        os.makedirs('keys')

    # Generate a new RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Get the public key
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode().split('\n')[1:-1]  # Remove BEGIN and END headers

    # Get the private key
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()   # Remove BEGIN and END headers

    # Write the public key to a file
    with open(os.path.join('keys', public_key_file), "w") as public_key_out:
        public_key_out.write(''.join(public_key))

    # Write the private key to a file
    with open(os.path.join('keys', private_key_file), "w") as private_key_out:
        private_key_out.write(''.join(private_key_bytes))

    print("Public and private keys generated and saved successfully in the 'keys' folder!")

    # Remove the end tags from both files
    with open(os.path.join('keys', public_key_file), 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if '----' not in line:
            new_lines.append(line)
        else:
            new_lines.append(line.split('----')[0])

    with open(os.path.join('keys', public_key_file), 'w') as file:
        file.writelines(new_lines)


def measureDockervTPM(sha_digest):
    # Extend docker image hash to PCR 15
    try:
        print("Extending the measurement to PCR 15 using TPM2 tools...")
        # Extend the measurement to PCR 15 using TPM2 tools
        subprocess.run(['sudo', 'tpm2_pcrextend', f'15:sha256={sha_digest}'])
        print("Measurement extended successfully to PCR 15.")
    except Exception as e:
        print("Error:", e)

    try:
        pcr_values = {}
        # Run tpm2_pcrread command to get the PCR values
        command = ['sudo', 'tpm2_pcrread', 'sha256:0,1,2,3,4,5,6,7,8,15']
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check if the command was successful
        if result.returncode == 0:

            output_lines = result.stdout.strip().split('\n')
            for line in output_lines[1:]:  # Skip the first line (sha256:)
                parts = line.split(':')
                if len(parts) == 2:
                    pcr_number = parts[0].strip()
                    pcr_value = parts[1].strip()
                    pcr_values[pcr_number] = pcr_value
                else:
                    print("Unexpected output format:", line)
            json_string = json.dumps(pcr_values)

            with open(os.path.join('keys', 'pcr_values.json'), 'w') as file:
                file.write(json_string)
            print("PCR values written to file successfully!")
        else:
            print(f"Error reading PCR values: {result.stderr}")
    except Exception as e:
        print("Error:", e)  

def execute_guest_attestation():
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)

    commands_folder = os.path.join(script_dir, "guest_attestation/cvm-attestation-sample-app")

    # Change directory to the specified folder
    os.chdir(commands_folder)

    # Execute the command to generate token
    subprocess.run(["python3", "generate-token.py"])

    # Change directory back to the original directory
    os.chdir(script_dir)


#APD verifies quote and releases token
def getAttestationToken(config):

    auth_server_url=config["auth_server_url"]
    headers={'clientId': config["clientId"], 'clientSecret': config["clientSecret"], 'Content-Type': config["Content-Type"]}

    with open('keys/jwt-response.txt', 'r') as file:
        token = file.read().strip()

    context={
                "jwtMAA": token
            }

    data={
            "itemId": config["itemId"],
            "itemType": config["itemType"],
            "role": config["role"],
            "context": context
         }
    dataJson=json.dumps(data)
    r= requests.post(auth_server_url,headers=headers,data=dataJson)

    if(r.status_code==200):
        print("Token verified and Token recieved.")
        jsonResponse=r.json()
        token=jsonResponse.get('results').get('accessToken')
        print(token)

        # create tokens.json in the same directory & append to it as attestationToken
        with open('tokens.json', 'w') as file:
            json.dump({"attestationToken": token}, file)
        print("Attestation token written to tokens.json file.")
    
    else:
        print("Attestation Token fetching failed.", r.text)
        sys.exit() 

def getYieldDataToken(config):

    auth_server_url=config["auth_server_url"]
    headers={'clientId': config["clientId"], 'clientSecret': config["clientSecret"], 'Content-Type': config["Content-Type"]}

    data={
        "itemId": config["yieldData_itemID"],
        "itemType": config["itemType"],
        "role": config["role"]
    }
    
    dataJson=json.dumps(data)
    r= requests.post(auth_server_url,headers=headers,data=dataJson)

    if(r.status_code==200):
        print("Token verified and Token recieved.")
        jsonResponse=r.json()
        token=jsonResponse.get('results').get('accessToken')
        print(token)

        # append yield data access token to tokens.json file
        with open('tokens.json', 'r') as file:
            tokens = json.load(file)
            tokens["yieldDataToken"] = token
        with open('tokens.json', 'w') as file:
            json.dump(tokens, file)
        print("Yield data access Token written to tokens.json file.")
    
    else:
        print("Yield data access Token fetching failed.", r.text)
        sys.exit() 

def getAPMCDataToken(config):

    auth_server_url=config["auth_server_url"]
    headers={'clientId': config["clientId"], 'clientSecret': config["clientSecret"], 'Content-Type': config["Content-Type"]}

    data={
        "itemId": config["APMCData_itemID"],
        "itemType": config["itemType"],
        "role": config["role"]
    }
    
    dataJson=json.dumps(data)
    r= requests.post(auth_server_url,headers=headers,data=dataJson)

    if(r.status_code==200):
        print("Token verified and Token recieved.")
        jsonResponse=r.json()
        token=jsonResponse.get('results').get('accessToken')
        print(token)

        # append APMC data access token to tokens.json file
        with open('tokens.json', 'r') as file:
            tokens = json.load(file)
            tokens["APMCDataToken"] = token
        with open('tokens.json', 'w') as file:
            json.dump(tokens, file)
        print("APMC data access Token written to tokens.json file.")
    
    else:
        print("APMC data access Token fetching failed.", r.text)
        sys.exit() 


def getSOFDataToken(config):

    auth_server_url=config["auth_server_url"]
    headers={'clientId': config["clientId"], 'clientSecret': config["clientSecret"], 'Content-Type': config["Content-Type"]}

    data={
        "itemId": config["SOFData_itemID"],
        "itemType": config["itemType"],
        "role": config["role"]
    }
    
    dataJson=json.dumps(data)
    r= requests.post(auth_server_url,headers=headers,data=dataJson)

    if(r.status_code==200):
        print("Token verified and Token recieved.")
        jsonResponse=r.json()
        token=jsonResponse.get('results').get('accessToken')
        print(token)

        # append SOF data access token to tokens.json file
        with open('tokens.json', 'r') as file:
            tokens = json.load(file)
            tokens["SOFDataToken"] = token
        with open('tokens.json', 'w') as file:
            json.dump(tokens, file)
        print("SOF data access Token written to tokens.json file.")
    
    else:
        print("SOF data access Token fetching failed.", r.text)
        sys.exit() 


def getFarmerDataToken(config, ppb_number):

    auth_server_url=config["auth_server_url"]
    headers={'clientId': config["clientId"], 'clientSecret': config["clientSecret"], 'Content-Type': config["Content-Type"]}

    context = {
        "ppbNumber": ppb_number
    }
    data={
        "itemId": config["FarmerData_itemID"],
        "itemType": config["itemType"],
        "role": config["role"],
        "context": context
    }
    
    dataJson=json.dumps(data)
    r= requests.post(auth_server_url,headers=headers,data=dataJson)

    if(r.status_code==200):
        print("Token verified and Token recieved.")
        jsonResponse=r.json()
        token=jsonResponse.get('results').get('accessToken')
        print(token)

        # append SOF data access token to tokens.json file
        with open('tokens.json', 'r') as file:
            tokens = json.load(file)
            tokens["FarmerDataToken"] = token
        
        with open('tokens.json', 'w') as file:
            json.dump(tokens, file)
        print("Farmer data access Token written to tokens.json file.")
    
    else:
        print("Farmer data access Token fetching failed.", r.text)
        sys.exit() 


#Send token to resource server for verification & get encrypted images  
def getFilesFromResourceServer(config):
    rs_url = config["adex_url"]

    # get all access tokens from tokens.json
    with open("tokens.json", "r") as file:
        tokens = json.load(file)
        token = tokens["attestationToken"]
        yieldDataToken = tokens["yieldDataToken"]
        APMCDataToken = tokens["APMCDataToken"]
        SOFDataToken = tokens["SOFDataToken"]
    
    # Get individual data & store in data/

    rs_headers={'Authorization': f'Bearer {token}'}
    rs=requests.get(rs_url,headers=rs_headers)
    if rs.status_code == 200:
        print("Token authenticated and Encrypted images received.")
        loadedDict = pickle.loads(rs.content)
        # Write the loadedDict to a file
        with open("loadedDict.pkl", "wb") as file:
            pickle.dump(loadedDict, file)
        print("loadedDict written to loadedDict.pkl file.")
    else:
        print("Token authentication failed.",rs.text)
        sys.exit()


def getFarmerData(config, ppb_number):
    # Define the URL and parameters
    url = config["farmer_data_url"]
    params = {
        "id": "c5422a0f-e60f-48e4-9d1e-1fa4b1714900",
        "q": f"Ppbno=={ppb_number}",
        "time": "2023-01-25T12:01:05Z",
        "endtime": "2023-02-01T12:01:05Z",
        "timerel": "during"
    }

    # read farmer data token from tokens.json
    with open('tokens.json', 'r') as file:
        tokens = json.load(file)
        token = tokens["FarmerDataToken"]

    # Define the headers
    headers = {
        "token": token
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            print("Farmer data fetched successfully.")
            # Ensure the 'data' directory exists
            os.makedirs("data", exist_ok=True)
            # Write the response content to a file
            with open("data/farmer_data.json", "wb") as file:
                file.write(response.content)
            print("Farmer data written to farmer_data.json file.")
        else:
            # Handle non-200 status codes
            print(f"Failed to fetch farmer data. Status code: {response.status_code}")
            print(f"Response content: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")


#function to set state of enclave
def setState(title,description,step,maxSteps,address):
    state= {"title":title,"description":description,"step":step,"maxSteps":maxSteps}
    call_set_state_endpoint(state, address)

#function to call set state endpoint
def call_set_state_endpoint(state, address):
    #define enpoint url
    endpoint_url=urllib.parse.urljoin(address, '/enclave/setstate')

    #create Json payload
    payload = { "state": state }
    #create POST request
    r = requests.post(endpoint_url, json=payload)

    #print response
    print(r.text)
