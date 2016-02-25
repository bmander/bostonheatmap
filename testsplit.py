from numpy import random

lines = open("data/all_deoutliered.csv")

header = lines.next()

recs = list(lines)

random.shuffle( recs )

splitpoint = int(len(recs)*0.1)
test = recs[:splitpoint]
train = recs[splitpoint:]

fpout = open("data/test.csv","w")
fpout.write(header)
for row in test:
    fpout.write(row)
fpout.close()

fpout = open("data/train.csv","w")
fpout.write(header)
for row in train:
    fpout.write(row)
fpout.close()
