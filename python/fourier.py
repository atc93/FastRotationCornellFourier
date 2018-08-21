# For the fourier computation

from importAll import *

def calc_cosine_dist(t0, cosine, binContent, binCenter):
    for i in range(150):
        frequency   = 6.6305 + i*0.001
        integral    = binContent*np.cos(2*math.pi*frequency*(binCenter-t0))*0.001
        cosine.SetBinContent(i+1, (np.sum(integral)))

def calc_sine_dist(t0, sine, binContent, binCenter):
    for i in range(150):
        frequency   = 6.6305 + i*0.001
        integral    = binContent*np.sin(2*math.pi*frequency*(binCenter-t0))*0.001
        sine.SetBinContent(i+1, (np.sum(integral)))

def calc_parabola_dist(t0, tS, firstApprox, parabola):
    for i in range(150):
        frq = 6630.5 + i*1
        integral = 0
        for j in range(1, 150):
            if (firstApprox.GetBinCenter(j)-frq) != 0:
                integral += firstApprox.GetBinContent(j)*np.sin(2*math.pi*(frq-firstApprox.GetBinCenter(j))*(tS-t0)/1000)/(1000*(frq-firstApprox.GetBinCenter(j))  )
            else:
                integral += 2*math.pi*firstApprox.GetBinContent(j)*(tS-t0)/1000000
        parabola.SetBinContent(i+1,integral)

def minimization(parabola, cosine):

    x = []
    y = []

    for i in range(32):
        x.append(parabola.GetBinContent(i+1))
        y.append(cosine.GetBinContent(i+1))
        x.append(parabola.GetBinContent(150-i))
        y.append(cosine.GetBinContent(150-i))

    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y,rcond=None)[0]

    return m, c
