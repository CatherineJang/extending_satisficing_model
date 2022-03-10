import seaborn as sns; sns.set_theme()
import matplotlib.pyplot as plt
import argparse
import pandas as pd

from model import runModel

from matplotlib.colors import LogNorm

fineHeatMap = True
if fineHeatMap:
  defaultSigmaHRange = [x/20.0 for x in range(1, 41, 1)]
  defaultrfRange = [x/20.0 for x in range(21, 81, 1)]
else:
  defaultSigmaHRange = [x/20.0 for x in range(1, 41, 4)]
  defaultrfRange = [x/10.0 for x in range(11, 25, 4)]

def main(args):
  if args.loadFile == None:
    DF = makeDFs(args.numVoters, iterations=args.iterations, toMean=args.toMean)

    filePath = '../figs/simulation-figs/Heatmaps/{}{}-{}-iter-Heat'.format('m-' if args.toMean else '', args.numVoters, args.iterations)

    # save and read back in data
    DF.to_csv(filePath+'.csv')
  else:
    filePath = '../figs/simulation-figs/Heatmaps/' + args.loadFile
  DFLoad = pd.read_csv(filePath+'.csv', header=0, index_col=0)

  sns.heatmap(DFLoad, cmap="YlGnBu", norm=LogNorm(), cbar_kws={'ticks': [6,8,10,20,30,40,60,80,100,200,300,400,600,800,1000], 'format':'%.i'})
  plt.xlabel("Rationalization Factor")
  plt.ylabel("Sigma Hat")
  plt.title('Model Iterations Until Convergence')

  ax = plt.gca()
  ax.invert_yaxis()
  plt.tight_layout()
  plt.savefig(filePath+'.png')
  plt.clf()

def makeDFs(numVoters, sigmaHRange=defaultSigmaHRange, rfRange=defaultrfRange, iterations=3, toMean=False):
  numIterToConverge = [[runModel(x, y, numVoters, iterations=iterations, convergence=True, toMean=toMean) for y in rfRange] for x in sigmaHRange]
  
  # Make pandas DF for plot
  colLabels = list(map(str, rfRange))
  rowLabels = list(map(str, sigmaHRange))
  return pd.DataFrame(numIterToConverge, columns=colLabels, index=rowLabels)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("iterations", help="Number of iterations per simulation.", type=int)
    parser.add_argument("numVoters", help="Number of agents to initialize.", type=int)
    parser.add_argument("--loadFile", help="If given load data from csv file, otherwise run model. Give as just filename in the Heatmaps directory, w/o '.csv'")
    parser.add_argument("--toMean", "-m", help="Parties go to their voter bases mean instead of vote maximizing ideology.", action="store_true")
    args = parser.parse_args()
    main(args)