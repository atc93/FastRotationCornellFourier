#!/bin/bash

for i in {1..24}; do

    tag=$1
    tag="${tag}_calo$i"

    for j in {0..50}; do

        echo ""
        date

        start=`date +%s`

        inputRootFile=$2
        outputRootFile="root/FRS_${tag}.root"
        histoName="calo${i}_intensitySpectrum"
        rebinFactor=149
        tS=4   # in mico-sec
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
        outputTextFile="txt/${tag}_calo$i.txt"
        histoName="fr"
        lowert0=$(bc <<< -318.5+$i*6.227-6.227)
        uppert0=$(bc <<< -317.5+$i*6.227-6.227)
        t0StepSize=0.2
        optLevel=0
        tS=4
        tM=400
        printPlot=0
        saveROOT=1
        runSine=0

        python python/t0OptimizationMin.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag $runSine -b

        while read -r line
        do
            t0=$line
        done < "$outputTextFile"

        outputRootFile="root/${tag}_fourierAnalysis_calo$i.root"
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

done
