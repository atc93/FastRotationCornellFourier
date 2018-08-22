#!/bin/bash

for i in {0..7}; do

 inputRootFile="root/FastRotation_60h.root"
outputRootFile="root/FRS_60h_bunch$i.root"
     histoName="FastRotation/allCalosBunch${i}_intensitySpectrum"
           tag="60h_bunch$i"
   rebinFactor=100
            tS=4   # in mico-sec
            tM=500 # in mico-sec
  startFitTime=30  # in mico-sec
    endFitTime=500  # in mico-sec
     printPlot=1
      saveROOT=1
      statFluc=0

rm -rf plots/eps/$tag
rm -rf plots/png/$tag
mkdir plots/eps/$tag
mkdir plots/png/$tag

python python/Data_produceFastRotationSignal.py $inputRootFile $outputRootFile $histoName $rebinFactor $tS $tM $startFitTime $endFitTime $printPlot $saveROOT $tag $statFluc -b

 inputRootFile="root/FRS_60h_bunch$i.root"
outputRootFile="root/60h_t0Opt_bunch$i.root"
outputTextFile="txt/60h_t0Opt_bunch$i.txt"
     histoName="fr"
       lowert0=-340
       uppert0=-310
    t0StepSize=2
      optLevel=4
            tS=4
            tM=400
     printPlot=0
      saveROOT=1

python python/Data_t0Optimization.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag -b

while read -r line
do
    t0=$line
done < "$outputTextFile"

outputRootFile="root/60h_fourierAnalysis_bunch$i.root"
outputTextFile="txt/60h_fourierAnalysis_bunch$i.txt"
    fieldIndex=0.108
     printPlot=1

python python/Data_fourierAnalysis.py  $inputRootFile $outputRootFile $outputTextFile $histoName $t0 $tS $tM $fieldIndex $printPlot $saveROOT $tag -b

done
