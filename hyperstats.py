#!/usr/bin/python

#Name: HyperStats
#Creators: Sandesh Hebbar <hebbarsandesh98@gmail.com>, Dheeraj Acharya <dheerajacharya78@gmail.com>
#Description: HyperV Resource Utilizaiton Statistics Reporter

import os
import json
import subprocess
import sys

from flask import Flask, g, jsonify, request    

app = Flask(__name__)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with werkzeug server')
    func()

#initial HTML webpage that will further prompt the user to get the required report
@app.route('/')
def init():
    str = "<html><body style=\"font-family: 'Courier New', Courier, monospace\"><br><div><img style=\"width: 15%; display: block; margin: 0 auto;\" alt=\"HyperStats Logo\" src=\"https://image.flaticon.com/icons/png/512/414/414183.png\" /><h1 style=\"text-align: center\">HyperStats</h1><p style=\"text-align: center\"><b>HyperV Resource Utilization Statistics Reporter</b></p><p style=\"text-align: center\"><b><span style=\"font-size: 20px\">&copy;</span> Sandesh Hebbar, Dheeraj Acharya</b></p><hr style=\"width: 70%\"></div><br><br><div><table style=\"width: 100%\"><thead></thead><tbody><tr><td style=\"width: 25%; text-align: center\"><div><h4>vCPU Usage</h4><button onclick=\"location.href='/cpustats'\">Get Report</button></div></td><td style=\"width: 25%; text-align: center\"><div><h4>Memory Parameters</h4><button onclick=\"location.href='/memstats'\">Get Report</button></div></td><td style=\"width: 25%; text-align: center\"><div><h4>Disk Utilization Information</h4><button onclick=\"location.href='/diskstats'\">GetReport</button></div></td><td style=\"width: 25%; text-align: center\"><div><h4>Network Statistics</h4><button onclick=\"location.href='/netstats'\">Get Report</button></div></td></tr></tbody></table></div></body></html>"
    return str

#an endpoint to shutdown the server (in case the terminal fails or in cases of exceptions)
@app.route('/system/shutdown')
def shutdwn():
    shutdown_server()

    str = "<html><body style=\"font-family: 'Courier New', Courier, monospace\"><br><div><img style=\"width: 15%; display: block; margin: 0 auto;\" alt=\"HyperStats Logo\" src=\"https://image.flaticon.com/icons/png/512/414/414183.png\" /><h2 style=\"text-align: center\">The server has been shut down successfully</h2></div></body></html>"
    return str

#returns network statistics in JSON format
@app.route('/netstats')
def network():

    try:
        p = subprocess.Popen(["powershell.exe",
       os.path.dirname(app.instance_path) + '\\PowerShell_Scripts\\networkStats.ps1'],
       stdout=sys.stdout)
    except Exception as e:
        raise e
    else:
        p.communicate()
        with open(os.path.dirname(app.instance_path) + '\\OutFiles\\netstats.json', 'r') as file_content:
            content = json.load(file_content)

        return jsonify(content)

#returns vCPU usage in JSON format
@app.route('/cpustats')
def cpu():

    try:
        p = subprocess.Popen(["powershell.exe",
       os.path.dirname(app.instance_path) + '\\PowerShell_Scripts\\cpuStats.ps1'],
       stdout=sys.stdout)
    except Exception as e:
        raise e
    else:
        p.communicate()
        with open(os.path.dirname(app.instance_path) + '\\OutFiles\\cpustats.json', 'r') as file_content:
            content = json.load(file_content)
            
        return jsonify(content)

#returns memory parameters in JSON format
@app.route('/memstats')
def memory():

    try:
        p = subprocess.Popen(["powershell.exe",
       os.path.dirname(app.instance_path) + '\\PowerShell_Scripts\\memoryStats.ps1'],
       stdout=sys.stdout)  
    except Exception as e:
        raise e
    else:
        p.communicate()
        with open(os.path.dirname(app.instance_path) + '\\OutFiles\\memstats.json', 'r') as file_content:
            content = json.load(file_content)
            
        return jsonify(content)

#returns disk utilization statistics in JSON format
@app.route('/diskstats')
def disk():

    try:
        p = subprocess.Popen(["powershell.exe",
       os.path.dirname(app.instance_path) + '\\PowerShell_Scripts\\diskUtilStats.ps1'],
       stdout=sys.stdout)  
    except Exception as e:
        raise e
    else:
        p.communicate()
        with open(os.path.dirname(app.instance_path) + '\\OutFiles\\diskstats.json', 'r') as file_content:
            content = json.load(file_content)
            
        return jsonify(content)

#specify the port in JSON format
if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0', port=9898)