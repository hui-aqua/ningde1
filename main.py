import numpy as np
import src.test.pointsVisualization as pv
import src.geoMaker.circular as geo

p=geo.gen_points()
print(p)
pv.show_point(p)