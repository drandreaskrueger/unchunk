# unchunk.py
Automation of compressing Sat-TV recordings into mp4

## Part 1: unchunk = concatenate
 
Sat-TV recordings are many 'chunk_[0-9].ts' (transport stream) files per movie.  
This script generates a DOS batch file to concatenate them together; and for several movies in subfolders, one after the other. A huge time saver.  

Then each concatenated 'targetname.ts' can be compressed with e.g. Handbrake.

### stay tuned
This is work in progress. More coming soon.


