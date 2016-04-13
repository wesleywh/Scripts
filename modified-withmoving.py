import os, socket, json, time                   #for file timse, os commands, jsons, threading
import subprocess                               #for system process
import shutil, errno                               #for file copy

def all_files_in_dir():
    process = os.popen('forfiles /C "cmd /c echo @file @fdate @ftime"')
    result = process.read()
    process.close()
    mod_list = []
    for root, dirs, files in os.walk("."):                      #find all dirs and files in directory that this file is in
        directory = {}
        directory['DIR'] = root.strip().replace("\\\\","\\")    #helps with file getting bloated on updates (otherwise adds more slashs)
        directory['NAME'] = ''
        directory['TYPE'] = 'DIR'
        directory['MODIFIED'] = ''
        mod_list.append(directory)                              #list of directories
        for file in files:              
            if file != '.' or file != '..':
                path = os.path.join(root, file)                 #get the directory path to this file (starting from root directory)
                data = {}
                data['DIR'] = root.strip().replace("\\\\","\\") #helps with file getting bloated on updates (otherwise adds more slashs)
                data['NAME'] = file.strip()
                data['TYPE'] = 'FILE'
                data['MODIFIED'] = os.path.getmtime('\\\\?\\'+ os.path.abspath(path)) + os.path.getctime('\\\\?\\'+ os.path.abspath(path))#get the files modified time (float format)
                print("1/4 Scanning Files: "+data['DIR']+"\\"+data['NAME'], end='\r')
                mod_list.append(data)                           #list of files and the directories they are in
    print("")
    print("...Done.")
    return mod_list                                             #return JSON list of all dirs and files in this directory

def open_db_file():
    if os.path.isfile("last_modified.txt") == False:
        open("last_modified.txt", 'a')

    return "last_modified.txt"

def return_file_contents(filename):
    list = []
    with open(filename) as file:
        for line in file:
            line = line.split('\n')[0]                      #remove "\n" since this messes up JSON format
            line = line.split('\r')[0]                      #remove "\r" since this messes up JSON format
            line = line.replace("'","")                     #remove quotes since this messes up JSON format
            line = line.replace("\"","")                    #remove quotes since this messes up JSON format
            line = line.replace("\\\\","\\")                #this prevents additional slashs being added
            line = line.replace("}","")                     #this helps to parse JSON vars
            line = line.replace("{","")                     #removing this helps to parse JSON vars
            json = line.split(",")                          #key-value seperated by commas
            data = {}                                       #rebuild JSON list
            data[json[0].split(':')[0].strip()] = json[0].split(':')[-1].strip()    
            data[json[1].split(':')[0].strip()] = json[1].split(':')[-1].strip()
            data[json[2].split(':')[0].strip()] = json[2].split(':')[-1].strip()
            data[json[3].split(':')[0].strip()] = json[3].split(':')[-1].strip()
            print("2/4 Scanning DB File:"+data['DIR']+"\\"+data['NAME'], end='\r')
            list.append(data)
    print ("")
    print ("...Done.")
    return list

def find_updates(files):
    filename = open_db_file()                               #get filename of db file (or creates it)
    contents = return_file_contents(filename)               #list of files in db file
    deletedFiles = find_deleted_files(files, contents)      #return a list of deleted files
    if len(deletedFiles) > 0:
        for deleted in deletedFiles:
            print("Found Deleted File(s): "+deleted['NAME'])
            contents.remove(deleted)                        #remove all deleted files from the db file
    print("...Done.")
    names = find_values('NAME',contents)
    dirs = find_values('DIR',contents)
    updates = []                                            #list of items to move

    print("4/4 Finding All Modified Files...")
    for item in files:
        print(item['DIR'],end='\r')
        if item['NAME'] != '' and item['NAME'] != '.' and item['NAME'] != '..' and item['NAME'] not in names:#Never before used filename
            contents.append(item)                           #add new item to db file (done later)
            updates.append(item)                            
        elif item['NAME'] != '' and item['NAME'] in names:  #Name currently used
            if item['DIR'] not in dirs:                     #This is a new directory
                contents.append(item)                       #add new directory to db file (done later)
                updates.append(item)    
            elif item['DIR'] in dirs:                       #Directory currently used
                original = match_contents(item, contents)   #return matching file
                if (float(original['MODIFIED']) != float(item['MODIFIED']) and 
                item['NAME'] != 'last_modified.txt' and item['NAME'] != 'modified.py'):    #file been modified?
                    contents[contents.index(original)] = item   #Update line in db file (done later)
                    updates.append(item)
    print("")
    print('...Done.')
    # write_changes(filename, contents)
    return updates, deletedFiles

def find_deleted_files(folderContents, dbFileContents):     #returns a list of deleted files since last sync
    deleted = []
    print("3/4 Finding Deleted Files...")
    for content in dbFileContents:
        obj = match_contents(content, folderContents)       #match the db file with the actual file
        if obj == []:                
            print("Found: "+obj['NAME'],end='\r')
            deleted.append(content)                         #if it can't find a match then it has been deleted
    return deleted

def find_values(id, jsonArray):
    output = [];
    for jsonObj in jsonArray:
        output.append(jsonObj[id])
    return output

def match_contents(item, jsonArray):                        #used to find value from key value in json array
    output = [];
    for json in jsonArray:                                  #find the original file that item is referencing
        if json['NAME'] == item['NAME'] and json['DIR'] == item['DIR']:
            output = json
    return output                                           #return that original file

def write_changes(filename, contents):
    open(filename, 'w').close()                             #clear the file
    file = open(filename, 'w')                              #Open the file for writing
    for item in contents:                                   #simply add everything in 'contents' array to file
        file.write(json.dumps(item))
        file.write('\n')
    file.close()                                            #close the file when done

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    # if os.path.isdir(src):
    #     shutil.copytree(src, dst, symlinks, ignore)
    # else:
    #     shutil.copy2(src, dst)

def move_files(updates):
    for file in updates:
        if file['DIR'] == '.' or file['DIR'] == '..':
            file['DIR'] = "\\"
        else: 
            file['DIR'] = file['DIR'].replace(".\\\\","\\")
            file['DIR'] = file['DIR']+"\\"

        currentDirectory = os.path.dirname(os.path.realpath(__file__));
        filepath = currentDirectory+file['DIR']+file['NAME']
        filepath = filepath.replace(".\\","\\")
        copyToDirectory = 'C:\\Users\\wesleywh\\Desktop\\Copies'+file['DIR']+file['NAME']
        copyToDirectory = copyToDirectory.replace(".\\","\\")
        copyToDirectory = copyToDirectory.replace("\\\\","\\")
        copytree(filepath, copyToDirectory)

def main():
    os.system('cls')
    print ('='*10,"Reading Modified Files in Current Dir",'='*10)
    print (' '*5,'-'*5,"1/2 Finding All Modified Files",'-'*5)
    print("")
    files = all_files_in_dir()
    updates, deleted = find_updates(files)
    print("")
    print(len(updates),"File(s) have been added or modified")
    print (len(deleted),"Files(s) have been moved or deleted")
    print("")
    print (' '*5,'-'*7,"2/2 Moving Modified Files",'-'*6)
    move_files(updates)
main()