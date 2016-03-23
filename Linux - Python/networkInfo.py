import re
import subprocess
import socket
from json import load
from urllib2 import urlopen

hostname = socket.gethostname()
'''ip = socket.gethostbyname(socket.gethostname())'''


command = "ip -4 addr show eth0 | grep inet | awk '{ print $2 }'"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, )
ipOutput = process.communicate()[0]
ipOutput = ipOutput.strip(' \t\n\r')

netmaskCommand = "/sbin/ifconfig eth0 | awk '/Mask:/{ print $4;} '"
netProc = subprocess.Popen(netmaskCommand, shell=True, stdout=subprocess.PIPE, )
netmaskOutput = netProc.communicate()[0]
netmaskOutput = netmaskOutput.strip(' \t\n\r')
netmaskOutput = netmaskOutput.replace("Mask:","")

gatewayCommand = "/sbin/ip route | awk '/default/ { print $3 }'"
netProc = subprocess.Popen(gatewayCommand, shell=True, stdout=subprocess.PIPE, )
gatewayOutput = netProc.communicate()[0]
gatewayOutput = gatewayOutput.strip(' \t\n\r')

dnsCommand = 'nm-tool | grep DNS'
dnsProc = subprocess.Popen(dnsCommand, shell=True, stdout=subprocess.PIPE, )
dnsOutput = dnsProc.communicate()[0]
dnsOutput = dnsOutput.strip(' \t\n\r')
dnsOutput = dnsOutput.replace(" ","")
dnsOutput = dnsOutput.replace("DNS:","")

publicIP = load(urlopen('https://api.ipify.org/?format=json'))['ip']

print "----------- MACHINE INFORMATION -----------"
print "HOSTNAME:        "+hostname
print "PUBLIC IP:       "+publicIP
print "LOCAL IP:        "+ipOutput
print "NETMASK:         "+netmaskOutput
print "DEFAULT GATEWAY: "+gatewayOutput
print "DNS SERVERS:     "
print dnsOutput
print "-------------------------------------------"

