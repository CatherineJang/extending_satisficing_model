import seaborn as sns; sns.set_theme()
import matplotlib.pyplot as plt
import argparse
import pandas as pd

from model import runModel

from matplotlib.colors import LogNorm, Normalize
from matplotlib.ticker import MaxNLocator

fineHeatMap = False
if fineHeatMap:
  defaultSigmaHRange = [x/20.0 for x in range(1, 61, 1)]
  defaultrfRange = [x/20.0 for x in range(21, 100, 1)]
else:
  defaultSigmaHRange = [x/20.0 for x in range(1, 41, 4)]
  defaultrfRange = [x/10.0 for x in range(11, 25, 4)]

def main(args):
  DF = makeDFs(args.numVoters, iterations=args.iterations)
  sns.heatmap(DF, cmap="YlGnBu", norm=LogNorm(), cbar_kws={'ticks': [5,10,20,40,60,80,100], 'format':'%.i'})
  plt.xlabel("rationalization factor")
  plt.ylabel("sigma_h")
  plt.savefig('../figs/simulation-figs/Heatmaps/{}-{}-iter-Heat.png'.format(args.numVoters, args.iterations))
  plt.clf()

def makeDFs(numVoters, sigmaHRange=defaultSigmaHRange, rfRange=defaultrfRange, iterations=3):
  numIterToConverge = [[runModel(x, y, numVoters, iterations=iterations, convergence=True) for y in rfRange] for x in sigmaHRange]
  
  # Make pandas DF for plot
  colLabels = list(map(str, rfRange))
  rowLabels = list(map(str, sigmaHRange))
  return pd.DataFrame(numIterToConverge, columns=colLabels, index=rowLabels)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("iterations", help="Number of iterations per simulation.", type=int)
    parser.add_argument("numVoters", help="Number of agents to initialize.", type=int)
    parser.add_argument("--toMean", "-m", help="Parties go to their voter bases mean instead of vote maximizing ideology.", action="store_true")
    args = parser.parse_args()
    main(args)