import subprocess
import os
import sys
import shutil
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import requests

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
    ).decode().split('\n')[1:-1]   # Remove BEGIN and END headers

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
            new_lines.append(line.split('----')[0] + '\n')

    with open(os.path.join('keys', public_key_file), 'w') as file:
        file.writelines(new_lines)

    with open(os.path.join('keys', private_key_file), 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if '----' not in line:
            new_lines.append(line)
        else:
            new_lines.append(line.split('----')[0] + '\n')

    with open(os.path.join('keys', private_key_file), 'w') as file:
        file.writelines(new_lines)

def measureDockervTPM(link):
    try:
        docker_image = link
        
        print(f"Fetching SHA256 digest for Docker image '{docker_image}'...")
        # Query Docker Hub API to get image info
        response = requests.get(f"https://registry.hub.docker.com/v2/repositories/{docker_image}/tags/latest")
        if response.status_code == 200:
            data = response.json()
            sha256_digest = data['images'][0]['digest'].replace('sha256:', '')
            print(f"SHA256 digest for image '{docker_image}' is: {sha256_digest}")

            print("Extending the measurement to PCR 15 using TPM2 tools...")
            # Extend the measurement to PCR 15 using TPM2 tools
            subprocess.run(['sudo', 'tpm2_pcrextend', f'15:sha256={sha256_digest}'])
            print("Measurement extended successfully to PCR 15.")
        else:
            print(f"Error: Image '{docker_image}' not found.")
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
            
            # Write the PCR values to a text file
            with open(os.path.join('keys', 'pcr_values.txt'), 'w') as file:
                for pcr_number, pcr_value in pcr_values.items():
                    file.write(f"{pcr_number}: {pcr_value}\n")
                    
            print("PCR values written to file successfully!")
        else:
            print(f"Error reading PCR values: {result.stderr}")
    except Exception as e:
        print("Error:", e)

def execute_guest_attestation(docker_image_link):
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)

    # Generate RSA keys 
    generate_and_save_key_pair()

    # Measure Docker image and get PCR values
    measureDockervTPM(docker_image_link)

    # Specify the folder containing the commands
    commands_folder = os.path.join(script_dir, "cvm-attestation-sample-app")

    # Change directory to the specified folder
    os.chdir(commands_folder)

    # Execute the command to generate token
    subprocess.run(["python3", "generate-token.py"])

    # Change directory back to the original directory
    os.chdir(script_dir)

    # Delete the 'keys' folder after generating the JWT
    shutil.rmtree(os.path.join(script_dir, "keys"), ignore_errors=True)

# Call the function with the Docker image link as an argument
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 guest-attestation.py <docker_image_link>")
        sys.exit(1)

    docker_image_link = sys.argv[1]
    execute_guest_attestation(docker_image_link)
    print('\n')

if __name__ == "__main__":
    main()
