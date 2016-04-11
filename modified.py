import os, socket, json, time
import subprocess

def all_files_in_dir():
    process = os.popen('forfiles /C "cmd /c echo @file @fdate @ftime"')
    result = process.read()
    process.close()
    mod_list = []
    for root, dirs, files in os.walk("."):
        # dirs = array of all found directories
        # path = root.split('/')
        # print (os.path.basename(root))
        directory = {}
        directory['DIR'] = root.strip().replace("\\\\","\\")
        directory['NAME'] = ''
        directory['TYPE'] = 'DIR'
        directory['MODIFIED'] = ''
        mod_list.append(directory)
        for file in files:
            filename, ext = os.path.splitext(file)
            if file != '.' or file != '..':
                path = os.path.join(root, file)
                data = {}
                data['DIR'] = root.strip().replace("\\\\","\\")
                data['NAME'] = file.strip()
                data['TYPE'] = 'FILE'
                data['MODIFIED'] = os.path.getmtime(path) + os.path.getctime(path)
                mod_list.append(data)

    return mod_list

def open_db_file():
    if os.path.isfile("last_modified.txt") == False:
        open("last_modified.txt", 'a')

    return "last_modified.txt"

def return_file_contents(filename):
    list = []
    with open(filename) as file:
        for line in file:
            line = line.split('\n')[0]
            line = line.replace("'","")
            line = line.replace("\"","")
            line = line.replace("}","")
            line = line.replace("{","")
            json = line.split(",")
            data = {}
            data[json[0].split(':')[0].strip()] = json[0].split(':')[-1].strip()
            data[json[1].split(':')[0].strip()] = json[1].split(':')[-1].strip()
            data[json[2].split(':')[0].strip()] = json[2].split(':')[-1].strip()
            data[json[3].split(':')[0].strip()] = json[3].split(':')[-1].strip()
            list.append(data)
    return list

def find_updates(files):
    filename = open_db_file()
    contents = return_file_contents(filename)
    # print(contents)
    names = find_values('NAME',contents)
    print (len(names))
    dirs = find_values('DIR',contents)
    updates = []                                            #list of items to move

    for item in files:
        if item['NAME'] != '' and item['NAME'] not in names:#Never before used filename
            contents.append(item)                           #add new item to db file (done later)
            updates.append(item)                            
        elif item['NAME'] != '' and item['NAME'] in names: #Name currently used
            if item['DIR'] not in dirs:                    #This is a new directory
                contents.append(item)                      #add new directory to db file (done later)
                updates.append(item)    
            elif item['DIR'] in dirs:                      #Directory currently used
                obj = match_contents(item, contents)       #return matching file
                if obj['MODIFIED'] != item['MODIFIED']:    #file been modified?
                    contents[contents.index(obj)] = item   #Update line in db file (done later)
                    updates.append(item)

    write_changes(filename, contents)
    return updates

def find_values(id, jsonArray):
    output = [];
    for jsonObj in jsonArray:
        output.append(jsonObj[id])
    return output

def match_contents(item, jsonArray):                        #used to find value from key value in json array
    output = [];
    for json in jsonArray:
        if json['NAME'] == item['NAME'] and json['DIR'] == item['DIR']:
            output = json
    return output

def write_changes(filename, contents):
    open(filename, 'w').close()         #clear the file
    file = open(filename, 'w')          #Open the file for writing
    for item in contents:               #simply add everything in 'contents' array to file
        file.write(json.dumps(item))
        file.write('\n')
    file.close()                        #close the file when done

def main():
    print ('-'*10,"Reading Modified Files in Current Dir",'-'*10)
    # file = open(filename, 'w')
    files = all_files_in_dir()
    updates = find_updates(files)

    # f.write('hi there\n')
    # f.close()

main()