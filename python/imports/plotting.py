#==============================================#
#== IMPORT FILE CONTAINING PLOTTING FUCNTION ==#
#==============================================#

#== To plot/print a histogram/canvas ==#
def plot( c, h, name, lower, upper ):
    h.GetXaxis().SetRangeUser( lower, upper );
    h.Draw("hist");
    c.Draw()
    printName = 'plots/eps/' + name + '_{0}us_{1}us.eps'.format(lower, upper)
    c.Print( printName )
    printName = 'plots/png/' + name + '_{0}us_{1}us.png'.format(lower, upper)
    c.Print( printName )

#== Function to plot multiples objects on the same Canvas ==#
def plotMultipleObjects( opt, objectList ):
    cpt = 0
    for obj in objectList:
        if ( cpt == 0 ):
            obj.Draw( opt )
        else:
            obj.Draw("same")
        cpt += 1
