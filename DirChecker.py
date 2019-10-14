import sys, os, subprocess

def main(directory):
    CONFIG = readConfig()
    if(CONFIG == -1):
        print("There is an error in the config file. Refer to header comment on how to structure the configuration.")
        return
    
    namelist = createNameList(directory, '_')

    OUT_FOLDER_NAME = "test"

    for name in namelist:
        zipLocation = directory + '/' + name['folder']
        dirLocation = directory + '/' + OUT_FOLDER_NAME

        if(name['status'] == 'OK'):
            extractRes = extractProjectFiles(zipLocation, OUT_FOLDER_NAME)
            if(extractRes != 0):
                name['status'] = 'FAIL'
                if(extractRes == -1):
                    name['error'] = 'Multiple zips found in students folder'
                elif(extractRes > 0):
                    name['error'] = 'The \'unzip\' command did not return a successful code'
        
        if(name['status'] == 'OK'):
            checkDirRes = checkDirectoryStructure(dirLocation, CONFIG)
            if(checkDirRes == 0):
                name['status'] = 'PASS'
                name['error']  = 'Directory matches desired structure'
            else:
                name['status'] = 'FAIL'
                # Error codes

    
    for name in nameList:
        print(nameToString(name))
    


def readConfig():
    f = open("CONFIG", "r")


## createNameList
#    Function to create a list of names from the names of the zip files in
#    the student submissions folder. Does not alter the files, just reads
#    their names.
def createNameList(directory, delim):
    nameList = []

    for filename in os.listdir(directory):
        fileArr = filename.split(delim)
        nameArr = fileArr[0].split(' ')
        curName = nameArr[1] + ", " + nameArr[0]
        nameList.append({
            'first': nameArr[0], 
            'last': nameArr[1], 
            'folder': filename, 
            'score': 0, 
            'status': 'OK', 
            'error': 'No errors occured'
        })
    
    return nameList


## extractProjectFiles
#    Function to unzip the file at 'directory' and name the folder 'outputFolder' 
def extractProjectFiles(directory, outputFolder):
    if(len(os.listdir(directory)) != 1):
        return -1

    files = os.listdir(directory)
    unzipRet = subprocess.call(["unzip", directory + "/" + files[0], "-d", directory + "/" + outputFolder])
    return unzipRet


## nameToString
#    Function to convert a name object to a human readable string
def nameToString(n):
    return n['last'] + ", " + n['first'] + ": " + n['status'] + " -> " + n['error']




if (len(sys.argv) < 2):
    print("You must provide a student submission folder name as an argument")
else:
    main(sys.argv[1])