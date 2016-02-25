import pandas as pd

import matplotlib
matplotlib.use('AGG')

from matplotlib import pyplot as plt
import numpy as np
from pyproj import Proj
from sklearn.neighbors import RadiusNeighborsRegressor, KDTree
from sklearn import cross_validation
from sklearn.neighbors import KNeighborsRegressor
import shapefile

# get raw data

print "loading data"
dd = pd.read_csv("data/train.csv")

minlat,minlon = dd.min()[["lat","lon"]]
maxlat,maxlon = dd.max()[["lat","lon"]]

# add stateplane projection features
# the projection is in meters, and has the same spatial scale in the x and y dimensions
pj = Proj(init="epsg:2805")
x,y = pj(dd["lon"].values,dd["lat"].values)
dd["x"] = x
dd["y"] = y

# add month ordinal feature
dd["monthord"] = dd.year*12 + dd.month

# train the model
print "fitting model"
clf = KNeighborsRegressor(n_neighbors=15,weights=lambda x:1/(x**2+200))

X = dd[["x","y","bedrooms","monthord"]]*[1,1,15000,15]
y = dd["price"]

clf.fit(X,y)

#============== DRAW HEATMAP ==================

print "drawing heatmap"
sf = shapefile.Reader("mapdata/borders")
borders = sf.shapes()

plt.ioff()

N = 400
dpi = 150
res = 800
figwidth = res/dpi

bedrooms = 3
monthord = 2014*12+0

# generate sample grid
xmin,ymin = dd.min()[["x","y"]]
xmax,ymax = dd.max()[["x","y"]]

xs = np.linspace(xmin,xmax,N)
ys = np.linspace(ymin,ymax,N)

xx, yy = [x.ravel() for x in np.meshgrid(xs,ys)]

grid_dd = pd.DataFrame.from_items((("x",xx),("y",yy),("bedrooms",bedrooms),("monthord",monthord)))
prices = clf.predict( grid_dd*[1,1,15000,15] )

# create figure
fig = plt.figure(figsize=(figwidth,figwidth),dpi=dpi,frameon=False)

# hide axes
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

# print contour map
cs = plt.contourf(xs,ys,prices.reshape((N,N)),levels=range(0,6500,500))
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)

# print date
year = int(monthord/12)
month = int(monthord%12)
day = int((monthord - (12*year+month))*31)
plt.text(0.95, 0.05,'%d/%02d/%02d'%(year,month+1,day+1), horizontalalignment='right', verticalalignment='bottom', transform=plt.gca().transAxes, fontsize=14)

# print number of bedrooms
bedtext = "bedroom" if bedrooms==1 else "bedrooms"
plt.text(0.5, 0.05,'%s %s'%(bedrooms,bedtext), horizontalalignment='center', verticalalignment='bottom', transform=plt.gca().transAxes, fontsize=14)

# create a legend for the contour set
artists, labels = cs.legend_elements()
labels = map(str, range(500,6500,500))
plt.legend(artists, labels, handleheight=1, fontsize=7)

# draw geographical borders
for border in borders:
    borderx,bordery = np.array( border.points ).T
    plt.plot(borderx,bordery,color="black",linewidth=0.2)

# save to disk
with open('heatmap.png', 'w') as outfile:
    fig.canvas.print_png(outfile)
