import matplotlib.pyplot as plt

from traffic.core.projection import Amersfoort, GaussKruger, Lambert93, EuroPP
from traffic.drawing import countries
from traffic.data.samples import quickstart, belevingsvlucht, airbus_tree


plt.style.context("traffic")
fig = plt.figure()
ax = fig.add_subplot(projection=EuroPP())
ax.add_feature(countries())
ax.set_global()
ax.outline_patch.set_visible(False)
ax.background_patch.set_visible(False)
ax.set_extent((-8, 18, 40, 60))

quickstart["AFR27GH"].plot(ax)
belevingsvlucht.plot(ax)

params = dict(fontsize=18, pad=12)
ax.set_title("EuroPP()", **params)

plt.show()