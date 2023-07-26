from os import listdir, remove
from shutil import rmtree
from time import sleep

for fname in ["node_modules", "__pycache__"]:
    try:
        rmtree("{}/".format(fname))
    except:
        pass


for fol in ["input", "output"]:
    try:
        for f in listdir("{}/".format(fol)):
            remove("{}/{}".format(fol, f))
    except:
        pass

print("Done")
sleep(1)