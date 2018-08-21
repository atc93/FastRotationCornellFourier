#! /bin/bash

     inputRootFile="root/FastRotation_60h.root"
    outputRootFile="root/FRS_60h_calo$1.root"
         histoName="FastRotation/calo$1_intensitySpectrum"
               tag="60h_calo$1"
       rebinFactor=100
                tS=4   # in mico-sec
                tM=500 # in mico-sec
      startFitTime=30  # in mico-sec
        endFitTime=500  # in mico-sec
         printPlot=1
          saveROOT=1

python python/Data_produceFastRotationSignal.py $inputRootFile $outputRootFile $histoName $rebinFactor $tS $tM $startFitTime $endFitTime $printPlot $saveROOT $tag -b
