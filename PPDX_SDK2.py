import requests
import urllib.parse

#function to set state of enclave
def setState(title,description,step,maxSteps,address):
    state= {"title":title,"description":description,"step":step,"maxSteps":maxSteps}
    call_set_state_endpoint(state, address)

#function to set state of enclave
# def setState(title,description,step,maxSteps):
#     state= {"title":title,"description":description,"step":step,"maxSteps":maxSteps}

#     with open('data/state.txt', 'w') as f:
#         json.dump(state, f)


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