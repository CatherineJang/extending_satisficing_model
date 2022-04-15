from model import runModel
import argparse
from matplotlib.colors import LinearSegmentedColormap
from xmlrpc.client import boolean
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

fineHeatMap = False
if fineHeatMap:
  defaultSigmaHRange = [x/20.0 for x in range(1, 61, 1)]
  defaultrfRange = [x/20.0 for x in range(21, 100, 1)]
else:
  defaultSigmaHRange = [x/20.0 for x in range(1, 41, 4)]
  defaultrfRange = [x/10.0 for x in range(11, 25, 4)]

def main(args):
  stateAtConvergence(args.numVoters, args.sigmaHRange, args.rfRange, args.iterations)

def stateAtConvergence(numVoters=10000, sigmaHRange=defaultSigmaHRange, rfRange=defaultrfRange, iterations=100):
  (convDF, zeroDF, depoDF) = makeDFs(numVoters, sigmaHRange, rfRange, iterations)

  # Assign discrete vals to end states:
  #   1 --> converged but not zero
  #   2 --> zero but not converged
  #   3 --> depolarized (zero and converged)
  #   4 --> neither converged nor zero

  convNotDepoDF = (convDF & ~depoDF)*2
  zeroNotDepoDF = (zeroDF & ~depoDF)*3
  depoDF = depoDF*4
  noneDF = (~convDF & ~zeroDF)*1

  heatmapDF = convNotDepoDF + zeroNotDepoDF +  depoDF + noneDF

  myColors = ((0.3, 0.0, 0.0, 1.0), (0.8, 0.0, 0.0, 1.0), (0.0, 0.8, 0.0, 1.0), (0.0, 0.0, 0.8, 1.0))
  cmap = LinearSegmentedColormap.from_list('Custom', myColors, len(myColors))

  ax = sns.heatmap(heatmapDF, cmap=cmap, linewidths=.5, linecolor='lightgray')

  # Manually specify colorbar labelling after it's been generated
  colorbar = ax.collections[0].colorbar
  colorbar.set_ticks([1.375, 2.125, 2.875, 3.625])
  colorbar.set_ticklabels(['neither zero nor converged', 'converged, not zero', 'zero, not converged', 'depolarized'])

  # X - Y axis labels
  ax.set_ylabel("sigma_h")
  ax.set_xlabel("rationalization factor")

  # Only y-axis labels need their rotation set, x-axis labels already have a rotation of 0
  _, labels = plt.yticks()
  plt.setp(labels, rotation=0)

  plt.show()
  return heatmapDF

def makeDFs(numVoters, sigmaHRange, rfRange, iterations) -> tuple:
  # Record time series data, final party mean for each param combination
  modelOut = [[runModel(x, y, numVoters, iterations=iterations, convergence=False) for y in rfRange] for x in sigmaHRange]
  finalStates = [[modelOut[x][y][-1] for y in range(len(rfRange))] for x in range(len(sigmaHRange))]

  # Determine conv, zero, depo states
  isConverged1D = [isConverged(x, windowSize = iterations//10) for sublist in modelOut for x in sublist]
  isZero1D= [x < 0.04 for sublist in finalStates for x in sublist]
  isDepolarized1D = [isConverged1D[i] == True and isZero1D[i] == True for i in range(len(isConverged1D))]

  # Make pandas DF for plot
  colLabels = list(map(str, rfRange))
  rowLabels = list(map(str, sigmaHRange))

  numRows = len(sigmaHRange)
  numCols = len(rfRange)

  convDF = pd.DataFrame(np.reshape(isConverged1D, (numRows, numCols)), columns=colLabels, index=rowLabels)
  zeroDF = pd.DataFrame(np.reshape(isZero1D, (numRows, numCols)), columns=colLabels, index=rowLabels)
  depoDF = pd.DataFrame(np.reshape(isDepolarized1D, (numRows, numCols)), columns=colLabels, index=rowLabels)

  return (convDF, zeroDF, depoDF)

def isConverged(partyMeans, RMSEthreshold = 0.5, windowSize = 1) -> bool:
  """Runs window RMS calculation on 1D list"""
  partyMeansSq = np.power(partyMeans, 2)
  window = np.ones(windowSize)/float(windowSize)
  windowRMSEs = np.sqrt(np.convolve(partyMeansSq, window, 'valid'))
  return any(x <= RMSEthreshold for x in windowRMSEs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("iterations", nargs='?', default = 100, help="Number of iterations per simulation.", type=int)
    parser.add_argument("numVoters", nargs='?', default = 100, help="Number of agents to initialize.", type=int)
    parser.add_argument("sigmaHRange", nargs='?', default = defaultSigmaHRange, help="List of sigmaH values to simulate.", type=list)
    parser.add_argument("rfRange",nargs='?', default = defaultrfRange, help="List of rationalization values to simulate.", type=list)
    args = parser.parse_args()
    main(args)