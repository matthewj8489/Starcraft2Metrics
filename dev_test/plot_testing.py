import matplotlib.pyplot as plt
import numpy as np

wc = [0, 0, 0, -5, -10, -13, -20, -22, -30, -26, -24, -28, -35]

plt.figure()
plt.plot(wc, label='worker time deviations')
plt.xlabel('workers')
plt.ylabel('time (s)')
plt.legend()
plt.savefig('bin\\plot_test.svg')
