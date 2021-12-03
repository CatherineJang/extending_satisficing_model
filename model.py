from Gaussian import Gaussian, GaussGroup
import math
import matplotlib.pyplot as plt
import numpy as np
import argparse

def main(args):
  population = GaussGroup(startPop=True)
  partyMeanInitialGuess = 1
  if args.doPlot:
    graph(population.eval, range(0, 1510, 10), 1, False)
  for i in range(1,args.iterations+1):
    population, partyMeanInitialGuess, voters1 = iteratePopulation(population, args.sigmaHat, args.rationalizationFactor, partyMeanInitialGuess)
    partyMean = int(1000*partyMeanInitialGuess)
    if args.doPlot:
      graph(population.eval, range(0, 1510, 10), 1-1*i/args.iterations, False)
      if args.doVoters:
        graph(voters1.eval, range(0, 1510, 10), 1-1*i/args.iterations, True)
      plt.plot([partyMean, partyMean], [0,0.5], color=(0, 1-1*(i-1)/args.iterations, 1), linewidth=1)
      plt.xlabel("Population")
      plt.ylabel("Ideology")
    print(partyMeanInitialGuess)
  if args.doPlot:
    plt.show()

gr = (math.sqrt(5) + 1) / 2

def graph(formula, x_range, hue, b):  
    x = np.array(x_range)  
    y = np.array(list(map(formula, list(x_range))))
    plt.plot(x, y, color=(int(b), hue, int(not b)), linewidth=1)

def gss(f, a, b, tol=1e-2):
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

def iteratePopulation(population: GaussGroup, sigmaHat, rationalizationFactor, partyMeanInitialGuess):
  """
    population is a GaussGroup that adds together 
    (some of them might be negative) to make the population.
    Returns the new population
  """

  # Step 1 using gss method

  def fToMinimize(partyMean):
    # Gaussians for proportion of people at an ideology who are satisfied by each party and both
    party1Satisfice = Gaussian(1, sigmaHat, partyMean)
    party2Satisfice = Gaussian(1, sigmaHat, 0-partyMean)
    bothPartiesSatisfice = party1Satisfice.multiply(party2Satisfice)
    # Potential voter group for each party (double counting doubly satisfied voters)
    party1Voters = population.multiply(party1Satisfice)
    party2Voters = population.multiply(party2Satisfice)
    # Remove half of doubly satisfied voters from each party
    doubleCountedVoters = population.multiply(bothPartiesSatisfice).scale(-0.5)
    party1Voters = party1Voters.add(doubleCountedVoters)
    party2Voters = party2Voters.add(doubleCountedVoters)
    return 0-party1Voters.totalPopSize()
  partyMean = gss(fToMinimize, 0, partyMeanInitialGuess*2)
  # uncomment to plot total votes at each ideology
  # graph(lambda x: 0-fToMinimize(x/1000), range(0, 1510, 10), 0, False)
  # plt.plot([partyMean*1000, partyMean*1000], [0,0.5], color=(0, 1, 1), linewidth=1)
  # plt.show()

  # Step 1 using secant method
  # epsilon = 0.01
  # lastPartyMean1 = partyMeanInitialGuess + 2*epsilon
  # lastPartyMean = lastPartyMean1
  # dVoteTotalPrev = population.totalAreaSecPartyMean(lastPartyMean, sigmaHat, epsilon)

  # while abs(partyMean-lastPartyMean)>epsilon:
  #   lastPartyMean1 = partyMean
  #   dVoteTotal = population.totalAreaSecPartyMean(partyMean, sigmaHat, epsilon)
  #   # dVoteTotalEpsilon = population.totalAreaDPartyMean(partyMean+epsilon, sigmaHat)

  #   partyMean = partyMean - dVoteTotal*(partyMean-lastPartyMean)/(dVoteTotal-dVoteTotalPrev)
  #   # partyMean = partyMean - dVoteTotal*(epsilon)/(dVoteTotalEpsilon - dVoteTotal)
  #   lastPartyMean = lastPartyMean1

  #   dVoteTotalPrev = dVoteTotal


  # Step 2

  # Gaussians for proportion of people at an ideology who are satisfied by each party and both
  party1Satisfice = Gaussian(1, sigmaHat, partyMean)
  party2Satisfice = Gaussian(1, sigmaHat, 0-partyMean)
  bothPartiesSatisfice = party1Satisfice.multiply(party2Satisfice)

  # Potential voter group for each party (double counting doubly satisfied voters)
  party1Voters = population.multiply(party1Satisfice)
  party2Voters = population.multiply(party2Satisfice)

  # Remove half of doubly satisfied voters from each party
  doubleCountedVoters = population.multiply(bothPartiesSatisfice).scale(-0.5)
  party1Voters = party1Voters.add(doubleCountedVoters)
  party2Voters = party2Voters.add(doubleCountedVoters)

  # Step 3

  party1VotersRationalized = party1Voters.rationalize(partyMean, rationalizationFactor)
  party2VotersRationalized = party2Voters.rationalize(0-partyMean, rationalizationFactor)

  # Step 4

  oldVotersRemoved = party1Voters.scale(-1).add(party2Voters.scale(-1))
  newVotersAdded = party1VotersRationalized.add(party2VotersRationalized)

  newPop = population.add(oldVotersRemoved).add(newVotersAdded)

  return newPop, partyMean, party1Voters


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sigmaHat", help = "sigmaHat", type=float)
    parser.add_argument("rationalizationFactor", help = "rationalization factor", type=float)
    parser.add_argument("iterations", help="Number of iterations.", type=int)
    parser.add_argument("--doPlot", "-p", help="Name of file to write plot to.", action="store_true")
    parser.add_argument("--doVoters", "-v", help="Plot voter curves.",action="store_true")
    args = parser.parse_args()
    main(args)
