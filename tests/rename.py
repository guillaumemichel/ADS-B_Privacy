from os import listdir, rename
from os.path import isfile, join

mypath = '../data/recordings/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for f in files:
    rename(mypath+f, mypath+f[1:])
