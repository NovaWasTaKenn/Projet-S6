import numpy as np
import random


uniques = np.unique(random.sample(range(1,50), 40), return_counts=True)
print(uniques)
dic = dict(zip(uniques[0], uniques[1]))
print(dic)
print(dic["1"])