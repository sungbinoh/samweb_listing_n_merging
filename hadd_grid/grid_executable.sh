# Setup grid submission

export TIER="reco2"
outDir=$1
echo "@@ outDir : ${outDir}"

echo "@@ pwd"
pwd
echo "@@ ls -alh"
ls -alh
echo "@@ mkdir output"
mkdir output
echo "@@ Done!"
thisOutputCreationDir=`pwd`/output/
filesFromSender=${CONDOR_DIR_INPUT}/grid_dir/grid_dir/

echo "@@ ls -alh ${filesFromSender}"
ls -alh ${filesFromSender}/

nProcess=$PROCESS
echo "@@ nProcess : "${nProcess}

# Assuming ICARUS
echo "@@ setup_sbnd.sh"
source /cvmfs/sbnd.opensciencegrid.org/products/sbnd/setup_sbnd.sh

#setup ifdhc
# Match to your input CAFs sbnanaobj
setup sbndcode v10_04_06_01 -q e26:prof
#setup sbnana v09_78_06 -q e20:prof
#setup sbnanaobj v09_23_02_01 -q e26:prof
# Set if your input CAFs has GENIE records
#setup genie v3_04_00d -q e20:prof

export IFDH_CP_MAXRETRIES=2

echo "@@ outDir : "${outDir}
echo "@@ ifdh  mkdir_p "${outDir}
ifdh  mkdir_p ${outDir}

echo "@@ source ${filesFromSender}/run_"${nProcess}".sh "${thisOutputCreationDir}
source ${filesFromSender}/run_${nProcess}.sh ${thisOutputCreationDir} &> ${thisOutputCreationDir}/log_${nProcess}.log
echo "@@ Check output : ${thisOutputCreationDir}/${TIER}_${nProcess}.root"
ls -alh ${thisOutputCreationDir}/${TIER}_${nProcess}.root

outFILE=${thisOutputCreationDir}/${TIER}_${nProcess}.root
if [ -f "$outFILE" ]; then
  echo "ifdh cp ${thisOutputCreationDir}/${TIER}_${nProcess}.root ${outDir}/${TIER}_${nProcess}.root"
  ifdh cp ${thisOutputCreationDir}/${TIER}_${nProcess}.root ${outDir}/${TIER}_${nProcess}.root
  echo "ifdh cp ${thisOutputCreationDir}/log_${nProcess}.log ${outDir}/log_${nProcess}.log"
  ifdh cp ${thisOutputCreationDir}/log_${nProcess}.log ${outDir}/log_${nProcess}.log
  echo "@@ Done!"
else
  echo "File not exist"
fi

