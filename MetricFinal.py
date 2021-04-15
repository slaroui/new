# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 18:06:02 2020

@author: Souwi
"""



from random import *
from conversion import *
from petalDec import *
from pruning import *
from randomGraphs import *
import pickle
import timeit



g = pickle.load( open( "ia-reality.p", "rb" ) )
t = pickle.load( open( "ia-reality/AlgoF/treepruningFia-reality.p", "rb" ) )
Dg1 = pickle.load( open( "Distance Graph/RandomREia-reality.p", "rb" ) )
outedges = pickle.load( open( "Result2/Random/Randomia-reality.p", "rb" ) )

def firstInSet(g, s, t):
	dist = {}
	toVisit = [s]
	seen = {s:1}
	dist[s] = 0
	found = False
	while not found:
		current = toVisit[0]
		del toVisit[0]
		if current in t:
			found = True
		else:
			for neigh in g[current]:
				if neigh not in seen:
					dist[neigh] = dist[current] + 1
					toVisit.append(neigh)
					seen[neigh] = 1
	return(current, dist[current])

def bfs(g, s,d):

	dist = {}
	toVisit = [s]
	seen = {s:1}
	dist[s] = 0

	while toVisit != []:
		current = toVisit[0]
		del toVisit[0]
		l = list(g[current].keys())
		l2 = mixlist(l)
		for neigh in l2:
			if neigh not in seen:
				dist[neigh] = dist[current] + 1

				toVisit.append(neigh)
				seen[neigh] = 1
		if current == d:
			break
	return( dist[current])



#Relative error our methods
#with refining

DtR=[]
DtWR=[]
RER=0
REWR=0

#Distance Graph
"""
startG=time.time()

for i in range (100):
	for e in outedges:

		Dg1.append(bfs(g, e[0],e[1]))

finG=time.time()
print("finG")
"""






#distance Tree
startT=timeit.default_timer()
projX = {}
projY = {}
i=0
for e in outedges:
	projX[i] = firstInSet(g, e[0], t)
	projY[i] = firstInSet(g, e[1], t)
	DistanceTotal=projX[i][1]+ bfs(t,projX[i][0],projY[i][0])+projY[i][1]
	DtR.append(DistanceTotal)
	i=i+1
finT=timeit.default_timer()

#Relative Error
for i in range (100):

	RER= RER+((abs(Dg1[i]- DtR[i]))/Dg1[i])


print("With Refining RE=", RER/100,"TimeT= ",finT-startT )

#without Refining 

#Distance Tree
startTWR=timeit.default_timer()


for e in outedges:
	if( e[0] in t) and (e[1] in t):
		DtWR.append(bfs(t,e[0],e[1]))
	else:
		DtWR.append(0)

finTWR=timeit.default_timer()

#Relative Error
for i in range (100):

	REWR= REWR+((abs(Dg1[i]- DtWR[i]))/Dg1[i])

print("Without Refining RE=", REWR/100,"TimeT= ",finTWR-startTWR )









