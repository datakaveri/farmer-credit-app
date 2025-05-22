#!/bin/bash

flask run & # RAM
python deploy_enclave.py 
python app.py 
/bin/bash