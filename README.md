# unchunk.py  **v0.10**
Automation of compressing Sat-TV recordings into mp4

## Part 1: unchunk = concatenate
 
Sat-TV recordings are many 'chunk_[0-9].ts' (transport stream) files per movie.  
This script generates a DOS batch file to concatenate them together; and for several movies in subfolders, one after the other. A huge time saver.  

Then each concatenated 'targetname.ts' can be compressed with e.g. Handbrake.

### NEW: Now with GUI
Download the Windows binary ``unchunk.exe``

* [unchunk_v0.10.zip](releases/unchunk_v0.10.zip)

Or if you have Python 2.7 installed (but read the part about the images in [pyinstaller.md](pyinstaller.md)):

    pip install gooey
    python unchunkGooey.py 

If wxPython is not yet installed, see [Chris' instructions](https://github.com/chriskiehl/Gooey#installation-instructions). In Anaconda it is simply:

    conda install wxpython


### Stay Tuned
This is work in progress. More coming soon.

## Support Me

If you like this, show it: Send Bitcoin to [15c3a2E7b3TZuzeoYQyBSj7zAZmsBFyom7](http://blockr.io/address/info/15c3a2E7b3TZuzeoYQyBSj7zAZmsBFyom7) - thanks.

![15c3a2E7b3TZuzeoYQyBSj7zAZmsBFyom7](http://blockr.io/api/v1/address/Qr/15c3a2E7b3TZuzeoYQyBSj7zAZmsBFyom7)  

---
https://github.com/drandreaskrueger/unchunk 2016-01-31
