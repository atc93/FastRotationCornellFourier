#!/bin/bash

for i in {1..1}; do

    for j in {1..1000}; do

        echo ""
        date

        start=`date +%s`

        inputRootFile="root/FastRotation_60h.root"
        outputRootFile="root/FRS_60h_calo$i.root"
        histoName="FastRotation/calo${i}_intensitySpectrum"
        tag="60h_calo$i"
        rebinFactor=150
        tS=4   # in mico-sec
        tM=500 # in mico-sec
        startFitTime=30  # in mico-sec
        endFitTime=500  # in mico-sec
        printPlot=0
        saveROOT=1
        statFluc=1

        rm -rf plots/eps/$tag
        rm -rf plots/png/$tag
        mkdir plots/eps/$tag
        mkdir plots/png/$tag

        python python/Data_produceFastRotationSignal.py $inputRootFile $outputRootFile $histoName $rebinFactor $tS $tM $startFitTime $endFitTime $printPlot $saveROOT $tag $statFluc -b

        inputRootFile="root/FRS_60h_calo$i.root"
        outputRootFile="root/60h_t0Opt_calo$i.root"
        outputTextFile="txt/60h_t0Opt_calo$i.txt"
        histoName="fr"
        lowert0=$(bc <<< -328+$i*6.225-6.225)
        uppert0=$(bc <<< -325+$i*6.225-6.225)
        t0StepSize=0.5
        optLevel=2
        tS=4
        tM=400
        printPlot=0
        saveROOT=1
        runSine=0

        python python/Data_t0Optimization.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag $runSine -b

        while read -r line
        do
            t0=$line
        done < "$outputTextFile"

        outputRootFile="root/60h_fourierAnalysis_calo$i.root"
        outputTextFile="txt/60h_fourierAnalysis_statFluc_calo$i.txt"
        outputDistribution="txt/60h_radialDist_statFluc_calo$i.txt"
        fieldIndex=0.108
        printPlot=0
        updateTextFile=1
        runSine=0

        python python/Data_fourierAnalysis.py  $inputRootFile $outputRootFile $outputTextFile $histoName $t0 $tS $tM $fieldIndex $printPlot $saveROOT $tag $updateTextFile $runSine $outputDistribution -b

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
