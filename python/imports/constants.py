#==============================================#
#== IMPORT FILE CONTAINING VARIOUS CONSTANTS ==#
#==============================================#

#== Physics constants ==#
speedOfLight = 299792458 #speed of light [m/s]

#== For plotting purposes ==#

##== Collimator frequency boundaries to draw line ==##
lowerCollimatorFreq = float(6662.799) # in kHz
upperCollimatorFreq = float(6747.651) # in kHz

##== Collimator frequency boundaries to print out text ==##
lowerCollimatorTextFreq1 = float(6650) # in kHz 
lowerCollimatorTextFreq2 = float(6674) # in kHz
upperCollimatorTextFreq1 = float(6737) # in kHz
upperCollimatorTextFreq2 = float(6759) # in kHz

##== Collimator radius boundaries to draw line ==##
lowerCollimatorRad = float(7112-45) # in mm
upperCollimatorRad = float(7112+45) # in mm

#== For analysis purposes ==#

##== Frequency range uses in analysis ==##
lowerFreq = float(6630) # in kHz
upperFreq = float(6780) # in kHz

##== Frequency step uses in analysis ==##
freqStep  = float(2)    # in kHz

##== Number of frequency steps uses in analysis ==##
nFreq = int( ( upperFreq - lowerFreq ) / freqStep )
