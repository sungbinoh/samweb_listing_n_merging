from __future__ import print_function
import sys
import os
import samweb_cli
from ROOT import TFile, gDirectory
import subprocess

#print(sys.argv[1])

#this_query = "production.type polaris and sbnd_project.stage reco2 and file_name like hist%run" + sys.argv[1] + "%"
this_query = "mc_MCP2025Av3_prodcorsika_proton_intime_sbnd_CV_reco2_sbnd"
samweb = samweb_cli.SAMWebClient(experiment='sbnd')
files = samweb.listFiles(defname=this_query)

f = open("list_Spring25Dev_mc_intimecosmics_flatcaf.txt", "w")

for file in files:
    loc = samweb.locateFile(file)
    print("loc: %s" % loc)
    pnfs = loc[0]['full_path'][8:]
    print("pnfs: %s" % pnfs)
    stream = os.popen("./my_pnfsToXRootD %s/%s" % (pnfs,file))
    xroot = stream.read()
    print("xroot: %s" % xroot)
    f.write(xroot)

f.close()
