# PyInstaller
The steps I took to make the *.exe

(Perhaps I should have [used anaconda](https://anaconda.org/auto/pyinstaller), but instead I did:)

    pip install pyinstaller
    
Then I adapted Chris' [build.spec](https://github.com/chriskiehl/Gooey/files/29568/build.spec.txt) into this [build.spec](build.spec), by changing ``unchunkGooey.py`` and and ``pathex`` and ``unchunk``. It took an hour of fiddling and learning, until I found out that without ``console=True`` it would not work. Then 

    pyinstaller build.spec
    
finally generated an executable.  

I copied the whole Gooey/gooey/images/ folder, and overwrote those images that I wanted changed.

 


    
