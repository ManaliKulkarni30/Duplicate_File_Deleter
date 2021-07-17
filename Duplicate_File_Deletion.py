#############################################################################
#
#  Author : Manali Kulkarni
#  Name : Automated Duplicate File Deletion
#  Date : 11 July 2021
#  About : Atomated python Script for Deleting duplicated files after periodic time in a given Directory.with email facility
#
#############################################################################

#Required Headers
from Header import *

#############################################################################

#Global Declaration
i = 0

############################################################################

#Helper Functions
def writeLog(duplicate):
    """
    name : writeLog
    param : list of duplicate files
    return:
    note : write log file and mail appropriate mail Id
    """
    global i
    today = date.today()
    Data = []

    if not os.path.exists("DuplicateFileLog"):
        os.mkdir("DuplicateFileLog")

    File_Path = os.path.join("MarvellousLog","Marvellous%s_%d.log"%(today,i))
    i = i + 1
    fd = open(File_Path,"w")
    fd.write("--------------------Deleted file List--------------------\n")

    for path in duplicate:
        fd.write("%s\n"%path)

    mail(File_Path)

########################################################################

def calculateChecksum(path,blocksize=1024):
    """
    param : directory path, block blocksize
    return : checksum of files
    """
    fd = open(path,'rb')
    hobj = hashlib.md5()

    buffer = fd.read(blocksize)
    while len(buffer) > 0:
        hobj.update(buffer)
        buffer=fd.read(blocksize)

    fd.close()
    return hobj.hexdigest()

###################################################################

def DirectoryTraversal(path):
    """
    name : traversal for directory
    param : Directory name
    return: duplacate Files
    """
    print("Contents of Directory")

    duplicate = {}
    for folder,subfolder,filename in os.walk(path):
        print("Directory Name: ",folder)
        for sub in subfolder:
            print("Sub Folder name: ",sub)
        for file in filename:
            print("File name: ",file)
            actualpath = os.path.join(folder,file)
            hash  = calculateChecksum(actualpath)


            if hash in duplicate:   #if checksum already exists
                duplicate[hash].append(actualpath)
            else:                  #if checksum does not exists
                duplicate[hash]=[actualpath]

    return duplicate

############################################################################

def DeleteDuplicate(path):
    """
    name: DeleteDuplicate
    param: path of directory
    return :
    """
    arr = {}
    arr = DirectoryTraversal(path)

    output = list(filter(lambda x : len(x)>1,arr.values()))
    dup = []
    if(len(output)>0):
        print("There are duplicate files.")
    else:
        print("There are not duplicate files")
        return

    print("List of duplicate files : ")
    icnt = 0
    for result in output:
        icnt = 0
        for path in result:
            icnt = icnt + 1
            if icnt >= 2:  #this logic skips the first file
                print("%s"%path)
                dup.append(path)
                os.remove(path)

    writeLog(dup)

###################################################################################

#Enter point function
def main():
    print("------------------------Manali KUlkarni--------------------------")
    print("------------------------------Duplicate File Deletion Script-----------------------------")

    if (len(argv)>3 and len(argv)<=3):
        print("ERROR : Invalid Number of Arguments")
        exit()


    if (argv[1]=="-h") or (argv[1]=="-H"):
        print("HELP : It is automated script for cleaning directory.")
        exit()

    if (argv[1]=="-u") or (argv[1]=="-U"):
        print("USAGE : FileName.py Name_of_Directory No_Of_Houres")
        exit()

    if not os.path.exists(argv[1]):
        print("Path Does not exists")
        exit()

    if not os.path.isabs(argv[1]):
        argv[1] = os.path.abspath(argv[1])
        print("Absolute path:",argv[1])

    schedule.every(int(argv[2])).hour.do(DeleteDuplicate,path=argv[1])#Passing argument to scheduled function
    while  True:
        schedule.run_pending()
        time.sleep(1)

######################################################################################

#Starter
if __name__ == '__main__':
    main()

#program execution command(Demo)
#>python Duplicate_File_Deletion.py Name_of_Directory 1
