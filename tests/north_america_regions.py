from traffic.data import faa
from traffic.drawing import AlbersUSA, countries, lakes, ocean, rivers

import matplotlib.pyplot as plt

fig, ax = plt.subplots(
    figsize=(10, 10),
    subplot_kw=dict(projection=AlbersUSA())
)

ax.add_feature(countries(scale="50m"))
ax.add_feature(rivers(scale="50m"))
ax.add_feature(lakes(scale="50m"))
ax.add_feature(ocean(scale="50m", alpha=0.1))

# just a hack to push walls (i.e. projection limits)
AlbersUSA.xlimits = property(lambda _: (-3e6, 3e6))

for airspace in faa.airspace_boundary.values():

    if airspace.type == "ARTCC":
        airspace.plot(ax, edgecolor="#3a3aaa", lw=2, alpha=0.5)
        if airspace.designator != "ZAN":  # Anchorage
            airspace.annotate(
                ax,
                s=airspace.designator,
                color="#3a3aaa",
                ha="center",
                fontsize=14,
            )

    if airspace.type == "FIR" and airspace.designator[0] in ["C", "M", "K"]:
        airspace.plot(ax, edgecolor="#aa3a3a", lw=3, alpha=0.5)
        if airspace.designator not in ["CZEG", "KZWY", "KZAK"]:
            airspace.annotate(
                ax,
                s=airspace.designator,
                color="#aa3a3a",
                ha="center",
                fontsize=14,
            )

plt.show()