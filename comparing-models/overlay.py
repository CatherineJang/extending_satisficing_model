import sys
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt


sys.path.insert(1, '/Users/ericthompson-martin/Desktop/SP2022/polarization-project/extending_satisficing_model/simulated-agent-model')
# print(sys.path)
from model import runModel as runAgentModel

sys.path.remove('/Users/ericthompson-martin/Desktop/SP2022/polarization-project/extending_satisficing_model/simulated-agent-model')
# print(sys.path)
sys.path.insert(1, '/Users/ericthompson-martin/Desktop/SP2022/polarization-project/extending_satisficing_model/precise-gaussian-model')
# print(sys.path)
from gaussianModel import runModel as runGaussianModel


def main(args):
    # make plots in folder (command: python3 gifs.py sigmaHat r-val iterations numVoters)
    gaussianGraphs = runGaussianModel(args.sigmaHat, args.rationalizationFactor, args.doPlot, multiplier=10000, iterations=args.iterations)
    agentBasedGraphs = runAgentModel(sigmaHat=args.sigmaHat, rationalizationFactor=args.rationalizationFactor, numVoters=args.numVoters, forGif=True, iterations=args.iterations, toMean=args.toMean)


    for idx,(gaussianGraphs, agentBasedGraphs) in enumerate(zip(gaussianGraphs, agentBasedGraphs)):
        # plt.savefig('overlay-{}-{}-iteration-{}'.format(args.sigmaHat, args.rationalizationFactor, idx))
        print("before show plot")
        plt.gca().yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, pos: '{}'.format(x/args.numVoters)))
        plt.show()
    # make voter ideology plots
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sigmaHat", help = "sigmaHat", type=float)
    parser.add_argument("rationalizationFactor", help = "rationalization factor", type=float)
    parser.add_argument("iterations", help="Number of iterations per simulation.", type=int)
    parser.add_argument("numVoters", help="Number of agents to initialize.", type=int)
    parser.add_argument("--doPlot", "-p", help="Plot voter ideology.", action="store_true")
    parser.add_argument("--toMean", "-m", help="Parties go to their voter bases mean instead of vote maximizing ideology.", action="store_true")
    args = parser.parse_args()
    main(args)
