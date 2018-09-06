# 16 5
for i in {0..16}; do    
    eth=$(echo "1000+$i*50" | bc); 
    for j in {0..5}; do
        dt=$(echo "6.205+$j*0.005" | bc);
        root -l -b -q "rootMacro/makeIntensityPlots.C($eth, $dt)"
    done
done
