#!/bin/bash

#===============================================================#
#==== BASH SCRIPT TO RUN THE FAST ROTATION FOURIER ANALYSIS ====#
#===============================================================#

#== Parse command line arguments ==#

          tag=$1
inputRootFile=$2
     dataType=$3

#== Overwrite previous results with given tag ==#

rm -rf plots/eps/$tag
rm -rf plots/png/$tag
mkdir  plots/eps/$tag
mkdir  plots/png/$tag

#== Print and keep track of data/running time ==#

echo ''
date
start=`date +%s`

#=============== STEP 1 ===============#
#==== PRODUCE FAST ROTATION SIGNAL ====#
#=============== STEP 1 ===============#

#== Configuration parameters ==#

outputRootFile="root/FRS_${tag}.root"
     histoName="allCalosallBunches_intensitySpectrum"
   rebinFactor=149
            tS=0   # in mico-sec
            tM=145 # in mico-sec
  startFitTime=30  # in mico-sec
    endFitTime=400 # in mico-sec
     printPlot=1 # 1 to print plots, 0 not to
      saveROOT=1 # 1 to save results in ROOT file, 0 not to
      statFluc=0 # 1 to enable statistical fluctuations, 0 not to
     nFitParam=5 # either 5 or 9
    produceFRS=1 # 1 to produce Fast Rotation signal, 0 if already exist    


#== Run Python code to produce Fast Rotation signal ==#

python python/produceFastRotationSignal.py\
    $inputRootFile\
    $outputRootFile\
    $histoName\
    $rebinFactor\
    $tS\
    $tM\
    $startFitTime\
    $endFitTime\
    $printPlot\
    $saveROOT\
    $tag\
    $statFluc\
    $dataType\
    $nFitParam\
    $produceFRS\
    -b

#=============== STEP 2 ===============#
#============ OPTIMIZE T0 =============#
#=============== STEP 2 ===============#

#== Configuration parameters ==#

 inputRootFile="root/FRS_${tag}.root"
outputRootFile="root/${tag}_t0Opt.root"
outputTextFile="txt/${tag}_t0Opt.txt"
     histoName="fr" # name set in the code from previous step
       lowert0=-327 # lower T0 boundary
       uppert0=-325 # upper T0 boundary
    t0StepSize=0.25 # T0 step size
      optLevel=1 # 1 or 2 (1 is coarser and 2 is finer)
            tS=4
            tM=400
     printPlot=1 # 1 to print plots, 0 not to
      saveROOT=1 # 1 to save results in ROOT file, 0 not to
       runSine=1 # run the sine Fourier Transform alongside the Cosine

#== Run Python code to perform the T0 optimization ==#

python python/t0OptimizationMin.py\
    $inputRootFile $outputRootFile\
    $outputTextFile\
    $histoName\
    $lowert0\
    $uppert0\
    $t0StepSize\
    $optLevel\
    $tS\
    $tM\
    $printPlot\
    $saveROOT\
    $tag\
    $runSine\
    -b



#=============== STEP 3 ===============#
#======= RUN FOURIER ANALYSIS =========#
#=============== STEP 3 ===============#

while read -r line
do
    t0=$line
done < "$outputTextFile"

outputRootFile="root/${tag}_fourierAnalysis.root"
outputTextFile="txt/${tag}_fourierAnalysis_tS.txt"
outputDistFile="txt/${tag}_radialDistribution.txt"
    fieldIndex=0.108 #0.1185
     printPlot=1
updateTextFile=0
       runSine=0

python python/runFourierAnalysis.py\
    $inputRootFile\
    $outputRootFile\
    $outputTextFile\
    $histoName\
    $t0\
    $tS\
    $tM\
    $fieldIndex\
    $printPlot\
    $saveROOT\
    $tag\
    $updateTextFile\
    $runSine\
    $outputDistFile\
    $dataType\
    $truthFile\
    -b

echo ""
date

end=`date +%s`
runtime=$((end-start))

echo ""
echo " ---> TIME ELAPSED: $runtime second(s)"
echo ""
