tag=$1

for i in {1..24}; do
    textFile="txt/${tag}_calo${i}_fourierAnalysis.txt"
    while read -r line
    do
        echo calo$i $line >> txt/${tag}_fourierAnalysis_perCalo.txt
    done < "$textFile"
done
