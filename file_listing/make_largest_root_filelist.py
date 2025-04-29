from __future__ import print_function
import sys
import os
import subprocess

input_dir = "/pnfs/sbnd/scratch/users/sungbino/sbnd_2025_prod/2025A_Spring25dev_data_new_ccal/caf/"
output_file = "./list_2025A_spring_data_flatcaf_new_ccal.txt"

# List subdirectories in input_dir
ls_output = subprocess.run(['ls', input_dir], stdout=subprocess.PIPE, universal_newlines=True)

with open(output_file, 'w') as f:
    if ls_output.returncode == 0:
        file_list = ls_output.stdout.strip().split('\n')

        print("Processing directories...")

        for item in file_list:
            subdir = os.path.join(input_dir, item)

            # List files in this subdir
            try:
                this_ls_output = subprocess.run(['ls', subdir], stdout=subprocess.PIPE, universal_newlines=True)
                this_file_list = this_ls_output.stdout.strip().split('\n')

                # Filter for relevant ROOT files
                filtered_files = [
                    fname for fname in this_file_list
                    if "json" not in fname and fname.endswith(".root")
                ]

                if not filtered_files:
                    continue

                # Find the largest file
                largest_file = max(
                    filtered_files,
                    key=lambda f: os.stat(os.path.join(subdir, f)).st_size
                )

                full_path = os.path.join(subdir, largest_file)

                # Convert to XRootD path using your script
                stream = os.popen(f"./my_pnfsToXRootD {full_path}")
                xroot_path = stream.read().strip()

                print(f"[✓] {xroot_path}")
                f.write(xroot_path + '\n')

            except Exception as e:
                print(f"[✗] Error processing {item}: {e}")

    else:
        print("Error:", ls_output.stderr)
