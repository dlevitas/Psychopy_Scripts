
#idea: output should be prefixed, not raw print
try:
    import psychopy
except ImportError:
    raise RuntimeError("You can only run this from PsychoPy's Python environment.  Start PsychoPy, go to the Coder view, and run this in the Shell tab instead")
import os
import shutil

import platform
dev = platform.node() in ('JoshWin','Lina')


def symlink(source, link_name):
    import ctypes
    csl = ctypes.windll.kernel32.CreateSymbolicLinkW
    csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
    csl.restype = ctypes.c_ubyte
    flags = 0
    if source is not None and os.path.isdir(source):
        flags = 1
    if csl(link_name, source, flags) == 0:
        raise ctypes.WinError()

home=os.path.expanduser("~")+"/"
config=home+".JkPsychoPy/"
package=config+'/jkpsycho/'
changed=False

if os.path.exists(config):
    shutil.rmtree(config)

if dev:
    os.makedirs(config)
    symlink(os.path.abspath('jkpsycho'),package)
    #os.link('jkpsycho',package)
else:
    shutil.copytree('jkpsycho',package)

# register extra components folder
paths=psychopy.prefs.builder['componentsFolders']
if package not in paths:
    changed=True
    paths.append(package)

# register extra coder paths
paths=psychopy.prefs.general['paths']
if config not in paths:
    changed=True
    paths.append(config)



if changed:
    psychopy.prefs.validate()
    psychopy.prefs.saveUserPrefs()
    #print('please restart PsychoPy for the changes to take effect')
else:
    #print('should be ready to go!')
    pass
# always need to restart for some reason.  PsychoPy might not reimport components on build?
print('please restart PsychoPy for the changes to take effect')
