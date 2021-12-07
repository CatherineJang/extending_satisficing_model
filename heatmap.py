from Gaussian import Gaussian, GaussGroup
import model
import math
import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns; sns.set_theme()

# Set default ranges
defaultSigmaHRange = [x/10.0 for x in range(1, 21, 1)]
defaultrfRange = [x/10.0 for x in range(10, 26, 1)]

def main():
  DF = makeDF()
  sns.heatmap(DF)
  plt.xlabel("rationalization factor")
  plt.ylabel("sigma_h")
  plt.show()

def makeDF(sigmaHRange=defaultSigmaHRange, rfRange=defaultrfRange, iterations=3):
  allPartyMeanShifts = [[] for x in sigmaHRange]
  for i in range(len(sigmaHRange)):
    for j in rfRange:
      partyMeans = model.runModel(sigmaHRange[i], j, iterations=iterations)
      partyMeanShift = abs(partyMeans[0] - partyMeans[-1])
      allPartyMeanShifts[i].append(partyMeanShift)
  
  # Make pandas DF for plot
  colLabels = list(map(str, rfRange))
  rowLabels = list(map(str, sigmaHRange))
  meanShiftsDF = pd.DataFrame(allPartyMeanShifts, columns=colLabels, index=rowLabels)

  return meanShiftsDF

main()