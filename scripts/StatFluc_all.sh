#!/bin/bash

tag=$1
inputRootFile=$2

for i in {1..1}; do

echo ""
date

start=`date +%s`

outputRootFile="root/FRS_${tag}.root"
     histoName="allCalosallBunches_intensitySpectrum"
   rebinFactor=149
            tS=4.03   # in mico-sec
            tM=400 # in mico-sec
  startFitTime=30  # in mico-sec
    endFitTime=400  # in mico-sec
     printPlot=0
      saveROOT=1
      statFluc=1

rm -rf plots/eps/$tag
rm -rf plots/png/$tag
mkdir plots/eps/$tag
mkdir plots/png/$tag

python python/Data_produceFastRotationSignal.py $inputRootFile $outputRootFile $histoName $rebinFactor $tS $tM $startFitTime $endFitTime $printPlot $saveROOT $tag $statFluc -b

 inputRootFile="root/FRS_${tag}.root"
outputRootFile="root/${tag}_t0Opt.root"
outputTextFile="txt/${tag}_t0Opt.txt"
     histoName="fr"
       lowert0=-326.2
       uppert0=-325.9
    t0StepSize=0.05
      optLevel=1
            tS=4.03
            tM=400
     printPlot=0
      saveROOT=1
       runSine=0

python python/t0OptimizationMin.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag $runSine -b

while read -r line
do
    t0=$line
done < "$outputTextFile"

outputRootFile="root/${tag}_fourierAnalysis.root"
outputTextFile="txt/${tag}_fourierAnalysis_statFluc.txt"
outputDistribution="txt/${tag}_radialDist_statFluc.txt"
    fieldIndex=0.108
     printPlot=0
updateTextFile=1
       runSine=0

python python/Data_fourierAnalysis.py  $inputRootFile $outputRootFile $outputTextFile $histoName $t0 $tS $tM $fieldIndex $printPlot $saveROOT $tag $updateTextFile $runSine $outputDistribution "data" "none" -b

echo ""
date

end=`date +%s`

runtime=$((end-start))

echo ""
echo " ---> TIME ELAPSED: $runtime second(s)"
echo ""

done

tag="${tag}_statFluc"
python python/Data_plotStatFluc.py $outputTextFile $tag "txt/${tag}.txt"
