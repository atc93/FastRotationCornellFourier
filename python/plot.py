# For all the styling

from importAll import *

def plot( c, h, name, lower, upper ):
    h.GetXaxis().SetRangeUser( lower, upper );
    h.Draw();
    c.Draw()
    printName = 'plots/eps/' + name + '_{0}us_{1}us.eps'.format(lower, upper)
    c.Print( printName )
    printName = 'plots/png/' + name + '_{0}us_{1}us.png'.format(lower, upper)
    c.Print( printName )

