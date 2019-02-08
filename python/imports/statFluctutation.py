# To vary histogram content according to statistics

def SquareRootN(  h ):
    nBins = h.GetXaxis().GetNbins()
    for iBin in range ( 1, nBins+1 ):
        binContent = h.GetBinContent( iBin )
        fluc = math.sqrt( binContent )
        rand = randint(0, 1)
        if ( rand > 0.5 ):
            h.SetBinContent( iBin, binContent + fluc )
        else:
            h.SetBinContent( iBin, binContent - fluc )

    return h

def Poisson( h ):
    nBins = h.GetXaxis().GetNbins()
    for iBin in range ( 1, nBins+1 ):
        binContent = h.GetBinContent( iBin )
        fluc = math.sqrt( np.random.poisson( binContent ) )
        rand = randint(0, 1)
        if ( rand > 0.5 ):
            h.SetBinContent( iBin, binContent + fluc )
        else:
            h.SetBinContent( iBin, binContent - fluc )
    return h
