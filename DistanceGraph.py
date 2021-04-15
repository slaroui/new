# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 13:43:57 2020

@author: Souwi
"""
from random import *

from conversion import *
from petalDec import *
from pruning import *
from randomGraphs import *
import pickle
import time




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


g = pickle.load( open( "ia-reality.p", "rb" ) )
outedges = pickle.load( open( "Result2/Randomia-reality.p", "rb" ) )


#Distance Graph

Dg1=[]

startG=time.time()

for i in range (100):
	for e in outedges:

		Dg1.append(bfs(g, e[0],e[1]))

finG=time.time()

pickle.dump(Dg1, open( "cro/RandomREia-reality.p", "wb" ) )
print("finG", finG-startG)