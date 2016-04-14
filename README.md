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

IP Address ................... 10.10.10.101
Subnet Mask .................. 255.255.255.0
Default Gateway .............. 10.10.10.10

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
0 File(s) have been modified
0 Files(s) have been moved or deleted
```
####metadata.py
This will attempt to display the metadata for a file. You will need to specify a single file or list of files to scan like the following:
```
python metadata.py -F last_modified.txt
```
The output will look like the following:
```
File Permissions .................... -rw-rw-rw-
Size ................................ 0 BYTES
User ID ............................. 0
Group ID ............................ 0
File Owner(s) ....................... NT AUTHORITY\SYSTEM:(I)(F)
                                      BUILTIN\Administrators:(I)(F)
                                      PMPC-AD\wesleywh:(I)(F)
                                      PMPC-AD\RichardRobins:(I)(F)
Creation Time ....................... 2016-04-11 09:27:42.605286
Last File Access .................... 2016-04-11 09:27:42.605286
Last Mod Time ....................... 2016-04-13 12:17:49.844588
Symbolic Link ....................... False
# of Locations on System ............ 1
Device .............................. 1719608249
```
