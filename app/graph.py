import numpy as np

import matplotlib.pyplot as plt

x = list(range(0,200,20))

test_data = [-60, -84, -98, 20, -72, 10, -36, -28, -94, -80]
answer197=2
answer22=0
notSureFlag='false'

y_base_low = [-18 for _ in range(len(x))]
y_base_center = [6 for _ in range(len(x))]
y_base_up = [33 for _ in range(len(x))]


plt.plot(x, y_base_low, '#ffcccf', x, y_base_center,
         '#ffcccf', x, y_base_up, '#cccccc')
plt.fill_between(x, y_base_up, y_base_center, color='#cccccc', alpha=0.3)
plt.fill_between(x, y_base_center, y_base_low, color='#ffcccf', alpha=0.3)
plt.plot(x, test_data, linewidth=3.0)

# circle2 = plt.Circle((60, 20), 3, color='r', fill=False)
plt.gca().add_patch(circle2)


plt.grid()
plt.xlim(0, 180), plt.ylim(-100, 100)
plt.show()
