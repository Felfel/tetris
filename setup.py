from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

data = []
for files in os.listdir('C:/Python34/Tetris/images'):
    f1 = 'C:/Python34/Tetris/images/' + files
    f2 = 'images', [f1]
    data.append(f2)
    
    
data.append(('sound', ['C:/Python34/Tetris/sound/game_loop.ogg']))
data.append(('sound', ['C:/Python34/Tetris/sound/main_loop.ogg']))
data.append(('fonts', ['C:/Python34/Tetris/fonts/LithosPro.otf']))


#Name of starting .py
script = 'tetris.py'

#Name of program
project_name = "Tetris"

#Project url
project_url = "about:none"

#Version of program
project_version = "0.0"

#Auhor of program
author_name = "Felfel"
author_e = "a.3lyounis@gmail.com"

#Description
project_description = "Classic old Tetris."

#Icon file (None will use pygame default icon)
icon_file = 'C:/Python34/Tetris/icon1.ico'


 
setup(
    data_files = data,
    version = project_version,
    description = project_description,
    name = "Tetris",
    url = project_url,
    author = author_name,
    author_email = author_e,
    
    options = {'py2exe': {'optimize': 2, 'bundle_files': 1, 'compressed':True} },
    windows = [{
            'script': script,
            'uac_info': "requireAdministrator",
            'icon_resources': [(1, icon_file)]
        }],
    zipfile = None,
)