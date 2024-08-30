import subprocess
import os

def run_command_and_save_output(command, output_file):
    # Run the command using subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check if the command was successful
    if process.returncode == 0:
        # Save the output to the specified file
        with open(output_file, "wb") as file:
            file.write(stdout)
        print("Token generated successfully. Output saved to ../keys/jwt-response.txt")
    else:
        # Print error message if the command failed
        print("Error executing command:")
        print(stderr.decode())

def main():
    # Specify the command to run
    command = "sudo ./AttestationClient -o token"

    # Specify the output file path
    output_file = "../../keys/jwt-response.txt"

    # Run the command and save the output
    run_command_and_save_output(command, output_file)

if __name__ == "__main__":
    main()
