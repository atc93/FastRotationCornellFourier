inputRootFile="root/frs_9d.root"
outputRootFile="root/result_9d.root"
outputTextFile="txt/frs_9d.txt"
histoName="fr"
lowert0=-330
uppert0=-310
t0StepSize=5
optLevel=1
tS=4
tM=400
printPlot=0
saveROOT=1
tag="9d"

python python/Data_t0Optimization.py  $inputRootFile $outputRootFile $outputTextFile $histoName $lowert0 $uppert0 $t0StepSize $optLevel $tS $tM $printPlot $saveROOT $tag -b
