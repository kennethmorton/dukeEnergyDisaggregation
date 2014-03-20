import urllib2, code
import xml.etree.cElementTree as ET
import MySQLdb
import datetime, threading, time

# Reads eGauge XML data from an input URL and outputs pertinent data
def readEgauge(uxmlurl,indices,includeTimeStamp):
    # Open the URL and parse the xml data
    try:
        response = urllib2.urlopen(uxmlurl,timeout = 15)
    # except urllib2.URLError, e:
    except:
        nValues = len(indices)
        return [99999999] * nValues
    html = response.read()
    root = ET.fromstring(html)

    # extract the relevant variables and return them
    outputList = []
    
#    if includeTimeStamp:
#        outputList.append(int(root[0].text)
#    for i in indices:
    for i in indices:
#        outputList.append(float(root[i][2].text)
        outputList.append(root[i].attrib['title'])
    return outputList

def timerLoop(db,cursor,commandString,url,indices):
    global next_call

    data = []
    # Output the timestamp with the first reading
    includeTimeStamp = True
    data = data + readEgauge(url[0],indices[0],includeTimeStamp)
    # Loop through the remaining measurements
    includeTimeStamp = False    
    for i in range(1,6):
        data = data + readEgauge(url[i],indices[i],includeTimeStamp)
    for d in data:
        print(d)
    #insertString = commandString % data
    #print(datetime.datetime.now())
    #try:
    #    cursor.execute(insertString)
    #    db.commit()
    #except:
    #    db.rollback()
#    next_call = next_call + 1
#    threading.Timer(next_call - time.time(), timerLoop,(db,cursor,commandString,url,indices)).start()
    
#--------------------------------------
# Begin Script
#--------------------------------------

# Connect to the MySQL Database
db = MySQLdb.connect(host="localhost", port=3306,
    user="crawler", passwd="disaggreg8tor",
    db="energydata");
cursor = db.cursor()

url_egauge = [
    'http://152.3.3.246/cgi-bin/egauge?noteam',
    'http://152.3.3.236/cgi-bin/egauge?noteam',
    'http://152.3.3.210/cgi-bin/egauge?noteam',
    'http://152.3.3.214/cgi-bin/egauge?noteam',
    'http://152.3.3.235/cgi-bin/egauge?noteam',
    'http://152.3.3.213/cgi-bin/egauge?noteam',
]

indices = [ [8,9,6,7],
            [11,12,10,7,8,9],
            [9,10,11,13,14,12],
            [8,9,10,11,12],
            [11,12,15,16,14,13],
            [7,8,9,10,11,12]]
labels = (
    "b7139_01_r_01_phase1",
    "b7139_01_r_02_phase2",
    "b7139_01_r_03_solar1",
    "b7139_01_r_04_solar2",
    "b7139_02_r_01_panelal2",
    "b7139_02_r_02_panelal1",
    "b7139_02_r_03_panelbl2",
    "b7139_02_r_04_panelbl1",
    "b7139_02_r_05_panelul2",
    "b7139_02_r_06_panelul1",
    "b7139_03_r_01_refrig",
    "b7139_03_r_02_micro",
    "b7139_03_r_03_dish",
    "b7139_03_r_04_oven",
    "b7139_03_r_06_cooktop",
    "b7139_03_r_08_kitchen1",
    "b7139_04_r_01_kitchen2",
    "b7139_04_r_02_kitchen3",
    "b7139_04_r_03_washer",
    "b7139_04_r_04_dryer",
    "b7139_04_r_06_hotbox",
    "b7139_05_r_01_ahu1",
    "b7139_05_r_03_ahu2",
    "b7139_05_r_05_cu1",
    "b7139_05_r_07_cu2",
    "b7139_05_r_09_airrecunit",
    "b7139_05_r_10_rwp",
    "b7139_06_r_01_irrigation",
    "b7139_06_r_02_erv",
    "b7139_06_r_03_h10p",
    "b7139_06_r_04_ef1",
    "b7139_06_r_05_ef2",
    "b7139_06_r_06_ef3"
)

commandString = "INSERT INTO smarthome (timestamp, power) VALUES (%s, %s)"

# URL for the eGauge XML file
#url = 'http://152.3.3.246/cgi-bin/egauge?noteam'

#code.interact(local=locals())

print("Starting poller.py...\n")
next_call = time.time()
try:
    timerLoop(db,cursor,commandString,url_egauge,indices)
except:
    db.close
    raise
else:
    db.close
#    raise
