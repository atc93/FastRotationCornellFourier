#!/bin/bash

tag="TMC_tGaus_pGaus_0to400mus_freqDist"
inputRootFile="root/TMC_tGaus_pGaus_0to400mus_freqDist.root"
outputRootFile="root/FRS_${tag}_tS_scan.root"
#histoName="FastRotation/allCalosallBunches_intensitySpectrum"
histoName="h_frs"
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

#python python/Data_produceFastRotationSignal.py $inputRootFile $outputRootFile $histoName $rebinFactor $tS $tM $startFitTime $endFitTime $printPlot $saveROOT $tag $statFluc -b

for itS in {0..1400}; do

    echo ''
    date

    start=`date +%s`

    #inputRootFile="root/FRS_${tag}_tS_scan.root"
    inputRootFile="root/TMC_tGaus_pGaus_0to400mus_freqDist.root"
    outputRootFile="root/${tag}_t0Opt_tS_scan.root"
    outputTextFile="txt/${tag}_t0Opt_tS_scan.txt"
    histoName="h_frs"
    lowert0=105
    uppert0=115
    t0StepSize=2
    optLevel=2 # 1, 2 3 or 4 (1 is coarser and 4 is finer)
    tM=400
    tS=$(echo "0+$itS*0.005" | bc)
    printPlot=0
    saveROOT=1
    runSine=0

    python python/Data_t0Optimization.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag $runSine -b

    while read -r line
    do
        t0=$line
    done < "$outputTextFile"

    outputRootFile="root/${tag}_tS_scan.root"
    outputTextFile="txt/${tag}_tS_scan.txt"
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
