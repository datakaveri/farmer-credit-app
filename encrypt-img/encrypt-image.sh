docker build -t unencrypted - <<EOF
FROM ghcr.io/datakaveri/farmer-credit-app:p3dx-v1.1
EOF

KEY_FILE="farmer-credit-app"
# head -c 32 /dev/urandom | openssl enc > "$KEY_FILE"
KEY_B64="$(base64 < $KEY_FILE)"

KEY_PATH="/default/image_key/farmer-credit-app"
KEY_ID="kbs://${KEY_PATH}"

git clone https://github.com/confidential-containers/guest-components.git
cd guest-components
docker build -t coco-keyprovider -f ./attestation-agent/docker/Dockerfile.keyprovider .

mkdir -p oci/{input,output}
skopeo copy docker-daemon:unencrypted:latest dir:./oci/input
docker run -v "${PWD}/oci:/oci" coco-keyprovider /encrypt.sh -k "$KEY_B64" -i "$KEY_ID" -s dir:/oci/input -d dir:/oci/output

skopeo inspect dir:./oci/output | jq '.LayersData[0].Annotations["org.opencontainers.image.enc.keys.provider.attestation-agent"] | @base64d | fromjson'


ENCRYPTED_IMAGE=ghcr.io/datakaveri/farmer-credit-app:p3dx-v1.1-encrypted
skopeo copy dir:./oci/output "docker://${ENCRYPTED_IMAGE}"


