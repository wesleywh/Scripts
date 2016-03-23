import socket,struct
import os
import subprocess
import platform 
from ctypes import *
from ctypes.wintypes import *

def get_netmask(ip):
	proc = subprocess.Popen('ipconfig',stdout=subprocess.PIPE)
	while True:
		line = proc.stdout.readline()
		if ip.encode() in line:
			break
	mask = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ',b'').decode()
	return mask
	
def os_bit_version():
	if os.environ['PROGRAMFILES(X86)']:
		return "64-Bit"
	else:
		return "32-Bit"

def main():
	os.system('cls')
	print ("-"*20,"Computer Information","-"*20)
	print ("Computer Name","."*16,socket.gethostname())
	internal_ip = socket.gethostbyname(socket.gethostname())
	print ("IPAddress","."*20,internal_ip)
	print ("Subnet Mask","."*18,get_netmask(internal_ip))
	print ("OS Type","."*22,os_bit_version())

main()