import urllib2, code
import xml.etree.cElementTree as ET
import MySQLdb
import datetime, threading, time
from datetime import datetime

# Reads eGauge XML data from an input URL and outputs pertinent data
def getOne():
    return 1
    
def getTwo():
    return 2
    
def getThree():
    return 3    

def timerLoop():
    global next_call
    print(datetime.datetime.now())

    next_call = next_call + 1
    threading.Timer(next_call - time.time(), timerLoop,()).start()
    
#--------------------------------------
# Begin Script
#--------------------------------------

print("Starting poller.py...\n")
next_call = time.time()
try:
    timerLoop()
except:
    db.close
    raise
else:
    db.close
    raise
