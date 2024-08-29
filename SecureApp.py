import subprocess
import os
import PPDX_SDK
import sys
import json
import shutil

# Simulate sourcing external scripts -  
# You'd integrate the necessary functions from setState.sh and profilingStep.sh here 


def load_config(filename):
    """Loads configuration data from a JSON file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{filename}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in configuration file '{filename}'.")

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


def remove_profiling_file():
    if os.path.exists("profiling.json"):
        os.remove("profiling.json")

def remove_files():
    file_path = os.path.join('.','docker-compose.yml')
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed file: {file_path}")
    else:
        print(f"File not found: {file_path}")

    folder_path = os.path.join('.', 'keys')
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Removed folder and contents: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")

    folder_path = os.path.join('/tmp', 'inputdata')
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Removed folder and contents: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")
    
    folder_path = os.path.join('/tmp', 'output')
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Removed folder and contents: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")

# Start the main process
if __name__ == "__main__":
    config_file = "config_file.json"
    config = load_config(config_file)  # Loads configuration into a dictionary
    address = config["enclaveManagerAddress"]
    
    #PPDX_SDK.profiling_steps('Application Start', 0)
    #remove_profiling_file()
    remove_files()

    if len(sys.argv) < 2:
        print("Error: Missing GitHub raw link argument.")
        print("Usage: sudo python3 deploy_enclave.py <github_raw_link>")
        sys.exit(1)  # Exit with an error code

    github_raw_link = sys.argv[1]
    json_context = sys.argv[2]
    if not github_raw_link.startswith("https://raw.githubusercontent.com/"):
        print("Error: Invalid GitHub raw link format.")
        sys.exit(1)

    # Step 1 - Pulling docker compose & extracting docker image link
    print("\nStep 1")
    box_out("Pulling Docker Compose from GitHub...")
    PPDX_SDK.setState("Step 1","Pulling Docker Compose from GitHub...",1,10,address)
    #PPDX_SDK.profiling_steps('Step 1', 1)
    PPDX_SDK.pull_compose_file(github_raw_link)
    print('Extracting docker link...')
    link = subprocess.check_output(["sudo", "docker", "compose", "config", "--images"]).decode().strip()
    print("Image information:", link)


    # Step 2 - Key generation
    print("\nStep 2") 
    box_out("Generating and saving key pair...")
    PPDX_SDK.setState("Step 2","Generating and saving key pair...",2,10,address)
    #PPDX_SDK.profiling_steps('Step 2', 2)
    PPDX_SDK.generate_and_save_key_pair()

    # Step 3 - Docker image pulling
    print("\nStep 3")
    box_out("Pulling docker image...")
    PPDX_SDK.setState("Step 3","Pulling docker image...",3,10,address)
    #PPDX_SDK.profiling_steps('Step 3', 3)
    PPDX_SDK.pull_docker_image(link)
    print("Pulled docker")

    # Step 4 - Measuring image and storing in vTPM
    print("\nStep 4")
    box_out("Measuring Docker image into vTPM...")
    PPDX_SDK.setState("Step 4","Measuring Docker image into vTPM...",4,10,address)
    #PPDX_SDK.profiling_steps('Step 4', 4)
    PPDX_SDK.measureDockervTPM(link)
    print("Measured and stored in vTPM")

    # Step 5 - Send VTPM & public key to MAA & get attestation token
    print("\nStep 5")
    box_out("Guest Attestation Executing...")
    PPDX_SDK.setState("Step 5","Guest Attestation Executing...",5,10,address)
    #PPDX_SDK.profiling_steps('Step 5', 5)
    PPDX_SDK.execute_guest_attestation()
    print("Guest Attestation complete. JWT received from MAA")

    # Step 6 - Send the JWT to APD
    print("\nStep 6")
    box_out("Sending JWT to APD for verification...")
    PPDX_SDK.setState("Step 6","Sending JWT to APD for verification...",6,10,address)
    #PPDX_SDK.profiling_steps('Step 6', 6)
    token=PPDX_SDK.getTokenFromAPD('jwt-response.txt', 'config_file.json')
    print("Access token received from APD")

    # Step 7 - Docker image pulling
    print("\nStep 7")
    box_out("Getting files from RS...")
    PPDX_SDK.setState("Step 7","Getting files from RS...",7,10,address)
    #PPDX_SDK.profiling_steps('Step 7', 7)
    PPDX_SDK.getFileFromResourceServer(token)

    # Step 8 - Docker image pulling
    print("\nStep 8")
    box_out("Decrypting & storing files...")
    PPDX_SDK.setState("Step 8","Decrypting & storing files...",8,10,address)
    #PPDX_SDK.profiling_steps('Step 8', 8)
    PPDX_SDK.decryptFile()
    #PPDX_SDK.profiling_inputImages()
    print("Files decrypted and stored in /tmp/inputdata")

    # Executing the application in the docker
    print("\nStep 9")
    box_out("Running the Application...")
    PPDX_SDK.setState("Step 9","Running Application...",9,10,address)
    #PPDX_SDK.profiling_steps('Step 9', 9)
    subprocess.run(["sudo", "docker", "compose", 'up'])

    print("\nStep 10")
    PPDX_SDK.setState("Step 10","Finished Application Execution",10,10,address)
    #PPDX_SDK.profiling_steps('Step 10', 10)
    #PPDX_SDK.profiling_totalTime()
    print('DONE')
    print('Output saved to /tmp/output')
