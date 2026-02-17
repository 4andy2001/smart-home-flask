import socket               # Import socket modul
import json
from flask import render_template
from app import app

host = "smart-home-mqtt-subscriber"  # Use the service name defined in docker-compose.yaml
port = 12345                # Reserve a port for the sensor server


@app.route("/read_sensors", methods=["POST"])
def read_sensors():
    print("entered read_sensors\n")    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       print(f"calling connect(), host = {host}")
       s.connect((host, port))
       print("returned from connect()")
       json_byte_array = s.recv(1024)     

    print(f'json_byte_array len = {len(json_byte_array)} ')
    json_string = json_byte_array.decode()
    print(f'json_string = " {json_string}')

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
