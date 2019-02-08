# For all the styling

def plot( c, h, name, lower, upper ):
    h.GetXaxis().SetRangeUser( lower, upper );
    h.Draw("hist");
    c.Draw()
    printName = 'plots/eps/' + name + '_{0}us_{1}us.eps'.format(lower, upper)
    c.Print( printName )
    printName = 'plots/png/' + name + '_{0}us_{1}us.png'.format(lower, upper)
    c.Print( printName )

