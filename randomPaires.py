from random import *

import pickle
#takes random paires
g = pickle.load( open( "RandomPaires/road-italy-osm.p", "rb" ) )
l=len(g)
print(l)
outedges = []
i=0
while i < 100:

	r = randrange(l)
	r1 = randrange(l)
	if r != r1:
		for e in outedges:

			if (e[0] != r and e[1] != r1) or (e[0] != r1 and e[1] != r):
				print("ok")
			else:
				break
		i=i+1
		outedges.append((r,r1))
print(len(outedges))
pickle.dump( outedges, open( "RandomPaires/road-italy-osm100.p", "wb" ) )
