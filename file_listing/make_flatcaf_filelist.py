from __future__ import print_function
import sys
import os
#import samweb_cli
#from ROOT import TFile, gDirectory
import subprocess

input_dir = "/pnfs/sbnd/scratch/users/sungbino/sbnd_2025_prod/2025A_Spring25Dev_MC_intimecosmics/caf/"
ls_output = subprocess.run(['ls',input_dir], stdout=subprocess.PIPE, universal_newlines=True)

output_file = "./list_2025A_spring_mc_intimecosmic_nosce_sungbino.txt"
f = open(output_file,'a')

# Check if ls command executed successfully
if ls_output.returncode == 0:
    # Split the output into a list of filenames and directories
    file_list = ls_output.stdout.split('\n')
    # Remove the empty string from the end of the list
    file_list = file_list[:-1]
    
    # Display the list
    print("Files and directories:")
    for item in file_list:
        print(item)

        this_ls_output = subprocess.run(['ls',input_dir + item], stdout=subprocess.PIPE, universal_newlines=True)
        this_file_list = this_ls_output.stdout.split('\n')
        this_file_list = this_file_list[:-1]
        #print(this_file_list)

        for this_item in this_file_list:
            #if "hists_prodgenie" in this_item and "Reco2" in this_item and "json" not in this_item:
            if "flat.caf" in this_item and "json" not in this_item:
                this_line = input_dir + item + '/' + this_item + '\n'
                stream = os.popen("./my_pnfsToXRootD %s" % (this_line))
                xroot = stream.read()
                print(xroot)
                f.write(xroot)
else:
    print("Error:", ls_output.stderr)

f.close()
