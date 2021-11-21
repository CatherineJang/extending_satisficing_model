import math

class Gaussian:
  def __init__(self, coefficient, variance, mean):
    """
      Takes coef (C), variance (V), and mean (M) and initializes the Gaussian
      distribution with equation y = C(exp(-0.5(x-M)^2/V))
    """
    self.coef = coefficient
    self.var = variance
    self.mean = mean

  def multiply(self, otherGaussian):
    """
      Takes Gaussian to multiply by and returns product Gaussian
      (Does not modify original Gaussian)
    """
    newCoef = self.coef * otherGaussian.coef * (math.exp(-0.5*(self.mean-otherGaussian.mean)^2/(self.var+otherGaussian.var)))
    newVar = self.var * otherGaussian.var / (self.var + otherGaussian.var)
    newMean = (self.mean*otherGaussian.var + otherGaussian.mean*self.var)/(otherGaussian.var + self.var)
    return Gaussian(newCoef, newVar, newMean)

  def rationalized(self, to, by):
    """
      Takes value to rationalize gaussian towards and a rationalization factor
      and returns resulting Gaussian
      (Does not modify original Gaussian)
    """
    newCoef = self.coef * by
    newVar = self.var / by
    newMean = self.mean/by + (1-1/by)*to
    return Gaussian(newCoef, newVar, newMean)

  def totalArea(self):
    """
      Returns the value of the integral from negative to positive infinity of the Gaussian
    """
    return math.sqrt(2*math.pi*self.var)*self.coef

class GaussGroup:
  def __init__(self, startPop=False):
    self.gaussList = []
    if startPop:
      self.gaussList = [Gaussian(1/math.sqrt(2*math.pi),1,0)]

  def multiply(self, gaussian: Gaussian):
    newGroup = GaussGroup()
    newGroup.gaussList = list(map(lambda g: g.multiply(gaussian), self.gaussList))
    return newGroup
  
  def rationalize(self, to, by):
    newGroup = GaussGroup()
    newGroup.gaussList = list(map(lambda g: g.rationalized(to, by), self.gaussList))
    return newGroup

  def scale(self, by):
    newGroup = GaussGroup()
    newGroup.gaussList = self.gaussList[:]
    for gauss in newGroup.gaussList:
      gauss.coef = gauss.coef*by
    return newGroup

  def add(self, otherGaussGroup):
    newGroup = GaussGroup()
    newGroup.gaussList = self.gaussList + otherGaussGroup.gaussList
    return newGroup
  
  def totalPopSize(self):
    popSize = 0
    for g in self.gaussList:
      popSize += g.totalArea()
    return popSize