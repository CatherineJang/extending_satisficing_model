from Gaussian import Gaussian

def iteratePopulation(population, sigmaHat, rationalizationFactor):
  """
    population is a list of gaussians that all add together 
    (some of them might be negative) to make the population.
    Returns the new population
  """

  # Step 1 (lol)
  popMean = 1 # we will need to actually find the maximizing popMean (method TBD)

  # Step 2

  party1Satisfice = Gaussian(1, sigmaHat, popMean)
  party2Satisfice = Gaussian(1, sigmaHat, -popMean)

  bothPartiesSatisfice = party1Satisfice.multiply(party2Satisfice)

  party1Voters = []

  for popPart in population:
    party1Voters.append(party1Satisfice.multiply(popPart))

