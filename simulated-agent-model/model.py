import math
import matplotlib.pyplot as plt
import numpy as np
import argparse
from joblib import Parallel, delayed
import os

def main(args):
  # figName = '../figs/simulation-figs/party-ideologies-full-symmetry/s-{}-r-{}.png'.format(args.sigmaHat, args.rationalizationFactor)
  vary = 's'
  rationalizationFactors = [1.01, 1.02, 1.04, 1.06, 1.08, 1.1, 1.15, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2, 2.25, 2.5, 2.75, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 10] if (args.convergence and vary=='r') else [args.rationalizationFactor]
  sigmaHats = [0.1, 0.11, 0.12, 0.14, 0.16, 0.18, 0.2, 0.25, 0.3, 0.4, 0.5, 0.7, 1] if (args.convergence and vary=='s') else [args.sigmaHat]
  for rationalizationFactor in rationalizationFactors:
    for sigmaHat in sigmaHats:
      print(sigmaHat, rationalizationFactor)
      results = Parallel(n_jobs=1+args.parallell)(delayed(runModel)(sigmaHat, rationalizationFactor, args.numVoters, False, args.iterations, args.toMean, args.convergence) for j in range(args.numSimulations))
      if args.doPlot:
        for x in results:
          plt.plot(x)
      if args.convergence:
        print(results)
        plt.scatter([rationalizationFactor if vary=='r' else sigmaHat]*args.numSimulations, results)
  plt.show()

def runModel(sigmaHat, rationalizationFactor, numVoters, forGif=False, iterations=20, toMean=False, convergence=False):
  """
  sigmaHat -- the standard deviation of the party satisficing curves.
  rationalizationFactor -- how powerfully voters "rationalize" their votes. They will move to a distance that is their old distance divided by r (same direction).
  numVoters --  The number of agents in the model.
  forGif -- Whether or not to make a histogram to be made into a gif by Catherine's awesome gif code.
  iterations -- number of iterations to run the model for (sorta like election cycles... maybe).
  toMean -- if false parties go to vote maximizing ideology, if true parties go to mean ideology of their "half" of the population ideology distribution.
  convergence -- if true stop at convergence and return number of iterations, if false return vector with party ideology over time.  
  """
  print(sigmaHat, rationalizationFactor)
  population = np.random.normal(loc=0, scale=1, size = numVoters)
  np.random.normal()
  population = np.absolute(population)
  partyMeanInitialGuess = 1
  if forGif:
    plt.hist(population,list(map(lambda x: x/100, range(100))),color=(0.0,0,1,0.5))
    print("after yield")
    # os.mkdir('../figs/simulation-figs/gif-images/gif-{}-{}'.format(sigmaHat, rationalizationFactor))
    figName = '../figs/simulation-figs/gif-images/gif-{}-{}/iteration-{}.png'.format(sigmaHat, rationalizationFactor, 0)
    print("before yield agent")
    yield popHistForGif(population, 0, numVoters, figName)
  partyMeanList=[]
  populationMeanList=[]
  
  for itnum in range(1,iterations+1):
    population, newPartyMean = iteratePopulation(population, sigmaHat, rationalizationFactor, partyMeanInitialGuess, toMean)
    if convergence:
      if newPartyMean<0.04:
        return itnum
    partyMeanInitialGuess=newPartyMean
    partyMeanList.append(partyMeanInitialGuess)
    populationMeanList.append(np.mean(population))
    population = np.absolute(population)
    if forGif:
      figName = '../figs/simulation-figs/gif-images/gif-{}-{}/iteration-{}.png'.format(sigmaHat, rationalizationFactor, itnum)
      yield popHistForGif(population, itnum, numVoters, figName)

  if convergence:
    print(iterations)
    return iterations
  return partyMeanList

gr = (math.sqrt(5) + 1) / 2

def popHistForGif(population, i, numVoters, figName):
  # add the negative population ideology back
  negpop = np.negative(population)
  totalpop = np.concatenate((population,negpop), axis=None)
  ideologyPlotBound = 1.25 # histogram will be from -this to +this
  numBuckets = 50
  plt.hist(totalpop,list(map(lambda x: (x-numBuckets/2)/numBuckets*2*ideologyPlotBound, range(numBuckets))))
  plt.title('Iteration {}'.format(i))
  plt.xlabel("Population")
  plt.ylabel("Ideology")
  plt.xlim(0-ideologyPlotBound,ideologyPlotBound)
  plt.ylim(0, numVoters)
  # plt.savefig(figName)
  # plt.cla()

