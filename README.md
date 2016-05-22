# simpleC2
I developed a proof-of-concept bot, c2 server and admin control panel.  This was created for educational purposes only... 

To Setup the Proof-of-Concept to test to see if your defenses catch the bot...

Idea: Create a proxy script to relay a bot's traffic back to the controller... Black Hat Python...

Setup the C2 Server
-------------------
1. Setup the Web Server to Host the index.php file and the MySQL Database
2. Copy index.php to a directory that allows it to be accessible
3. Import the importDB.sql file into the database on the web server
4. Modify the sample.db.php file to contain your database configuration
5. Copy sample.db.php to the same directory on the web server as index.php

Setup a bot that talks to the C2 Server
---------------------------------------
1. You can run the bot.py on windows or linux as long as Python 2.7 is installed
2. If on windows copy bot.py to c:\python27 (Assuming it is installed in the default directory)
3. Execute from the command prompt with administrator privileges "python.exe bot.py"

2. Verify that you are running python 2.7
3. If on linux you can execute "python bot.py"
4. The bot is silent unless you uncomment in the python code to see when commands are executed

Control your bot from the Control Panel
---------------------------------------
1. From windows or linux as long as you run python 2.7
2. Copy adminCP.py to where you are going to execute it
2. Configure the sample.config.ini with the necessary information to connect to the database
3. Copy the sample.config.ini to where the adminCP.py is located and rename it to config.ini
4. After launching adminCP.py it should locate and load the database settings from config.ini


This was built for educational purposes only.  It can be used to test the defenses of your current network and identify how you could detect a bot beaconning to a C2 server.
