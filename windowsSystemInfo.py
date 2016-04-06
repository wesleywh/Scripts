import socket,struct
import os, re 
import subprocess
import platform 

# def get_workstation_info():
# 	proc = subprocess.Popen('net config workstation',stdout=subprocess.PIPE)
# 	info = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ',b'').decode()
# 	temp = []
# 	for line in proc.stdout:
# 		temp.append(line.rstrip().split(b':')[-1].decode());

# 	final = []
# 	for item in temp:
# 		values = item.split(" ")
# 		if values[0] != "" and (values[0] == "User" or values[0] == "Software" or values[1] == "Domain"):
# 			if values[0] == "Software":
# 				final.append(item.split(" ")[-3]+" "+item.split(" ")[-2]+" "+item.split(" ")[-1])
# 			else:
# 				final.append(item.split(" ")[-1])

# 	return final

def get_net_info():
	internal_ip = socket.gethostbyname(socket.gethostname())
	proc = subprocess.Popen('ipconfig',stdout=subprocess.PIPE)
	while True:
		line = proc.stdout.readline()
		if internal_ip.encode() in line:
			break
	mask = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ',b'').decode()
	gateway = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ',b'').decode()
	return [internal_ip, mask, gateway]

def os_bit_version():
	if os.environ['PROGRAMFILES(X86)']:
		return "64-Bit"
	elif os.environ['PROGRAMFILES']:
		return "32-Bit"
	else:
		return "Unable To Detect"

def get_mem():
	if os.name == "posix":
		value = linuxRam()
	elif os.name == "nt":
		value = windowsRam()
	else:
		print ("Unable To Detect")

	return value

def windowsRam():
	process = os.popen('wmic memorychip get capacity')
	result = process.read()
	process.close()
	memory = 0
	slots = 0;
	for value in result.split("\n"):
		if value.strip('').strip(' ').isdigit():
			memory += int(value.strip('').strip(' '))
			if value.strip('').strip(' ') != 0:
				slots += 1;
	# 1 GB = 1,073,741,824 Bytes
	totalMem = memory/1073741824
	return [totalMem, slots]

def linuxRam():
	totalMemory = os.popen("free -m").readlines()[1].split()[1]
	return int(totalMemory)

def main():
	os.system('cls')
	print ("-"*20,"Computer Information","-"*20)
	print ("")
	print ("Computer Name","."*16,socket.gethostname())
	print ("Current Domain","."*15, socket.getfqdn().split('.',1)[-1])
	print ("")
	netInfo = get_net_info()
	print ("IP Address","."*19,netInfo[0])
	print ("Subnet Mask","."*18,netInfo[1])
	print ("Default Gateway","."*14,netInfo[2])
	print ("")
	print ("OS Type","."*22,os_bit_version())
	version = platform.win32_ver()
	system = platform.system()
	print ("Logged In User","."*15, os.environ.get( "USERNAME" ))
	print ("Machine","."*22,system+" "+version[0])
	print ("Version","."*22,version[1]+", Service Pack: "+version[2])

	memory = get_mem();
	print ("RAM","."*26, memory[0],'GB')
	print ("RAM Slots Used","."*15, memory[1])

main()