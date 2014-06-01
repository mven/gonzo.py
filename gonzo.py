# GONZO: A PYTHON SCRIPT TO RECORD PHP ERRORS INTO MONGO
# Michael Vendivel - vendivel@gmail.com

import subprocess
import datetime
from pymongo import MongoClient

# where's the log file
filename = '/path/to/php/logs.log'

# set up mongo client
client = MongoClient('mongo.server.address', 27017)

# which DB
db = client.logs

# which Collection
php_logs = db.php_logs

# open a subprocess to tail (and follow) the log file
f = subprocess.Popen(['tail','-f',filename],\
	stdout=subprocess.PIPE,stderr=subprocess.PIPE)

# continue to read the file and record lines into mongo
while True:

	# read line by line
	line = f.stdout.readline()
	
	# compose the document to be inserted
	post = {"line": line,
			"created": datetime.datetime.utcnow()
			}

	# insert the document into the Collection
	post_id = php_logs.insert(post)

	# output the line for visual debugging (optional)
	print line