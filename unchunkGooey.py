'''
unchunkGooey.py

@summary: GUI for unchunk.py - see explanations there. 

@license: If you like this, send Bitcoin to 15c3a2E7b3TZuzeoYQyBSj7zAZmsBFyom7 
@author:  Andreas Krueger (github.com/drandreaskrueger)

@since:   Created on 30 Jan 2016

'''

VERSION =                 "v0.11"

PRODUCTION = False # switches off a few debug logging lines

import unchunk

import os, argparse
from gooey  import Gooey, GooeyParser
# pip install Gooey
# if that does not work, then 
# git clone https://github.com/chriskiehl/Gooey.git
# python setup.py install
#
# also install wxPython
# https://github.com/chriskiehl/Gooey#installation-instructions

def gooey_checkParser(parser):
  """Prints a WARNING if one of the dead checkbox combinations is used
     See https://github.com/chriskiehl/Gooey/issues/148
     N.B.: Switch off in production. Just a helper during coding. 
  """
  dead=[a.dest  
        for a in parser.parser._actions 
        if type(a) in (argparse._StoreFalseAction, argparse._StoreTrueAction)
        and a.default==a.const]
  if dead!=[]:
    print "WARNING: These combinations (default= and action=) lead to dead checkboxes:", 
    print dead    


def gooey_transformArgs(args, parser, printBefore=False, printAfter=False):
  """Returns as dict all args ... exactly as given in args, 
     BUT those which are 'store_false' are inverted.
     See https://github.com/chriskiehl/Gooey/issues/148"""
     
  if printBefore: print "original parsed: ", args._get_kwargs()
  
  SFAs=[a.dest 
        for a in parser.parser._actions 
        if type(a)==argparse._StoreFalseAction]

  transformedArgs=[( k, (not v if k in SFAs else v) ) 
                   for k, v in args._get_kwargs()]
  
  if printAfter: print "transformed args:", transformedArgs
  return dict(transformedArgs)


def boxedPrint(text):
  """Attention seeker"""
  print "-" * len(text)
  print text
  print "-" * len(text)


# because of pyInstaller packaging: 
# http://chriskiehl.com/article/packaging-gooey-with-pyinstaller/
import sys
nonbuffered_stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
sys.stdout = nonbuffered_stdout


@Gooey (monospace_display=True, 
        default_size=(900, 600) 
        ) #, image_dir='images') # see pyinstaller.md why not

def gui():
  description=("(version %s) Concatenate Sat-TV recordings (chunk_[0-9].ts), "
               "via a DOS batch file that is generated here.\n"
               "For several movies in subfolders. Then each concatenated 'targetname.ts' "
               "can be compressed with e.g. Handbrake.")
  description = description % VERSION
  parser = GooeyParser(description=description)
  
  parser.add_argument("Source", default=unchunk.SOURCEFOLDER, help="Location of subfolders with chunk05.ts files", widget="DirChooser")
  parser.add_argument("Destination", default=unchunk.TARGETFOLDER, help="better on a different harddisk", widget="DirChooser")
  parser.add_argument('-f', '--fake', dest='fake', default=True, action="store_false", 
                      help="Fast. Just to see if working. But destination files will be broken.")
  parser.add_argument("-e", "--execute", dest='execute', default=True, action="store_false" , 
                      help="Immediately run the .bat file here.")
  
  if not PRODUCTION: gooey_checkParser(parser) 
  args=parser.parse_args()

  boxedPrint("unchunkGooey %s" % VERSION)  
  tArgs=gooey_transformArgs(args, parser, 
                            printBefore=not PRODUCTION, printAfter=not PRODUCTION)
  return tArgs


def boxedPrint(text):
  """Attention seeker"""
  print "-" * len(text)
  print text
  print "-" * len(text)


def runUnchunk(A):
  
  copyCommand = "COPY" if A["fake"] else "COPY /B"
  # print copyCommand  
  
  batfile=os.path.join(A["Source"], unchunk.BATFILE)
  boxedPrint( "Generating the DOS .bat script '%s' that will concatenate all files per movie folder:" % (batfile))

  unchunk.unchunkSubfolders(source=A["Source"], destination=A["Destination"], 
                            copyCommand=copyCommand, endWithPause=not A["execute"])

  if A["execute"]:
    print 
    boxedPrint("Now immediately execute that DOS .bat script:")
    os.system(batfile)
    

def warningFake(tArgs):
  if tArgs["fake"]:
    boxedPrint("Warning: Destination files are not useful. Edit, and run again with 'fake OFF'.")   

if __name__ == "__main__":
  tArgs=gui()
  runUnchunk(tArgs)
  warningFake(tArgs)
    