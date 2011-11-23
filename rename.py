#!/usr/bin/env python

import os
import sys

if len(sys.argv) == 1:
    cdir = "."
else:
    cdir = sys.argv[1]

dircontents = os.listdir(cdir)
renamelist = []

for f in dircontents:
    if f.find("corrS") >= 0:
        plot_type = "corrS"
        plot_name = f[7:-4]
        plot_ext = f[-4:]
        oldname = f
        newname = plot_name+"--"+plot_type+plot_ext
        renamelist.append([oldname,newname])
    elif f.find("hist") >= 0:
        plot_type = "hist"
        plot_name = f[6:-4]
        plot_ext = f[-4:]
        oldname = f
        newname = plot_name+"--"+plot_type+plot_ext
        renamelist.append([oldname,newname])
    else:
        pass

print "Files will be renamed as follows:"
for rnm in renamelist:
    print rnm[0],"--->",rnm[1]

yn = raw_input("Is this OK?")
if yn == "y" or yn == "Y":
    for rnm in renamelist:
        os.rename(rnm[0],rnm[1])

print "Done!"


