while [ 0==0 ]; do pid=$(pidof python); echo $pid; sudo renice -n -20 $pid; sleep 5; done
