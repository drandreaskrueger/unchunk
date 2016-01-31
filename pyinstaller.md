# PyInstaller
The steps I took to make the *.exe

(Perhaps I should have [used anaconda](https://anaconda.org/auto/pyinstaller), but instead I did:)

    pip install pyinstaller
    
Then I adapted Chris' [build.spec](https://github.com/chriskiehl/Gooey/files/29568/build.spec.txt) into this [build.spec](build.spec), by changing ``unchunkGooey.py`` and and ``pathex`` and ``unchunk``, and ``icon=``.   

It took an hour of fiddling and learning, until I found out that with the given ``console=False`` it would not work. Then 

    pyinstaller build.spec
    
finally generated a working executable.  

### images missing
I copied the whole Gooey/gooey/images/ folder [into my repo](images), and overwrote those images that I wanted changed. http://icoconvert.com/ was useful for PNG-->ICO conversion of the ``program_icon.ico``.

When running ``unchunkGooey.py`` it did work to use the Gooey parameter 

    @Gooey (image_dir='images')
    
But the executable built by pyinstaller then complained with:

    File "site-packages\gooey\gui\image_repository.py", line 35, in patch_images
    IOError: Unable to find the user supplied directory images
    
which is a problem in
    
    def patch_images(new_image_dir)
    
because there, the current path is ``/dist/`` - and there is no ``images`` folder.

#### Hacked workaround    
    
In the end, I decided to remove the 

    @Gooey (image_dir='images')
    
and instead pretend to be using the default images, by

    @Gooey ()  

and then manually override the ``gooey_images`` in ``build.spec``:

    import os
    my_root = os.getcwd()
    my_images = Tree(os.path.join(os.getcwd(), 'images'), prefix = 'gooey/images')
    gooey_images = my_images 
    
It is a dirty hack, because now my icons are not shown anymore, when I am running ``unchunkGooey.py`` via Python - but the images do get included into the ``unchunk.exe`` binary - great!

Please help me: How to correctly extend the ``build.spec`` in case of ``@Gooey (image_dir='images')``?  Or must the ``image_dir`` path be absolute? But how to collect the images from there?
 
Thanks a lot!

