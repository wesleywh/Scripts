import os, socket, json, time
import subprocess

def modifed_files():
    process = os.popen('forfiles /C "cmd /c echo @file @fdate @ftime"')
    result = process.read()
    process.close()
    lines = []
    print(os.getcwd())
    for root, dirs, files in os.walk("."):
        data = {}
        path = root.split('/')
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            data = {}
            # print(len(path) * '---', file)
            # print(len(path)*"----",os.path.getmtime(file))
            # print(len(path)*"----",os.path.getctime(file))
            data['NAME'] = file
            data['TYPE'] = 'FILE'
            data['MODIFIED'] = os.path.getmtime(file) + os.path.getctime(file)
            list.append(data)

    for line in result.split("\n"):
        if len(line) > 0:
            data = {}
            lastModified = date_time_serial(line.split('"')[-1].strip())
            data['MODIFIED'] = lastModified
            data['NAME'] = line.split('"')[1].strip()
            data9['TYPE'] = 'FILE'
            lines.append(data)

    return lines

def date_time_serial(time_date): 
    date = time_date.split(' ')[0].strip()
    date_numbers = date.split('/')
    date_number = 10000*float(date_numbers[2]) + 1000*float(date_numbers[0]) + float(date_numbers[1])

    time = time_date.split(' ')[-2].strip()
    time_numbers = time.split(':')
    if time_date.split(' ')[-1].strip() == "PM":
        time_numbers[0] = time_numbers[0] * 12

    time_number = 3600*float(time_numbers[0])+60*float(time_numbers[1])+float(time_numbers[2])

    serial_number = int(float(date_number)) + int(float(time_number))
    return serial_number

def check_db_file():
    if os.path.isfile("last_modified.txt") == False:
        open("last_modified.txt", 'a')

    return "last_modified.txt"

def main():
    print ("Reading Modified Files in Current Dir")
    filename = check_db_file()
    # f=open(filename, 'a')
    mod_files = modifed_files()
    # f.write('hi there\n')
    # f.close()

main()