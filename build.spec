import gooey
gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
# gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

#########################################
# hack, workaround, see pyinstaller.md
import os
my_root = os.getcwd()
my_images = Tree(os.path.join(os.getcwd(), 'images'), prefix = 'gooey/images')
gooey_images = my_images 
######################################### 

a = Analysis(['unchunkGooey.py'],              ### !
             pathex=['C:\\Anaconda\\Scripts'], ### !
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             )
             
pyz = PYZ(a.pure)

options = [('u', None, 'OPTION'), ('u', None, 'OPTION'), ('u', None, 'OPTION')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          options,
          gooey_languages, # Add them in to collected files
          gooey_images, # Same here.
          my_images, # fiddling without much success  ### !
          name='unchunk',  ### !
          debug=False,
          strip=None,
          upx=True,
          console=True,    ### !
          windowed=True,
          icon=os.path.join(my_root, 'images', 'program_icon.ico'))     ### !
