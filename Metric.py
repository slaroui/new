# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 18:09:51 2020

@author: Souwi
"""
from random import *
from distance import *
from conversion import *
from petalDec import *
from pruning import *
from randomGraphs import *
import time

import pickle
#takes random paires
g = pickle.load( open( "musae_facebook_edges.p", "rb" ) )
t = pickle.load( open( "Result3/fatherfileaface.p", "rb" ) )
outedges=pickle.load( open( "Result3/Random/facebook10.p", "rb" ) )

def dijkstra(g, s,d):
	n = len(g)
	father = {}
	dist = {}
	toVisit = {s:1}
	visited = {}
	for i in g:
		dist[i] = n  # Warning: lies on the fact that weights are either 1 or 1/2
	dist[s] = 0
	father[s] = s
	while toVisit != {}:
		mindist = n
		l = mixlist(list(toVisit.keys()))
		for i in l:
			if dist[i] < mindist:
				current = i
				mindist = dist[i]
		for neigh in g[current]: # random ordering
			if neigh not in visited and dist[current] + g[current][neigh] < dist[neigh]:
				dist[neigh] = dist[current] + g[current][neigh]


				father[neigh] = current
				toVisit[neigh] = 1

		if current == d:
			break
		visited[current] = 1
		del toVisit[current]

	return( dist[d])

def distTree(father,x,y):


	lx = [x]
	a = x
	while father[a] != a:
		lx.append(father[a])
		print(father[a],a)
		a = father[a]
	ly = [y]
	b = y
	while father[b] != b:
		ly.append(father[b])
		b = father[b]
	i = 1
	while i <= len(lx) and i <= len(ly) and lx[-i] == ly[-i]:
		i += 1
	d = len(lx)+len(ly)-2*i+2
	return(d)



#calculate RE+Time
dg = 0
dT = 0
RE = 0
Dg1=[]
Dt1=[]
startG=time.time()

for i in range (10):
	for e in outedges:

		Dg1.append(dijkstra(g, e[0],e[1]))

finG=time.time()
print("finG")

startT=time.time()
for i in range (10):
	for e in outedges:

		#dT=distTree(t, e[0],e[1])
		Dt1.append(distTree(t, e[0],e[1]))
finT=time.time()
print("fin")
for i in range (10):

	RE= RE+((Dg1[i]- Dt1[i])/Dg1[i])



print("RE=", RE/10,"TimeG= ",finG-startG,"TimeT= ",finT-startT )

pickle.dump( Dg1, open( "Result3/DGFace.p", "wb" ) )



