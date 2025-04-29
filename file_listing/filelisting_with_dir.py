from __future__ import print_function
import sys
import os
import samweb_cli
from ROOT import TFile, gDirectory
import subprocess

Sample = ["list_2025A_Sprint25Dev_mc_intimecosmics_reco2_sungbino.txt", "/pnfs/sbnd/scratch/users/sungbino/sbnd_2025_prod/2025A_Spring25Dev_MC_intimecosmics/reco2"]

outFileList = Sample[0]
inputDir = Sample[1]

def list_files(directory="."):
    try:
        # Run the ls command and capture the output
        result = subprocess.run(["ls", directory], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Split the output into a list of file names
        file_list = result.stdout.strip().split('\n')

        return file_list
    except subprocess.CalledProcessError as e:
        print(f"Error executing 'ls' command: {e}")
        return []

# Example usage
files = list_files(inputDir)

f = open(outFileList, "w")

for file in files:
    if "root" in file:
        stream = os.popen("./my_pnfsToXRootD %s/%s" % (inputDir,file))
        xroot = stream.read()
        print(xroot)
        #tfile = TFile.Open(xroot.strip())
        #mytree = gDirectory.Get('caloskim/TrackCaloSkim')
        #totalevts = mytree.GetEntries()
        #print("totalevts : %d", totalevts) 
        f.write(xroot)

f.close()
