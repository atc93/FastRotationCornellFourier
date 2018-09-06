#!/bin/bash

inputRootFile="root/FastRotation_60h.root"
outputRootFile="root/FRS_60h_tM_scan.root"
histoName="FastRotation/allCalosallBunches_intensitySpectrum"
tag="60h_allCalos_allBunches_tM_scan"
rebinFactor=150
tS=4   # in mico-sec
tM=500 # in mico-sec
startFitTime=30  # in mico-sec
endFitTime=500  # in mico-sec
printPlot=0
saveROOT=1
statFluc=0

rm -rf plots/eps/$tag
rm -rf plots/png/$tag
mkdir plots/eps/$tag
mkdir plots/png/$tag

python python/Data_produceFastRotationSignal.py $inputRootFile $outputRootFile $histoName $rebinFactor $tS $tM $startFitTime $endFitTime $printPlot $saveROOT $tag $statFluc -b

for itM in {0..490}; do

    echo ''
    date

    start=`date +%s`

    inputRootFile="root/FRS_60h_tM_scan.root"
    outputRootFile="root/60h_t0Opt_tM_scan.root"
    outputTextFile="txt/60h_t0Opt_tM_scan.txt"
    histoName="fr"
    lowert0=-335
    uppert0=-320
    t0StepSize=5
    optLevel=2 # 1, 2 3 or 4 (1 is coarser and 4 is finer)
    tS=4
    tM=$(echo "10+$itM*1" | bc)
    printPlot=0
    saveROOT=1
    runSine=0

    python python/Data_t0Optimization.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag $runSine -b

    while read -r line
    do
        t0=$line
    done < "$outputTextFile"

    outputRootFile="root/60h_tM_scan.root"
    outputTextFile="txt/60h_tM_scan.txt"
    fieldIndex=0.108
    printPlot=0
    updateTextFile=1
    runSine=0

    python python/Data_fourierAnalysis.py  $inputRootFile $outputRootFile $outputTextFile $histoName $t0 $tS $tM $fieldIndex $printPlot $saveROOT $tag $updateTextFile $runSine -b

    echo ""
    date

end=`date +%s`

runtime=$((end-start))

echo ""
echo " ---> TIME ELAPSED: $runtime second(s)"
echo ""

done
