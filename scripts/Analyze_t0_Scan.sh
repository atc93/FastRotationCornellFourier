#!/bin/bash

tag=$1
inputRootFile=$2
dataType=$3


for itS in {0..30}; do

    t0=$(echo ".1015+$itS*0.00005" | bc)    

    echo ''
    date

    start=`date +%s`

    outputRootFile="root/FRS_${tag}.root"
    histoName="allCalosallBunches_intensitySpectrum"
    rebinFactor=149
    tS=4.02
    tM=400 # in mico-sec
    startFitTime=30  # in mico-sec
    endFitTime=400  # in mico-sec
    printPlot=1
    saveROOT=1
    statFluc=0

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

    python python/Data_produceFastRotationSignal.py $inputRootFile $outputRootFile $histoName $rebinFactor $tS $tM $startFitTime $endFitTime $printPlot $saveROOT $tag $statFluc $dataType -b

    inputRootFile="root/FRS_${tag}.root"

    outputRootFile="root/${tag}_fourierAnalysis.root"
    outputTextFile="txt/${tag}_t0_scan.txt"
    fieldIndex=0 #0.1185
    printPlot=1
    updateTextFile=1
    runSine=0

    python python/Data_fourierAnalysis.py  $inputRootFile $outputRootFile $outputTextFile $histoName $t0 $tS $tM $fieldIndex $printPlot $saveROOT $tag $updateTextFile $runSine "test.txt" $dataType $truthFile -b

    echo ""
    date

end=`date +%s`

runtime=$((end-start))

echo ""
echo " ---> TIME ELAPSED: $runtime second(s)"
echo ""

done
