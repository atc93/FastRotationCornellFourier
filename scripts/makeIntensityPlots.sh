for i in {0..0}; do    
    eth=$(echo "1500+$i*50" | bc); 
    for j in {0..0}; do
        dt=$(echo "6.220+$j*0.005" | bc);
        root -l -b -q "rootMacro/makeIntensityPlots.C($eth, $dt)"
    done
done