def graph(formula, x, hue, b):
    y = list(map(lambda x: formula(x/100), x))
    x = x + list(map(lambda a: 0-a, x[-2::-1]))
    y = y + y[-2::-1]
    plt.plot(x, y, color=(int(b), hue, int(not b)), linewidth=1)

def gss(f, a, b, tol=1e-3):
    """Golden-section search
    to find the minimum of f on [a,b]
    f: a strictly unimodal function on [a,b]

    Example:
    >>> f = lambda x: (x-2)**2
    >>> x = gss(f, 1, 5)
    >>> print("%.15f" % x)
    2.000009644875678

    """
    c = b - (b - a) / gr
    d = a + (b - a) / gr
    while abs(b - a) > tol:
        if f(c) < f(d):
            b = d
        else:
            a = c

        # We recompute both c and d here to avoid loss of precision which may lead to incorrect results or infinite loop
        c = b - (b - a) / gr
        d = a + (b - a) / gr

    return (b + a) / 2

def iteratePopulation(population, sigmaHat, rationalizationFactor, partyMeanInitialGuess, toMean):
  """
    population is a vector of ideologies of people in the population.
    Returns the new population
  """

  # TODO: Step 1 for non-symetrical
  partyMean = partyMeanInitialGuess
  if toMean:
    partyMean=np.mean(population)
  else:
    def fToMinimize(partyMean):
      # Gaussians for proportion of people at an ideology who are satisfied by each party and both
      party1SatisficeProbs = np.array(list(map(lambda x: math.exp(0-(x-partyMean)**2/sigmaHat/2), population)))
      party2SatisficeProbs = np.array(list(map(lambda x: math.exp(0-(x+partyMean)**2/sigmaHat/2), population)))
      bothPartiesSatisfice = party1SatisficeProbs * party2SatisficeProbs
      return 0 - np.sum(party1SatisficeProbs) - np.sum(party2SatisficeProbs) + np.sum(bothPartiesSatisfice)
    partyMean = gss(fToMinimize, 0, partyMeanInitialGuess*2)

  # Step 2

  # Gaussians for proportion of people at an ideology who are satisfied by each party and both
  party1SatisficeProbs = np.array(list(map(lambda x: math.exp(0-(x-partyMean)**2/sigmaHat/2), population)))
  party2SatisficeProbs = np.array(list(map(lambda x: math.exp(0-(x+partyMean)**2/sigmaHat/2), population)))

  party1SatisficeUniform = np.random.uniform(size=population.shape)
  party2SatisficeUniform = np.random.uniform(size=population.shape)
  party1Satisfice = party1SatisficeProbs > party1SatisficeUniform
  party2Satisfice = party2SatisficeProbs > party2SatisficeUniform

  notBothSatisfice = np.logical_not(party1Satisfice & party2Satisfice)

  tieBreakerUniform = np.random.uniform(size=population.shape)

  # Find all voters for each party
  party1Voters = party1Satisfice & (notBothSatisfice | (tieBreakerUniform > 0.5))
  party2Voters = party2Satisfice & (notBothSatisfice | (tieBreakerUniform < 0.5))

  # Step 3 & 4

  votes = [0,0]
  for i in range(population.shape[0]):
    if party1Voters[i]:
      population[i] += ((rationalizationFactor-1)/rationalizationFactor)*(partyMean - population[i])
      votes[0]+=1
    if party2Voters[i]:
      population[i] += ((rationalizationFactor-1)/rationalizationFactor)*(0-partyMean - population[i])
      votes[1]+=1

  return population, partyMean


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sigmaHat", help = "sigma hat (broadness of party appeal relative to broadness of population ideology).", type=float)
    parser.add_argument("rationalizationFactor", help = "rationalization factor (the proportion voters cut their distance to their party by after voting).", type=float)
    parser.add_argument("iterations", help="Number of iterations per simulation.", type=int)
    parser.add_argument("numVoters", help="Number of agents to initialize.", type=int)
    parser.add_argument("numSimulations", help="Number of simulations to run.", type=int)    
    parser.add_argument("--doPlot", "-p", help="Toggle plot for party ideologies over time.", action="store_true")
    parser.add_argument("--parallell", "-l", help="Parallellize running of the simulation (will be fast, and your computer will heat up).", action="store_true")
    parser.add_argument("--toMean", "-m", help="Parties go to their voter bases mean instead of vote maximizing ideology.", action="store_true")
    parser.add_argument("--convergence", "-c", help="Stop if converged and return convergence time. Only outputs graph when parallelized.", action="store_true")
    args = parser.parse_args()
    main(args)
