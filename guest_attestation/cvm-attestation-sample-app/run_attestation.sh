#!/bin/bash

echo "Running attestation.."

sudo ./AttestationClient -n d2a84f4b8b650937ec8f73cd8be2c74add5a911ba64df27458ed8229da804a26 -o token >> attestation_output

JWT=$(cat attestation_output)

header=$(echo -n "$JWT" | cut -d "." -f 1 | base64 -d 2>/dev/null | jq .)
payload=$(echo -n "$JWT" | cut -d "." -f 2 | base64 -d 2>/dev/null | jq .)

# Concatenate header and payload JSON objects
json="$header\n$payload"

# Save JSON object to a file
echo -e "$json" > jwt_content.json

echo "JWT content saved to jwt_content.json"
