# -*- coding:utf-8 -*-



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fig, ax = plt.subplots()

plt.subplot(4, 1, 1)
data = pd.DataFrame(np.random.randn(1000, 4), columns=['x', 'y', 'z', 't'])
index = range(len(data))

plt.plot(index, data['x'].cumsum(), label='xxx')

plt.subplot(4, 1, 2)
plt.plot(index, data.loc[:, ['x', 'y']].cumsum())


plt.subplot(4, 1, 3)
plt.plot(index, data.loc[:, ['x', 'y', 'z']].cumsum())

plt.subplot(4, 1, 4)
plt.plot(index, data.cumsum())

fig.set_size_inches(40, 32)
plt.show()