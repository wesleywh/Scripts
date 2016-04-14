import os,sys               #for system commands
import argparse             #used for allowing command line switches 
from stat import *          #for stat command
import datetime             #used for float to datetime

def convert(bytes, type):
    text = ""
    if bytes < 1024:
        number = bytes
        text = "BYTES"
    elif bytes >= 1025 and bytes < 1048576:
        number = bytes/1024
        text = "KB"
    elif bytes >= 1048577 and bytes < 1073741824:
        number = number = bytes/1048576
        text = "MB"
    elif bytes >= 1073741825:
        number = bytes/1073741824 
        text = "GB"
    return str(round(number,2))+" "+text

def main():
    #Available command line options
    parser = argparse.ArgumentParser(description='Available Command Line Switches')
    parser.add_argument('-F',metavar='F', nargs="+", help="Target File To Scan")

    #all all available arguments to the 'args' variable
    args = parser.parse_args()
    for filePath in args.F:
        try:
            st = os.stat(os.path.abspath(filePath))
            # print(st)
            print("File Permissions","."*20,filemode(st.st_mode))
            print("Size","."*32,convert(st.st_size, "MB"))
            print("User ID","."*29,st.st_uid)
            print("Group ID","."*28,st.st_gid)
            print("Creation Time","."*23,datetime.datetime.fromtimestamp(st.st_ctime))
            print("Last File Access","."*20,datetime.datetime.fromtimestamp(st.st_atime))
            print("Last Mod Time","."*23,datetime.datetime.fromtimestamp(st.st_mtime))
            print("Symbolic Link","."*23,S_ISLNK(st.st_mode))
            print("Device","."*30,st.st_dev)
            # print("st_mode:",st.st_mode)        #protection bits
            # print("st_ino:",st.st_ino)          #inode number
            # print("st_dev:",st.st_dev)          #device
            # print("st_nlink:",st.st_nlink)      #number of hard links (number of locations in the file system)
            # print("st_uid:",st.st_uid)          #user id of owner
            # print("st_gid:",st.st_gid)          #group id of owner
            # print("st_size:",st.st_size)        #size of file, in bytes
            # print("st_atime:",st.st_atime)      #time of most recent access
            # print("st_mtime:",st.st_mtime)      #time of most recent content modification
            # print("st_ctime:",st.st_ctime)      #windows = time of creation, unix = time of most recent metadata change
            # print("is directory:",S_ISDIR(st.st_mode)) #is it a directory?
            # print("Character Special Device:",S_ISCHR(st.st_mode)) #Return non-zero if the mode is from a character special device file.
            # print("block special device file:",S_ISBLK(st.st_mode)) #Return non-zero if the mode is from a block special device file.
            # print("Regular File:",S_ISREG(st.st_mode)) #Return non-zero if the mode is from a regular file.
            # print("FIFO (named pipe):",S_ISFIFO(st.st_mode)) #Return non-zero if the mode is from a FIFO (named pipe).
            # print("symbolic link:",S_ISLNK(st.st_mode)) #Return non-zero if the mode is from a symbolic link..
            # print("Is Socket:",S_ISSOCK(st.st_mode)) #Return non-zero if the mode is from a socket.
            # print("Is Door:",S_ISDOOR(st.st_mode)) #Return non-zero if the mode is from a door.
            # print("Event Port:",S_ISPORT(st.st_mode)) #Return non-zero if the mode is from an event port.
            # print("whiteout:",S_ISWHT(st.st_mode)) #Return non-zero if the mode is from a whiteout.
            # try:
            #     print("file’s permission bits:",S_IMODE(st.st_mode)) #Return the portion of the file’s mode that can be set by os.chmod()—that is, the file’s permission bits, plus the sticky bit, set-group-id, and set-user-id bits (on systems that support them).
            # except:
            #     print("file's permission bits: Unable To Determine")
            # print("file type:",S_IFMT(st.st_mode)) #Return the portion of the file’s mode that describes the file type (used by the S_IS*() functions above).


        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        except ValueError:
            print ("Could not convert data to an integer.")
        except:
            print ("Unexpected error:", sys.exc_info()[0])

main()