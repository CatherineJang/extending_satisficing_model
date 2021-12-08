from Gaussian import Gaussian, GaussGroup
import model
import math
import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns; sns.set_theme()
from joblib import Parallel, delayed

# Set default ranges
defaultSigmaHRange = [x/20.0 for x in range(1, 41, 1)]
defaultrfRange = [x/10.0 for x in range(10, 25, 1)]

theme = sns.diverging_palette(260, 20, s=100, as_cmap=True)

def main():
  for i, DF in enumerate(makeDFs()):
    sns.heatmap(DF, center=0, cmap=theme)
    plt.xlabel("rationalization factor")
    plt.ylabel("sigma_h")
    plt.savefig('figs/Heatmaps/{}-iter-Heat.png'.format(i+2))
    plt.clf()

def makeDFs(sigmaHRange=defaultSigmaHRange, rfRange=defaultrfRange, iterations=5, P=True):
  allPartyMeanShiftsAllIter = [[[] for x in sigmaHRange] for y in range(iterations-1)]
  for i in range(len(sigmaHRange)):
    print(i)
    if P:
      #something
      partyMeans2D = Parallel(n_jobs=-1)(delayed(model.runModel)(sigmaHRange[i], j, iterations=iterations) for j in rfRange)
      for partyMeans in partyMeans2D:
        for iterCount in range(1, iterations):
          partyMeanShift = partyMeans[iterCount] - partyMeans[0]
          allPartyMeanShiftsAllIter[iterCount-1][i].append(partyMeanShift)
    else:
      for j in rfRange:
        partyMeans = model.runModel(sigmaHRange[i], j, iterations=iterations)
        for iterCount in range(1, iterations):
          partyMeanShift = partyMeans[iterCount] - partyMeans[0]
          allPartyMeanShiftsAllIter[iterCount-1][i].append(partyMeanShift)
  
  # Make pandas DF for plot
  colLabels = list(map(str, rfRange))
  rowLabels = list(map(str, sigmaHRange))
  for allPartyMeanShifts in allPartyMeanShiftsAllIter:
    meanShiftsDF = pd.DataFrame(allPartyMeanShifts, columns=colLabels, index=rowLabels)
    yield meanShiftsDF

main()