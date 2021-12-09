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

heatOf = "P-MEAN"
iterations = 5

theme = sns.diverging_palette(260, 20, s=100, as_cmap=True)
thirdsNames = ["EXTREME", "ESTABLISHMENT", "MODERATES"]

def main():
  for i, DF in enumerate(makeDFs(heatOf, iterations=iterations)):
    sns.heatmap(DF, center=0 if heatOf=="P-MEAN" else 0.33, cmap=theme, vmin=0.1 if heatOf=="THIRDS" else None, vmax=0.6 if heatOf=="THIRDS" else None)
    plt.xlabel("rationalization factor")
    plt.ylabel("sigma_h")
    plt.savefig('figs/Heatmaps/{}-{}-iter-Heat.png'.format(thirdsNames[i//iterations] if heatOf=="THIRDS" else heatOf, i%iterations+2))
    plt.clf()

def makeDFs(of, sigmaHRange=defaultSigmaHRange, rfRange=defaultrfRange, iterations=3, P=True):
  allPartyMeanShiftsAllIter = [[[] for x in sigmaHRange] for y in range(iterations-1)]

  extremeAllIter = [[[] for x in sigmaHRange] for y in range(iterations)]
  establishmentAllIter = [[[] for x in sigmaHRange] for y in range(iterations)]
  moderatesAllIter = [[[] for x in sigmaHRange] for y in range(iterations)]
  for i in range(len(sigmaHRange)):
    print(i)
    if P:
      #something
      results2D = Parallel(n_jobs=-1)(delayed(model.runModel)(sigmaHRange[i], j, iterations=iterations, retVal=of) for j in rfRange)
      if of=="P-MEAN":
        for partyMeans in results2D:
          for iterCount in range(1, iterations):
            partyMeanShift = partyMeans[iterCount] - partyMeans[0]
            allPartyMeanShiftsAllIter[iterCount-1][i].append(partyMeanShift)
      if of=="THIRDS":
        for results in results2D:
          for iterCount, result in enumerate(results):
            extremeAllIter[iterCount][i].append(result[0])
            establishmentAllIter[iterCount][i].append(result[1])
            moderatesAllIter[iterCount][i].append(result[2])
    else:
      for j in rfRange:
        partyMeans = model.runModel(sigmaHRange[i], j, iterations=iterations)
        for iterCount in range(1, iterations):
          partyMeanShift = partyMeans[iterCount] - partyMeans[0]
          allPartyMeanShiftsAllIter[iterCount-1][i].append(partyMeanShift)
  
  # Make pandas DF for plot
  colLabels = list(map(str, rfRange))
  rowLabels = list(map(str, sigmaHRange))
  if of=="P-MEAN":
    for allPartyMeanShifts in allPartyMeanShiftsAllIter:
      meanShiftsDF = pd.DataFrame(allPartyMeanShifts, columns=colLabels, index=rowLabels)
      yield meanShiftsDF
  if of=="THIRDS":
    for thirdAllIter in [extremeAllIter, establishmentAllIter, moderatesAllIter]:
      for third in thirdAllIter:
        thirdDF = pd.DataFrame(third, columns=colLabels, index=rowLabels)
        yield thirdDF

main()