for i in {1..24}; do
    textFile=txt/60h_fourierAnalysis_calo$i.txt
    while read -r line
    do
        echo calo$i $line >> txt/60h_fourierAnalysis_perCalo.txt
    done < "$textFile"
done
