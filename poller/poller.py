import urllib2, code
import xml.etree.cElementTree as ET
import MySQLdb
import datetime, threading, time

# Reads eGauge XML data from an input URL and outputs pertinent data
def readEgauge(uxmlurl):
    # Open the URL and parse the xml data
    try:
        response = urllib2.urlopen(uxmlurl,timeout = 1)
    except urllib2.URLError, e:
        return (999999999,999999999)
    html = response.read()
    root = ET.fromstring(html)

    # extract the relevant variables and return them
    timeNumber = int(root[0].text)
    totalPower = float(root[1].text) + float(root[2].text)
    return (timeNumber, totalPower)
    
def timerLoop(db,cursor,commandString,url,iLimit):
    global next_call
    data = readEgauge(url)
    insertString = commandString % data
    print(datetime.datetime.now())
    try:
        cursor.execute(insertString)
        db.commit()
    except:
        db.rollback()
    next_call = next_call + 1
    iLimit = iLimit + 1
    if (iLimit < 10):
        threading.Timer(next_call - time.time(), timerLoop,(db,cursor,commandString,url,iLimit)).start()
    
#--------------------------------------
# Begin Script
#--------------------------------------

# Connect to the MySQL Database
db = MySQLdb.connect(host="localhost", port=3306,
    user="crawler", passwd="disaggreg8tor",
    db="energydata");
cursor = db.cursor()
commandString = "INSERT INTO smarthome (timestamp, power) VALUES (%s, %s)"

# URL for the eGauge XML file
url = 'http://egauge1146.egaug.es/cgi-bin/egauge?noteam'

#code.interact(local=locals())

next_call = time.time()
i = 0
timerLoop(db,cursor,commandString,url,i) 
db.close
