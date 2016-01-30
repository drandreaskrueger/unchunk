'''
unchunk.py

Automation of compressing Sat-TV recordings into mp4, part 1. 

@summary: 

Sat-TV recordings are many 'chunk_[0-9].ts' (transport stream) files per movie

This script generates a DOS batch file to concatenate them together; and 
for several movies in subfolders, one after the other. A huge time saver.

Then each concatenated 'targetname.ts' can be compressed with e.g. Handbrake.

@license: If you like this, send Bitcoin to 15c3a2E7b3TZuzeoYQyBSj7zAZmsBFyom7 
@author: Andreas Krueger (github.com/drandreaskrueger)

@since: Created on 9 Jan 2016

@version v03

'''

import os 


# source and destination ... ideally on two different disks:

# raw recordings ("chunks") from Sat-TV-receiver
SOURCEFOLDER= "G:\pvr"          
# Huge files, not FAT or FAT32! Continue there with Handbrake.
TARGETFOLDER= "H:\TODO"    

# DOS batch file that is the outcome of this Python script 
BATFILE="unchunk.bat"

# Please give generously:
DONATION = "15c3a2E7b3TZuzeoYQyBSj7zAZmsBFyom7"

# COMMAND = "copy /B" # "copy" # only for testing the script (wrongly copies non-binary files)
COMMAND = "copy /B"


def unchunkFiles(destination=TARGETFOLDER, copyCommand=COMMAND):
    """
    in the end, such a command is returned:
    copy /b chunk_1.ts+chunk2.ts+chunk3.ts "C:\targetdir\something.ts"

    how?
    
    gets all the file names in current dir
    extracts the .ts files, assuming they are called like 'chunk_12.ts'
    cuts out the numbers, casts to integer, and sorts them
    
    target name for concatenation is 'something.txt'
    there can be only one per folder
    when found --> 'something.ts'
    
    then put all together: 
    copy /b (sources.ts+) "destination.ts"
    """
    
    files=[ name for name in os.listdir(".") if os.path.isfile(os.path.join(".", name)) ]
    chunks=[name for name in files if os.path.splitext(name)[1]==".ts"]
    parts=[int(name[6:-3]) for name in chunks] # assumes "chunk_12.ts"
    parts.sort()
    
    unchunkedName=[name for name in files if os.path.splitext(name)[1]==".txt"]
    if len(unchunkedName)!=1: 
        print "none or several .txt files in this folder:"
        print os.getcwd()
        print unchunkedName
        print "Exiting. Please put ONE empty file 'targetname.txt' into each folder."
        exit() 
        
    unchunkedName = os.path.splitext( unchunkedName[0] ) [0] + ".ts"
    
    # now create the DOS command for binary copying:
    command = copyCommand + " "
    for p in parts:
        command += "chunk_%d.ts+" % p
    command = command[:-1] # remove last plus sign
    command += ' "' + os.path.join(destination, unchunkedName) + '"'
    
    return command 
    
def unchunkSubfolders(source=SOURCEFOLDER, destination=TARGETFOLDER, copyCommand=COMMAND):
    """
    change into topfolder
    get all the directories
    jump into each one,
    and execute unchunkFiles() there
    
    print all commands onto screen
    and into outfile o
    
    then close o
    """
    
    # this folder contains all the movie subfolders:
    os.chdir(source)
    
    # get the names of the movie subfolders:
    dirs=[ name for name in os.listdir(".") 
           if os.path.isdir(os.path.join(".", name)) 
          ]
    
    outfile=open(BATFILE,"w") # for writing
    
    def p(command, toScreen=True):
      "print and save the command"
      outfile.write(command + "\n")
      if toScreen: print command
    
    
    for folder in dirs:

        # into folder:
        os.chdir(folder)
        c = "cd %s" % folder
        p(c)
    
        # create copy command
        c=unchunkFiles(destination=destination, copyCommand=copyCommand)
        p(c)

        # out of folder
        os.chdir("..")
        c = "cd .."
        p(c)
        
    # there are some good people out there.
    p("@echo .", False)
    p("@echo .", False)
    p("@echo . Ready.")    
    p("@echo . If you like this, show it: [BTC] %s - thanks." % DONATION)
    p("@echo .", False)  
    
    # keep the window open when ready
    p("pause")    
    
    # close the written batch file:
    outfile.close()


if __name__ == "__main__":
  
    unchunkSubfolders()
    
    