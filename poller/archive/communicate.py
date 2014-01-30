import urllib2, code

url = 'http://egauge1146.egaug.es/cgi-bin/egauge?noteam'
response = urllib2.urlopen(url)
html = response.read()
print(html)

code.interact(local=locals())
