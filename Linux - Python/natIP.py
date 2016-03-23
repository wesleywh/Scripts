from json import load
from urllib2 import urlopen

publicIP = load(urlopen('https://api.ipify.org/?format=json'))['ip']
print "PUBLIC IP:"+publicIP
