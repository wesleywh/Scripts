# Scripts
This is a collection of helpful scripts and personal, just for fun, scripts that I have been writing.

####windowsSystemInfo.py
This will simply display basic information about your computer. Simply run it:
```
python windowsSystemInfo.py
```
and it will output information like the following:
```
-------------------- Computer Information --------------------

Computer Name ................ WorldWideWes
Current Domain ............... PMPC-AD.byu.edu

IP Address ................... 10.25.22.132
Subnet Mask .................. 255.255.255.128
Default Gateway .............. 10.25.22.129

OS Type ...................... 64-Bit
Logged In User ............... wesleywh
Machine ...................... Windows 10
Version ...................... 10.0.10240, Service Pack: SP0
RAM .......................... 8.0 GB
RAM Slots Used ............... 2
```

####modified.py
This is used as a syncing method to keep track of all deleted files and modified files. This will scan the directory it is located in (including all sub folder and files) and return a list of updated files or deleted files. It keeps track of all files that it has scanned in a file called "last_modified.txt". This is how it will know if a file as been updated or deleted. It stores it like a JSON object which is later parsed for its information. It stores the filename, the directory it is located in, if it is a directory or file, and the last modified time (in float format for easy comparison).

Simply run the file the following:
```
python modified.py
```
And it will output a file called "last_modified.txt" and show the following output in the console:
```
---------- Reading Modified Files in Current Dir ----------
No Modified Files
```
or if files are modified:
```
---------- Reading Modified Files in Current Dir ----------
816 Files or directories have been modified
```
