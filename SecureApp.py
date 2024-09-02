import subprocess
import os
import PPDX_SDK
import json
import shutil

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

# Start the main process
if __name__ == "__main__":
    config_file = "config_file.json"
    with open(config_file) as f:
        config = json.load(f)
    address = config["address"]
    
    remove_files()

    # read the json context file stored in the context folder
    json_context = "./UIcontext/context.json"
    with open(json_context) as f:
        context = json.load(f)

    sha_digest = context["sha_digest"]
    ppb_number = context["ppb_number"]

    # Step 4 - Key generation
    print("\nStep 4") 
    box_out("Generating and saving key pair...")
    PPDX_SDK.setState("Step 4","Generating and saving key pair...",4,10,address)
    PPDX_SDK.generate_and_save_key_pair()
    print("Key pair generated and saved")

    # Step 5 - storing image digest in vTPM
    print("\nStep 5")
    box_out("Measuring Docker image into vTPM...")
    PPDX_SDK.setState("Step 5","Measuring Docker image into vTPM...",5,10,address)
    PPDX_SDK.measureDockervTPM(sha_digest)
    print("Measured and stored in vTPM")

    # Step 6 - Send VTPM & public key to MAA & get attestation token
    print("\nStep 6")
    box_out("Guest Attestation Executing...")
    PPDX_SDK.setState("Step 6","Guest Attestation Executing...",6,10,address)
    PPDX_SDK.execute_guest_attestation()
    print("Guest Attestation complete. JWT received from MAA")

    # Step 6 - Send the JWT to APD
    print("\nStep 7")
    box_out("Sending JWT to APD for verification...")
    PPDX_SDK.setState("Step 7","Sending JWT to APD for verification...",7,10,address)
    PPDX_SDK.getAttestationToken(config)
    print("Attestation token received from APD")

    # Call APD for getting ADEX data access tokens
    PPDX_SDK.getYieldDataToken(config)
    PPDX_SDK.getAPMCDataToken(config)
    PPDX_SDK.getSOFDataToken(config)

    # Call APD for getting Rythabandhu data access token
    PPDX_SDK.getFarmerDataToken(config, ppb_number)

    # Step 8 - Getting files from RS
    print("\nStep 8")
    box_out("Getting files from RS...")
    PPDX_SDK.setState("Step 8","Getting files from RS...",8,10,address)

    # getting files from ADEX
    PPDX_SDK.getFilesFromResourceServer(config)

    # getting Rytabandhu farmer data
    PPDX_SDK.getFarmerData(config, ppb_number)

    # Executing the application  
    print("\nStep 9")
    box_out("Running the Application...")
    PPDX_SDK.setState("Step 9","Running Application...",9,10,address)
    subprocess.run(["python3", "app.py"])
    # check for synchronous execution

    print("\nStep 10")
    PPDX_SDK.setState("Step 10","Finished Application Execution",10,10,address)
    #PPDX_SDK.profiling_steps('Step 10', 10)
    #PPDX_SDK.profiling_totalTime()
    print('DONE')
    print('Output saved to /tmp/output')
