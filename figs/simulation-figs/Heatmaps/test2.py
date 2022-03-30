import matplotlib.pyplot as plt
import numpy as np

def x():
  for i in range(3):
    plt.plot(np.linspace(0, i+10))
    yield None