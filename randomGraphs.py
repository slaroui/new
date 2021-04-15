from math import *
from random import *


# creates a random unit disk graph on n vertices in a 1x1 square with balls of radius r
def unitDiskGraph(n, r):
	points = []
	for i in range(n):
		x = random()
		y = random()
		points.append((x,y))
	g = {}
	for i in range(n):
		g[i] = {}
		for j in range(n):
			if j != i:
				if pow(points[j][0] - points[i][0], 2) + pow(points[j][1] - points[i][1], 2) <= 4*pow(r, 2):
					g[i][j] = 1
	return(g)


# creates a random disk graph on n vertices in a 1x1 square with balls of radius between rmin and rmax					
def diskGraph(n, rmin, rmax):
	points = []
	for i in range(n):
		x = random()
		y = random()
		r = uniform(rmin,rmax)
		points.append((x,y,r))
	g = {}
	for i in range(n):
		g[i] = {}
		for j in range(n):
			if j != i:
				if pow(points[j][0] - points[i][0], 2) + pow(points[j][1] - points[i][1], 2) <= pow(points[i][2] + points[j][2], 2):
					g[i][j] = 1
	return(g, points)
	

# Good parameters for almost connected graphs
#g = diskGraph(100, 0.07, 0.1)
#g = diskGraph(200, 0.05, 0.08)
#g = diskGraph(500, 0.03, 0.05)
#g = diskGraph(1000, 0.025, 0.035)
#g = diskGraph(2000, 0.015, 0.025)
#g = diskGraph(5000, 0.012, 0.018)
#g = diskGraph(10000, 0.008, 0.012)
#g = diskGraph(20000, 0.0045, 0.006)


# returns a random spanning tree by making a connected component growing
def randSpanTree(g):
	i = randrange(len(g))
	s = list(g.keys())[i]
	t = {s:{}}
	outedges = []
	for i in g[s]:
		outedges.append((s,i))
	while len(t) < len(g):


		r = randrange(len(outedges))
		(x,y) = outedges[r]
		t[x][y] = 1
		t[y] = {x:1}
		outedges2 = []
		for ed in outedges:
			if ed[1] != y:
				outedges2.append(ed)
		for i in g[y]:
			if i not in t:
				outedges2.append((y,i))
		outedges = list(outedges2)
	return(t)
	

# random reordering of l
def mixlist(l):
	l2 = []
	n = len(l)
	for i in range(n):
		r = randrange(len(l))
		l2.append(l[r])
		del l[r]
	return(l2)
	
