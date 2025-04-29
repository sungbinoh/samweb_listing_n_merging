import os

tier = "reco2"
Samples = [

  ["list_Spring25Dev_mc_intimecosmics_reco2.txt", "/pnfs/sbnd/scratch/users/sungbino/sbnd_2025_prod/2025A_Spring25Dev_MC_intimecosmics/reco2/"]

]

os.system('mkdir -p grid_dir')

for Sample in Samples:

  inputFileList = Sample[0]
  outDir = Sample[1]

  os.system('rm grid_dir/*')

  lines = open(inputFileList).readlines()
  NInputfiles = len(lines)

  print("@@ %s, number of files = %d"%(inputFileList, len(lines)))

  #NTarget = 100
  NTarget = 500
  #NTarget = 30
  #NTarget = 20

  flistForEachJob = []
  for i in range(0,NTarget):
    flistForEachJob.append( [] )

  for i_line in range(0,len(lines)):
    line = lines[i_line].strip('\n')
    flistForEachJob[i_line%NTarget].append(line)

  for i_flist in range(0,len(flistForEachJob)):

    flist = flistForEachJob[i_flist]
    out = open('grid_dir/run_%s.sh'%(i_flist),'w')
    out.write('#!/bin/bash\n')
    out.write('outDest=$1\n')

    ## hadd verseion
    cmd = 'hadd ${outDest}/%s_%d.root '%(tier, i_flist)
    for i_f in range(0,len(flist)):
      out.write('echo "[run_%s.sh] input %d : %s"\n'%(i_flist, i_f, flist[i_f]))
      cmd += ' '+flist[i_f]
    
    '''
    ## concat verseion
    cmd = 'concat_cafs'
    for i_f in range(0,len(flist)):
      out.write('echo "[run_%s.sh] input %d : %s"\n'%(i_flist, i_f, flist[i_f]))
      cmd += ' '+flist[i_f]
    cmd += ' ${outDest}/reco2_%d.root '%(i_flist)
    '''
    
    out.write(cmd)
    out.close()

  os.system('tar cf grid_dir.tar grid_dir/')

  submitCMD = '''jobsub_submit \\
-G sbnd \\
-e LC_ALL=C \\
--role=Analysis \\
--resource-provides="usage_model=DEDICATED,OPPORTUNISTIC" \\
-l '+SingularityImage=\\"/cvmfs/singularity.opensciencegrid.org/fermilab/fnal-wn-sl7:latest\\"' \\
--lines '+FERMIHTC_AutoRelease=True' --lines '+FERMIHTC_GraceMemory=1000' --lines '+FERMIHTC_GraceLifetime=3600' \\
--append_condor_requirements='(TARGET.HAS_SINGULARITY=?=true)' \\
--tar_file_name "dropbox://$(pwd)/grid_dir.tar" \\
--email-to sungbin.oh555@gmail.com \\
-N %d \\
--disk 100GB \\
--expected-lifetime 10h \\
"file://$(pwd)/grid_executable.sh" \\
"%s"'''%(NTarget,outDir)

  print(submitCMD)

  os.system(submitCMD)
