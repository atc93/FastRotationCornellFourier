t0=0
tS=4
tm=400
n=0.12
textfile="txt/frs_9d.txt"
rootfile="root/frs_9d.root"

rm -f $textfile
./renice.sh >& log/renice.log &

for itm in {0..0}; do
    tm=$(echo "400+$itm*100" | bc)
    for itS in {0..0}; do
        tS=$(echo "4+$itS*0.025" | bc)
        for it0 in {0..0}; do
            t0=$(echo "-0.31935+$it0*0.0001" | bc)
            echo $t0, $tS, $tm
            python python/Data_fourierAnalysis.py $t0 $tS $tm $n $textfile $rootfile -b
        done
    done
done
