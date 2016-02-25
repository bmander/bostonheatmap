import pandas as pd
from pyproj import Proj
from sklearn.neighbors import KDTree
import numpy as np

# real all data
dd = pd.read_csv("data/all.csv")

# project into state plane coordinates
pj = Proj(init="epsg:2805")
x,y = pj(dd["lon"].values,dd["lat"].values)
dd["x"] = x
dd["y"] = y

# compute price per bedroom for all rows
dd["ppb"] = dd["price"]/(dd["bedrooms"]+1)

# get points for nearest neighbor search
pts = dd[["x","y"]]
price = dd["ppb"]

tree = KDTree(pts)

# get nearest neighbor indices, thus prices, thus percentiles
indices = tree.query(pts,k=300,return_distance=False)[:,1:]
neighbor_prices = price.values[ indices ]
low,mid,high = np.percentile( neighbor_prices, [5,50,95],axis=1)

# find outliers
outliers = price[ (price<low) | (price>high) ]

# drop outliers and write to disk
deoutlier = dd.drop(outliers.index)
deoutlier[["price","bedrooms","id","lon","lat","year","month","day"]].to_csv("data/all_deoutliered.csv",index=False)
