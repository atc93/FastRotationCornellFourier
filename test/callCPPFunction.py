import ROOT as r

r.gROOT.ProcessLine('.L cppFunction.C+')

print(r.cppFunction(9))
