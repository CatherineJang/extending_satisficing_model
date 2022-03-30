import matplotlib.pyplot as plt
import numpy as np

from test2 import x
from test3 import y

def main():
  for (one, two) in zip(x(), y()):
    plt.show()

main()