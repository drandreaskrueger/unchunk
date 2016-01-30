'''
unchunkGooey.py

@summary: GUI for unchunk.py - see explanations there. 

@license: If you like this, send Bitcoin to 15c3a2E7b3TZuzeoYQyBSj7zAZmsBFyom7 
@author:  Andreas Krueger (github.com/drandreaskrueger)

@since:   Created on 9 Jan 2016

@version  v04

'''

import unchunk

import os, argparse
from gooey  import Gooey, GooeyParser
# NOT: pip install Gooey 
# BUT:
# git clone https://github.com/chriskiehl/Gooey.git
# python setup.py install
#
# also install wxPython
# https://github.com/chriskiehl/Gooey#installation-instructions




def gooey_transformArgs(args, parser, printBefore=False, printAfter=False):
  """Returns as dict all args ... exactly as given in args, 
     BUT those which are 'store_false' are inverted.
     See argparseBoolProblemSolved.py and 
     https://github.com/chriskiehl/Gooey/issues/148"""
     
  if printBefore: print args._get_kwargs()
  
  SFAs=[a.dest 
        for a in parser.parser._actions 
        if type(a)==argparse._StoreFalseAction]

  transformedArgs=[( k, (not v if k in SFAs else v) ) 
                   for k, v in args._get_kwargs()]
  
  print transformedArgs
  return dict(transformedArgs)

def gooey_checkParser(parser):
  """prints a WARNING if one of the dead checkbox combinations is used
     See argparseBoolProblemSolved.py and 
     https://github.com/chriskiehl/Gooey/issues/148
  """
  dead=[a.dest  
        for a in parser.parser._actions 
        if type(a) in (argparse._StoreFalseAction, argparse._StoreTrueAction)
        and a.default==a.const]
  if dead!=[]:
    print "WARNING: These combinations (default= and action=) lead to dead checkboxes:", 
    print dead    

@Gooey (monospace_display=True, default_size=(900, 600))
def gui():
  description=("Concatenate Sat-TV recordings (chunk_[0-9].ts), via a DOS batch file that is generated here.\n"
               "For several movies in subfolders. Then each concatenated 'targetname.ts' "
               "can be compressed with e.g. Handbrake.")  
  parser = GooeyParser(description=description)
  
  parser.add_argument("Source", default=unchunk.SOURCEFOLDER, help="Location of subfolders with chunk05.ts files", widget="DirChooser")
  parser.add_argument("Destination", default=unchunk.TARGETFOLDER, help="better on a different harddisk", widget="DirChooser")
  parser.add_argument('-f', '--fake', dest='fake', default=False, action="store_true", 
                      help="Fast. Just to see if working. But destination files are all wrong.")
  parser.add_argument("-e", "--execute", dest='execute', default=False, action="store_true" , 
                      help="Immediately run .bat file.")
  
  args=parser.parse_args()
  
  tArgs=gooey_transformArgs(args, parser, printBefore=True, printAfter=True)
  return tArgs

def boxedPrint(text):
  print "-" * len(text)
  print text
  print "-" * len(text)

def runUnchunk(A):
  copyCommand = "COPY" if A["fake"] else "COPY /B"
  # print copyCommand  
  
  batfile=os.path.join(A["Source"], unchunk.BATFILE)
  boxedPrint( "Generating the DOS .bat script '%s' that will concatenate all files per movie folder:" % (batfile))

  unchunk.unchunkSubfolders(source=A["Source"], destination=A["Destination"], copyCommand=copyCommand)

  if A["execute"]:
    print 
    boxedPrint("Now immediately execute that DOS .bat script:")
    

if __name__ == "__main__":
  tArgs=gui()
  runUnchunk(tArgs)
    
    