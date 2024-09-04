import subprocess
import os
import PPDX_SDK
import json
import shutil
import app

# Simulate sourcing external scripts -  
# You'd integrate the necessary functions from setState.sh and profilingStep.sh here 

def box_out(message):
    """Prints a box around a message using text characters."""

    lines = message.splitlines()  # Split message into lines
    max_width = max(len(line) for line in lines)  # Find longest line

    # Top border
    print("+" + "-" * (max_width + 2) + "+")

    # Content with padding
    for line in lines:
        print("| " + line.ljust(max_width) + " |")

    # Bottom border
    print("+" + "-" * (max_width + 2) + "+")

def remove_files():
    folder_path = os.path.join('.', 'keys')
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Removed folder and contents: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")

    folder_path = os.path.join('.', 'output')
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Removed folder and contents: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")
    # create the output folder
    os.makedirs(folder_path)

# Start the main process
if __name__ == "__main__":
    
    remove_files()
    
    with open("output/output.json", "w") as f:  
        # make status code 300 & status as "Executing" to indicate that the process has started 
        json.dump({"status_code": "300"}, f)

    config_file = "config_file.json"
    with open(config_file) as f:
        config = json.load(f)
    address = config["address"]

    # read the json context file stored in the context folder
    json_context = "./UIcontext/context.json"
    with open(json_context) as f:
        context = json.load(f)

    sha_digest = context["sha_digest"]
    ppb_number = context["ppb_number"]

    # Step 4 - Key generation
    box_out("Generating and saving key pair...")
    PPDX_SDK.setState("TEE Attestation & Authorisation", "Step 2",2,5,address)
    PPDX_SDK.generate_and_save_key_pair()
    print("Key pair generated and saved")

    # Step 5 - storing image digest in vTPM
    box_out("Measuring Docker image into vTPM...")
    PPDX_SDK.measureDockervTPM(sha_digest)
    print("Measured and stored in vTPM")

    # Step 6 - Send VTPM & public key to MAA & get attestation token
    box_out("Guest Attestation Executing...")
    PPDX_SDK.execute_guest_attestation()
    print("Guest Attestation complete. JWT received from MAA")

    # Step 7 - Send the JWT to APD
    box_out("Sending JWT to APD for verification...")
    #attestationToken = PPDX_SDK.getAttestationToken(config)
    print("Attestation token received from APD")

    # Call APD for getting ADEX data access token
    print("Getting ADEX data access token")
    adexDataToken = PPDX_SDK.getADEXDataAccessTokens(config)

    # Call APD for getting Rythabandhu data access token
    print("Getting Rytabandhu consent token")
    farmerDataToken = PPDX_SDK.getFarmerDataToken(config, ppb_number)

    # Step 8 - Getting files from RS
    box_out("Getting files from RS...")
    PPDX_SDK.setState("Getting data into Secure enclave","Step 3",3,5,address)

    # getting files from ADEX
    PPDX_SDK.getSOFDataFromADEX(config, adexDataToken)
    PPDX_SDK.getYieldDataFromADEX(config, adexDataToken)
    PPDX_SDK.getAPMCDataFromADEX(config, adexDataToken)

    # getting Rytabandhu farmer data
    PPDX_SDK.getFarmerData(config, ppb_number, farmerDataToken)

    # Executing the application  
    box_out("Running the Application...")
    PPDX_SDK.setState("Computing farmer credit amount in TEE", "Step 4",4,5,address)
    kisaan_loan_amount, consumer_loan_amount = app.main()

    # check if status code is 300 and set it to 000
    with open("output/output.json") as f:
        output = json.load(f)
        if output["status_code"] == "300":
            response = {
                "output": {
                    "kisaan_loan_amount": kisaan_loan_amount,
                    "consumer_loan_amount": consumer_loan_amount
                },
                "status": "Success",
                "status_code": "000"  
            }
        else:
            print("Status code: ", output["status_code"])
            print("Status: ", output["status"])
            response = {
                "output": {
                    "kisaan_loan_amount": 0,
                    "consumer_loan_amount": 0
                },
                "status": output["status"],
                "status_code": output["status_code"]
            }
        with open("./output/output.json", "w") as f:
            json.dump(response, f)

    print("Output saved to output.json")

    # execution completed
    PPDX_SDK.setState("Secure Computation Complete","Step 5",5,5,address)
    print('DONE')
