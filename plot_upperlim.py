import matplotlib.pyplot as plt
import mplhep as hep
from matplotlib import rc



plt.style.use(hep.style.ROOT)
plt.rcParams["figure.figsize"] = (8,8)
plt.xlim(10,1000)
plt.ylim(0.00000000001, 10)

mass = [10,50,100,500,1000]
xsec_theo = [0.05199,0.03649,0.01757,0.001214,0.0002683] #7.504e-09,7.066e-10]

xsec_m2s = [2.768,0.939,0.199,0.0147,0.00996]
xsec_m1s = [3.612,1.236,0.262,0.0194,0.01324]
xsec_mean = [4.887,1.669,0.357,0.0269,0.01821]
xsec_p1s = [6.562,2.248,0.484,0.0371,0.02511]
xsec_p2s = [8.410,2.878,0.627,0.0489,0.03315]



plt.plot(mass,xsec_theo, label ="$\sigma$$_{theo}$", color ='red')
plt.plot(mass,xsec_mean, label = "Median Expected Limit", color='black')
plt.fill_between(mass, xsec_m2s, xsec_p2s, color='yellow', label = 'Expected $\pm$ 2$\sigma$')
plt.fill_between(mass, xsec_m1s, xsec_p1s, color='limegreen', label = 'Expected $\pm$ 1$\sigma$')
plt.yscale('log')
plt.rc('xtick',labelsize=10)
plt.rc('ytick',labelsize=10)
plt.title("$\sqrt{s}$ = 13 TeV, L = 150 fb$^{-1}$", loc='left',fontsize=15)
plt.xlabel("$M$$_{Y_{0}}$ [GeV]", fontsize=15)
plt.ylabel("Expected Cross Section [pb]", fontsize=15)
plt.minorticks_on()
plt.legend()
plt.savefig("testlimit")

