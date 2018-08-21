#!/bin/bash

inputRootFile="root/FRS_60h_allCalos.root"
outputRootFile="root/60h_t0Opt_allCalos.root"
outputTextFile="txt/60h_t0Opt_allCalos.txt"
histoName="fr"
lowert0=-340
uppert0=-310
t0StepSize=2
optLevel=4
tS=4
tM=400
printPlot=0
saveROOT=1
tag="60h_allCalos"

python python/Data_t0Optimization.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag -b

while read -r line
do
    t0=$line
done < "$outputTextFile"

outputRootFile="root/60h_fourierAnalysis_allCalos.root"
outputTextFile="txt/60h_fourierAnalysis_allCalos.txt"
fieldIndex=0.108
printPlot=1

python python/Data_fourierAnalysis.py  $inputRootFile $outputRootFile $outputTextFile $histoName $t0 $tS $tM $fieldIndex $printPlot $saveROOT $tag -b
