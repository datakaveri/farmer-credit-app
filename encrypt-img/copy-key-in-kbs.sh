# Copy the key to the KBS
# In further features,the application developer should set-resources in kbs using and API to the resource KBS to handle keys from the application developer

KEY_PATH="default/image_key/farmer-credit-app"
KEY_FILE="farmer-credit-app"

kubectl exec trustee-kbs -- mkdir -p "/opt/confidential-containers/kbs/repository/$(dirname "$KEY_PATH")"
cat "$KEY_FILE" | kubectl exec -i trustee-kbs -- tee "/opt/confidential-containers/kbs/repository/${KEY_PATH}" > /dev/null