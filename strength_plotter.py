from __future__ import division
import numpy as np 
import matplotlib.pyplot as plt 
import sys
import os
from utilities import *
import seaborn as sns
import matplotlib.ticker as ticker

Bn=6.534000 # MeV

sns.set()
# sns.set_context("paper")
sns.set_context("talk")
#sns.set(rc={'figure.figsize':(5.5,6.5)})
sns.set_style("ticks", { 'axes.grid': False})
plt.rcParams['legend.loc'] = 'best'

# Cross section factor for formula strength = xsec*factor/Egamma
xsec_factor = 8.68e-8

def readGSF(folder):

	# import fgteo.rsg to get the calibration
	folded1, cal, E_array, tmp = read_mama_2D(folder+"/fgteo.rsg")

	# Constants for energy binning
	if(cal["a0x"] != cal["a0y"] 
		or cal["a1x"] != cal["a1y"] 
		or cal["a2x"] != cal["a2y"]):
		raise ValueError("Calibration coefficients for the axes don't match")  

	a0 =  cal["a0x"]/1e3 # in MeV
	a1 = cal["a1x"]/1e3 # in MeV

	strengthfile = open(folder+'/strength.nrm', 'r')
	strengthlines = strengthfile.readlines()
	strengthfile.close()
	N = len(strengthlines)
	strength = np.zeros((N,3))
	for i in range(N):
		words = strengthlines[i].split()
		if i < int(N/2):
			strength[i,0] = a0 + i*a1 # Energy coordinate 
			strength[i,1] = float(words[0]) # Strength coordinate
		else:
			strength[i-int(N/2),2] = float(words[0]) # Strength uncertainty (this way due to horrible file format!)

	transextfile = open(folder+'/transext.nrm')
	transextlines = transextfile.readlines()
	transextfile.close()
	Next = len(transextlines)
	strengthext = np.zeros((Next, 2))
	for i in range(Next):
		transext_current = float(transextlines[i].split()[0])
		energy_current = a0 + i*a1 + 1e-8
		strengthext[i,:] = ( energy_current, transext_current/(2*np.pi*energy_current**3) )

	# comptonfile = open(folder+'/187Re_gamma_n.dat', 'r')
	# comptonlines = comptonfile.readlines()
	# comptonfile.close()
	# Ncompton = len(comptonlines)
	# comptonstrength = np.zeros((Ncompton,3))
	# for i in range(Ncompton):
	# 	words = comptonlines[i].split()
	# 	comptonstrength[i,0] = float(words[3])
	# 	comptonstrength[i,1] = float(words[0]) * xsec_factor / comptonstrength[i,0]
	# 	comptonstrength[i,2] = np.sqrt(float(words[1])**2 + float(words[2])**2) * xsec_factor / comptonstrength[i,0] # Energy, strength, uncertainty (sqrt(stat^2 + sys^2))

	return strength, strengthext

# Plotting:
fig, axes = plt.subplots(figsize=(10,9))

axes.tick_params("x", top="off")
axes.tick_params("y", right="off")
axes.yaxis.set_minor_locator(ticker.NullLocator())

folder = "orig"
strength, strengthext = readGSF(folder)
iBn = (np.abs(strengthext[:,0] - Bn)).argmin()
plt.plot(strengthext[0:iBn,0], strengthext[:iBn,1], ":", color='red', label='orig')
plt.errorbar(strength[:,0], strength[:,1], yerr=strength[:,2], label="orig", fmt='d', color='red')
# plt.errorbar(comptonstrength[:,0], comptonstrength[:,1], yerr=comptonstrength[:,2], label='Shizuma et.al. (2005)', fmt='.-', color='crimson')

fname = folder +"/gsfTable.dat"
Eg_ = strengthext[0:iBn,0]
E1 = strengthext[:iBn,1]
Eg = Eg_[Eg_>0]
E1 = E1[Eg_>0]
WriteRAINIERgsfTable(fname, Eg, E1)

folder = "reduce_rhoSn"
strength, strengthext = readGSF(folder)
plt.plot(strengthext[0:iBn,0], strengthext[:iBn,1], ":", color='blue', label='reduce_rho')
plt.errorbar(strength[:,0], strength[:,1], yerr=strength[:,2], label="reduce_rho", fmt='d', color='blue')

fname = folder +"/gsfTable.dat"
Eg_ = strengthext[0:iBn,0]
E1 = strengthext[:iBn,1]
Eg = Eg_[Eg_>0]
E1 = E1[Eg_>0]
WriteRAINIERgsfTable(fname, Eg, E1)


plt.xlim([0,15])
plt.ylim([1e-10,5e-6])
plt.yscale('log')
plt.xlabel(r'$\gamma$-ray energy $E_\gamma$ [MeV]')
plt.ylabel(r'$\gamma$-ray strength [MeV$^{-3}$]')
# plt.text(0, 1e-7, '$^{187}\mathrm{Re}$', fontsize=30)
plt.text(-1.5,1e-6, 'PRELIMINARY', alpha=0.1, fontsize=70, rotation=30)

fig.tight_layout()

handles, labels = axes.get_legend_handles_labels()
axes.legend(handles, labels, numpoints=1, fancybox=True, framealpha=0.5)

plt.savefig('strength_pyplot.png')

plt.show()


