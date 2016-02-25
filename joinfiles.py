import os
import csv
import datetime

fns = os.listdir("data")

allrecs = []
seen = set()
for fn in fns:
    ts = int(fn.split("-")[1].split(".")[0])
    dt = datetime.datetime.fromtimestamp( ts )

    fp = open( os.path.join("data",fn) )

    for line in fp:
        rec = line.split()
        rec.extend( [dt.year,dt.month,dt.day] )

        key = (rec[0],rec[1],rec[3],rec[4])
        if key not in seen:
        	allrecs.append( rec )
        seen.add(key)

fpout = open("data/all.csv","w")
fpout.write("price,bedrooms,id,lon,lat,year,month,day\n")

for rec in allrecs:
    fpout.write( ",".join(map(str,rec)) )
    fpout.write( "\n" )

fpout.close()
