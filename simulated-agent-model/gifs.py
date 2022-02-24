from model import runModel
import argparse
import imageio as io
import os

def main(args):
    # make plots in folder (command: python3 gifs.py sigmaHat r-val iterations voters numSim -p -v -s)
    runModel(args.sigmaHat, args.rationalizationFactor, args.numVoters, args.doPlot, args.doVoters, args.iterations, args.symmetrical, args.numSimulations)
    print("running here")
    # making gif
    makeGif(args.sigmaHat, args.rationalizationFactor, args.numVoters, args.iterations)
    print("done")


def makeGif(sigmaHat, rationalizationFactor, numVoters, iterations):
    # make filelist
    filelist = []
    for i in range(1,iterations+1):
        filelist.append('../figs/simulation-figs/gif-{}-{}-{}/iteration-{}.png'.format(sigmaHat, rationalizationFactor, numVoters,i))

    # build gif
    print("compiling voter curve gif...")
    name = '../figs/simulation-figs/gifs/votercurve-{}-{}.gif'.format(sigmaHat,rationalizationFactor)
    with io.get_writer(name, mode='I') as writer:
        for filename in filelist:
            image = io.imread(filename)
            writer.append_data(image)
            os.remove(filename)

    # Remove files
    os.rmdir('../figs/simulation-figs/gif-{}-{}-{}'.format(sigmaHat, rationalizationFactor,numVoters))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sigmaHat", help = "sigmaHat", type=float)
    parser.add_argument("rationalizationFactor", help = "rationalization factor", type=float)
    parser.add_argument("iterations", help="Number of iterations per simulation.", type=int)
    parser.add_argument("numVoters", help="Number of agents to initialize.", type=int)
    parser.add_argument("numSimulations", help="Number of simulations to run.", type=int)    
    parser.add_argument("--doPlot", "-p", help="Name of file to write plot to.", action="store_true")
    parser.add_argument("--doVoters", "-v", help="Plot voter curves.", action="store_true")
    parser.add_argument("--symmetrical", "-s", help="Constrain voter ideologies to be symetrical.", action="store_true")
    parser.add_argument("--parallell", "-l", help="Parallellize running of the simulation (will be fast, and your computer will heat up).", action="store_true")
    args = parser.parse_args()
    main(args)







