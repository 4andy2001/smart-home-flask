#
# Create a virtual environment (if it doesn't already exist)
# $ python -m venv env

#
# Activate the virtual environment
# $ source env/bin/activate 

# Install Flask (if it isn't already installed in the virtual environment
# $ pip install flask

# Set the environment variables for the server
# $ export FLASK_ENV=development
# $ export FLASK_APP=application.py

# Run the server:
# $ flask run
#       OR
# $ python <application.py>

# To access with a web client:
# Browse to http://127.0.0.1:5000 if browser on same machine as the Flask server or
# browse to http://<server_address>:5000

# Link to Flask API
# https://flask.palletsprojects.com/en/2.0.x/api/#

import socket               # Import socket module

import json
from flask import Flask, render_template

app = Flask(__name__)

host = "enodigm.com"
port = 12345                # Reserve a port for the sensor server


@app.route("/read_sensors", methods=["POST"])
def read_sensors():
    print("entered read_sensors\n")    

    s = socket.socket()         # Create a socket object
    # host = socket.gethostname() # Get local machine name
    print(f"calling connect(), host = {host})

    s.connect((host, port))
    print("returned from connect()")
    json_byte_array = s.recv(1024)

    json_string = json_byte_array.decode()
    print(f'json_string = " {json_string}')
    s.close     

    return (json_string)


@app.route("/")
def index():
   # print("entered index()")

   '''
   return render_template("index.html", temperature=mqtt_sub.sensor["temperature"], 
   humidity=mqtt_sub.sensor["humidity"], pressure=mqtt_sub.sensor["pressure"])
   '''
   return render_template("index.html", time_hallway="Waiting", temperature_hallway="Waiting",
                          humidity_hallway="Waiting", pressure_hallway="Waiting",
                          time_outside="Waiting", temperature_outside="Waiting",
                          humidity_outside="Waiting", pressure_outside="Waiting")


def main():

   # print(f"*** Entered main, application name = {__name__}")
   app.run(host="0.0.0.0")

   
if __name__ == "__main__":
   main()   
else:
   pass
   # print(f"*** application name = {__name__}")
