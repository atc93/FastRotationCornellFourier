#!/bin/bash

          tag=$1
inputRootFile=$2
     dataType=$3

echo ''
date

start=`date +%s`

outputRootFile="root/FRS_${tag}.root"
     histoName="allCalosallBunches_intensitySpectrum"
   rebinFactor=149
            tS=0   # in mico-sec
            tM=145 # in mico-sec
  startFitTime=30  # in mico-sec
    endFitTime=400  # in mico-sec
     printPlot=1
      saveROOT=1
      statFluc=0
     nFitParam=9
    produceFRS=0     

if [ "$dataType" == "data" ]; then
    histoName="allCalosallBunches_intensitySpectrum"
else
    histoName="fr"
    truthFile=$2
fi

rm -rf plots/eps/$tag
rm -rf plots/png/$tag
mkdir plots/eps/$tag
mkdir plots/png/$tag

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

 inputRootFile="root/FRS_${tag}.root"
outputRootFile="root/${tag}_t0Opt.root"
outputTextFile="txt/${tag}_t0Opt.txt"
     histoName="fr"
       lowert0=-318.3
       uppert0=-317.9
    t0StepSize=0.1
      optLevel=2 # 1 or 2 (1 is coarser and 2 is finer)
            tS=0
            tM=145
     printPlot=1
      saveROOT=1
       runSine=0

#python python/t0OptimizationMin.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag $runSine -b

while read -r line
do
    t0=$line
done < "$outputTextFile"

outputRootFile="root/${tag}_fourierAnalysis.root"
outputTextFile="txt/{tag}_fourierAnalysis_tS.txt"
    fieldIndex=0.108 #0.1185
     printPlot=1
updateTextFile=1
       runSine=0

#python python/Data_fourierAnalysis.py  $inputRootFile $outputRootFile $outputTextFile $histoName $t0 $tS $tM $fieldIndex $printPlot $saveROOT $tag $updateTextFile $runSine "test.txt" $dataType $truthFile -b

echo ""
date

end=`date +%s`

runtime=$((end-start))

echo ""
echo " ---> TIME ELAPSED: $runtime second(s)"
echo ""
