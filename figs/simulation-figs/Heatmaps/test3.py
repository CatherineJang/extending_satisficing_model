import matplotlib.pyplot as plt
import numpy as np

def y():
  for i in range(3):
    plt.hist([1,2,3,4,5,6], color=(0.0,0,1,0.5))
    yield None