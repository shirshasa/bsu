import numpy as np
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection, LineCollection
import matplotlib.pyplot as plt
import pylab as pl
from matplotlib import collections  as mc
# Fixing random state for reproducibility
np.random.seed(19680801)

fig, ax = plt.subplots()
N = 5


def draw_polygons(polygons,show = False):
    patches = []
    for polygon in polygons:
        print(len(polygon))
        polygon = Polygon(polygon, True)
        patches.append(polygon)

    # colors = 100 * np.random.rand(len(patches))
    p = PatchCollection(patches, alpha=0.4)
    # p.set_array(np.array(colors))
    ax.add_collection(p)



