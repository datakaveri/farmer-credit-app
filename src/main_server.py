from flask import Flask, jsonify, request
import json
import  configparser
from main_app import MainApp

app = Flask(__name__)
server_config = configparser.ConfigParser()
server_config.read('config/server_config.cfg')


main_server_ip = server_config.get('MAIN_SERVER', 'ip')
main_server_port = server_config.get('MAIN_SERVER', 'port')


def send_response(status, response):
    output = {"status":status,
        "output":response
    }
    ### start: to use only while testing the server ###
    print('response saved successfully')
    ### end: to use only while testing the server ###

    return output


@app.route("/test_server", methods = ["GET"])
def test_server():
    if (request.method == "GET"):
        data = "Test Server"
        return jsonify({'data': data})

@app.route("/process_app", methods = ["POST"])
def process_dp():
    try:
        config = json.loads(request.get_data().decode())    
        main_app_obj = MainApp()
        status, output = main_app_obj.main_process(config=config)
        response = send_response(status=status, response=output)
    except Exception as e:
        print(e)
        response = {"status":"failed", "output":{}}
    return response

if __name__ == '__main__':
    app.run(host=main_server_ip, port=main_server_port, debug=False)