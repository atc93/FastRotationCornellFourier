#!/bin/bash

inputRootFile="root/FRS_60h_calo$1.root"
outputRootFile="root/60h_t0Opt_calo$1.root"
outputTextFile="txt/60h_t0Opt_calo$1.txt"
histoName="fr"
lowert0=$( expr -340 + "$1" '*' 6 - 6 )
uppert0=$( expr -310 + "$1" '*' 6 - 6 )
t0StepSize=2
optLevel=4
tS=4
tM=400
printPlot=0
saveROOT=1
tag="60h_calo$1"

python python/Data_t0Optimization.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag -b

while read -r line
do
    t0=$line
done < "$outputTextFile"

outputRootFile="root/60h_fourierAnalysis_calo$1.root"
outputTextFile="txt/60h_fourierAnalysis_calo$1.txt"
fieldIndex=0.108
printPlot=1

python python/Data_fourierAnalysis.py  $inputRootFile $outputRootFile $outputTextFile $histoName $t0 $tS $tM $fieldIndex $printPlot $saveROOT $tag -b
