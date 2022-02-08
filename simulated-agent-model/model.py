import math
import matplotlib.pyplot as plt
import numpy as np
import argparse

def main(args):
  for i in range(args.numSimulations):
    runModel(args.sigmaHat, args.rationalizationFactor, args.numVoters, args.doPlot, args.doVoters, args.iterations, args.symmetrical, args.numSimulations)
  plt.show()

def runModel(sigmaHat, rationalizationFactor, numVoters, doPlot=False, doVoters=False, iterations=10, symmetrical=False, numSimulations=1):
  population = np.random.normal(loc=0, scale=1, size = numVoters)
  if symmetrical:
    population = np.absolute(population)
  partyMeanInitialGuess = 1
  if doPlot and numSimulations==1:
    plt.hist(population,list(map(lambda x: x/66, range(100))),color=(0.0,0,1,0.01))
  x=[]
  for i in range(1,iterations+1):
    population, partyMeanInitialGuess = iteratePopulation(population, sigmaHat, rationalizationFactor, partyMeanInitialGuess, symmetrical)
    x.append(partyMeanInitialGuess)
    if symmetrical:
      population = np.absolute(population)
    if doPlot and numSimulations==1:
      plt.hist(population,list(map(lambda x: x/66, range(100))),color=(0.0,i/iterations,(1-i/iterations),(iterations/100+i/20)/iterations))
  if doPlot:
    if numSimulations==1:
      plt.show()
    plt.plot(x)

gr = (math.sqrt(5) + 1) / 2

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

def iteratePopulation(population, sigmaHat, rationalizationFactor, partyMeanInitialGuess, symmetrical):
  """
    population is a vector of ideologies of people in the population.
    Returns the new population
  """

  # TODO: Step 1
  partyMean = partyMeanInitialGuess
  if symmetrical:
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
    parser.add_argument("sigmaHat", help = "sigmaHat", type=float)
    parser.add_argument("rationalizationFactor", help = "rationalization factor", type=float)
    parser.add_argument("iterations", help="Number of iterations per simulation.", type=int)
    parser.add_argument("numVoters", help="Number of agents to initialize.", type=int)
    parser.add_argument("numSimulations", help="Number of simulations to run.", type=int)    
    parser.add_argument("--doPlot", "-p", help="Name of file to write plot to.", action="store_true")
    parser.add_argument("--doVoters", "-v", help="Plot voter curves.", action="store_true")
    parser.add_argument("--symmetrical", "-s", help="Constrain voter ideologies to be symetrical.", action="store_true")
    args = parser.parse_args()
    main(args)
