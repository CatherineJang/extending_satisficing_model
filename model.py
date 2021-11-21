from Gaussian import Gaussian, GaussGroup

def main(sigmaHat, rationalizationFactor):
  population = GaussGroup(startPop=True)
  partyMeanInitialGuess = 1
  for i in range(5):
    population, partyMeanInitialGuess, totalVoters = iteratePopulation(population, sigmaHat, rationalizationFactor, partyMeanInitialGuess)
    print(partyMeanInitialGuess, totalVoters, population.totalPopSize(), '\n')

def iteratePopulation(population: GaussGroup, sigmaHat, rationalizationFactor, partyMeanInitialGuess):
  """
    population is a GaussGroup that adds together 
    (some of them might be negative) to make the population.
    Returns the new population
  """

  # Step 1 using secant method
  partyMean = partyMeanInitialGuess
  epsilon = 0.01
  lastPartyMean1 = partyMeanInitialGuess + 2*epsilon
  lastPartyMean = lastPartyMean1
  dVoteTotalPrev = population.totalAreaDPartyMean(lastPartyMean, sigmaHat)

  while abs(partyMean-lastPartyMean)>epsilon:
    lastPartyMean1 = partyMean
    dVoteTotal = population.totalAreaDPartyMean(partyMean, sigmaHat)

    partyMean = partyMean - dVoteTotal*(partyMean-lastPartyMean)/(dVoteTotal-dVoteTotalPrev)
    lastPartyMean = lastPartyMean1

    dVoteTotalPrev = dVoteTotal

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

  return newPop, partyMean, party1Voters.totalPopSize()

main(0.5, 1)