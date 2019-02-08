#!/bin/bash

inputFile=$2

for i in {1..24}; do

           tag=$1
 inputRootFile="$inputFile"
outputRootFile="root/FRS_${tag}_calo$i.root"
     histoName="calo${i}_intensitySpectrum"
   rebinFactor=100
           tag="${tag}_calo$i"
            tS=4   # in mico-sec
            tM=400 # in mico-sec
  startFitTime=30  # in mico-sec
    endFitTime=400  # in mico-sec
     printPlot=1
      saveROOT=1
      statFluc=0


rm -rf plots/eps/$tag
rm -rf plots/png/$tag
mkdir plots/eps/$tag
mkdir plots/png/$tag

python python/Data_produceFastRotationSignal.py $inputRootFile $outputRootFile $histoName $rebinFactor $tS $tM $startFitTime $endFitTime $printPlot $saveROOT $tag $statFluc -b

 inputRootFile="root/FRS_${tag}.root"
outputRootFile="root/${tag}_t0Opt.root"
outputTextFile="txt/${tag}_t0Opt.txt"
     histoName="fr"
     lowert0=$(echo "-320 + $i*6.225-6.225" | bc)
     uppert0=$(echo "-316 + $i*6.225-6.225" | bc)
     #lowert0=$( expr -319 + "$i" '*' 6 - 6 )
     #uppert0=$( expr -317 + "$i" '*' 6 - 6 )     
    t0StepSize=0.05
      optLevel=2 #4
            tS=$(echo "4.03 + $i*0.006225" | bc)
            tM=400
     printPlot=1
      saveROOT=1
       runSine=0

python python/t0OptimizationMin.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag $runSine -b

while read -r line
do
    t0=$line
done < "$outputTextFile"

outputRootFile="root/${tag}_fourierAnalysis.root"
outputTextFile="txt/${tag}_fourierAnalysis.txt"
    fieldIndex=0.108
     printPlot=1
updateTextFile=0     
       runSine=0

python python/Data_fourierAnalysis.py  $inputRootFile $outputRootFile $outputTextFile $histoName $t0 $tS $tM $fieldIndex $printPlot $saveROOT $tag $updateTextFile $runSine "test.txt" "data" "none" -b

done

tag=$1

./scripts/mergeCaloResults.sh $tag
