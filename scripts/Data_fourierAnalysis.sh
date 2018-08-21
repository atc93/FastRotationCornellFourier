inputRootFile="root/frs_9d.root"
outputRootFile="root/result_9d.root"
outputTextFile="txt/frs_9d.txt"
histoName="fr"
t0=-0.31932
tS=4
tM=400
fieldIndex=0.12
printPlot=1
saveROOT=1
tag="9d"


python python/Data_fourierAnalysis.py  $inputRootFile $outputRootFile $outputTextFile $histoName $t0 $tS $tM $fieldIndex $printPlot $saveROOT $tag -b
