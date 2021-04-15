from math import *
from distance import *
import time

# t is a tree represented by a dictionary of dictionaries of weights
def pruningNicolas(t, k):
	leaves = []
	depth = {}

	for i in t:
		if len(t[i]) == 1:
			leaves.append(i)
		depth[i] = 0
	while leaves != [] and len(t) > 1:
		leaf = leaves[0]
		del leaves[0]
		dad = list(t[leaf].keys())[0]
		if depth[leaf] < k:
			depth[dad] = max(depth[dad], depth[leaf]+1)
			del t[dad][leaf]
			del t[leaf]
			if len(t[dad]) == 1:
				leaves.append(dad)
	return(t)

def pruning(t, k):
	leaves = []
	depth = {}
	t2={}
	t3={}
	for i in t:
		if len(t[i]) == 1:
			leaves.append(i)
		depth[i] = 0
	while leaves != [] and len(t) > 1:
		leaf = leaves[0]
		del leaves[0]
		dad = list(t[leaf].keys())[0]
		if depth[leaf] < k:
			depth[dad] = max(depth[dad], depth[leaf]+1)

			if dad in t2 and leaf in t2:

				t3[dad]=[]
				t3[dad].append(leaf)

				for i in t2[dad]:
					cX=0
					if i==0:
						t3[dad].append(0)

						for n in t2[leaf] :
							if n!=0:
								t3[dad].append(n)

								cX=cX+1

							else:
								del t2[leaf][:cX+1]
								break

					else:

						t3[dad].append(i)

				if t2[leaf]!=[]:
					t3[dad].append(0)
					for i in t2[leaf]:
						t3[dad].append(i)
					del t2[leaf]
				t2[dad].clear()
				for i in t3[dad]:
					t2[dad].append(i)

			elif leaf not in t2 and dad in t2:

				t3[dad]=[]
				t3[dad].append(leaf)
				for i in t2[dad]:
					t3[dad].append(i)
				t2[dad].clear()
				for i in t3[dad]:
					t2[dad].append(i)
			elif leaf in t2 and dad not in t2:

				t3[dad]=[]
				t3[dad].append(leaf)
				t3[dad].append(0)
				for i in t2[leaf]:
					t3[dad].append(i)
				del t2[leaf]
				t2[dad]=[]
				for i in t3[dad]:
					t2[dad].append(i)
			elif leaf not in t2 and dad not in t2:

				t3[dad]=[]
				t2[dad]=[]
				t2[dad].append(leaf)


			del t3[dad]


			del t[dad][leaf]
			del t[leaf]
			if len(t[dad]) == 1:
				leaves.append(dad)
	return(t,t2)










# g dictionary of dictionaries
# s source of the BFS
def pruning2Nicolas(g, s, k):

	start = time.time()
	t2={}
	t3={}
	(f, dist, ecc) = bfs(g, s)
	shells = []
	for i in range(ecc+1):
		shells.append([])
	for i in dist:
		shells[dist[i]].append(i)
	bigx = dist
	maxDist = {}
	furthest = {}
	minDist = {}
	closest = {}
	for i in bigx:
		maxDist[i] = 0
		furthest[i] = {}
	l = list(range(ecc+1))
	l.reverse()
	cptt = 0
	for d in l:
		mix = mixlist(shells[d]) # random reordering
		for x in mix:
			cptt += 1
			if len(bigx) > 1 and isConnected(g, bigx, x):
				condi = True
				for y in furthest[x]:
					if minDist[y] == k and len(closest[y]) == 1:
						condi = False
				if maxDist[x] < k or (maxDist[x] == k and condi):
					del bigx[x]
					for y in furthest[x]:
						if len(closest[y]) >= 2:
							del closest[y][x]
						else:
							minDist[y] = minDist[y] + 1
							(di, sh) = bfsBounded(g, y, minDist[y])
							for z in list(sh.keys()):
								if di[z] != minDist[y] or z not in bigx:
									del sh[z]
							closest[y] = sh
							for z in closest[y]:
								furthest[z][y] = 1
								maxDist[z] = max(maxDist[z], minDist[y])
					minDist[x] = 1
					closest[x] = {}
					for y in g[x]:
						if y in bigx:
							closest[x][y] = 1
						furthest[y][x] = 1
						maxDist[y] = max(maxDist[y], minDist[x])			

	t = {}
	for i in bigx:
		t[i] = {}
		for j in g[i]:
			if j in bigx:
				t[i][j] = 1
	r = randrange(len(t))
	f = bfs(t, list(t.keys())[r])[0]

	t2 = {}
	for i in f:
		if f[i] != i:
			if i in t2:
				t2[i][f[i]] = 1
			else:
				t2[i] = {f[i]:1}
			if f[i] in t2:
				t2[f[i]][i] = 1
			else:
				t2[f[i]] = {i:1}
	fin = time.time()
	proj = {}
	for i in g:
		if i in bigx:
			proj[i] = (i, 0)
		else:
			proj[i] = (list(closest[i])[0], minDist[i])
	return(t2, proj,fin-start)

def pruning2(g, s, k):
	t2 = {}
	t3 = {}
	start = time.time()
	(f, dist, ecc) = bfs(g, s)
	shells = []
	for i in range(ecc+1):
		shells.append([])

	for i in dist:
		shells[dist[i]].append(i)

	bigx = dist
	maxDist = {}
	furthest = {}
	minDist = {}
	closest = {}
	for i in bigx:
		maxDist[i] = 0
		furthest[i] = {}

	l = list(range(ecc+1))

	l.reverse()

	cptt = 0
	for d in l:
		mix = mixlist(shells[d]) # random reordering

		for x in mix:
			cptt += 1
			if len(bigx) > 1 and isConnected(g, bigx, x):
				condi = True
				for y in furthest[x]:
					if minDist[y] == k and len(closest[y]) == 1:
						condi = False
				if maxDist[x] < k or (maxDist[x] == k and condi):
					del bigx[x]
					for y in furthest[x]:
						if len(closest[y]) >= 2:
							del closest[y][x]
						else:
							minDist[y] = minDist[y] + 1
							(di, sh) = bfsBounded(g, y, minDist[y])
							for z in list(sh.keys()):
								if di[z] != minDist[y] or z not in bigx:
									del sh[z]
							closest[y] = sh
							for z in closest[y]:
								furthest[z][y] = 1
								maxDist[z] = max(maxDist[z], minDist[y])
					minDist[x] = 1
					closest[x] = {}
					for y in g[x]:
						if y in bigx:
							closest[x][y] = 1
						furthest[y][x] = 1
						maxDist[y] = max(maxDist[y], minDist[x])



	t = {}
	for i in bigx:
		t[i] = {}
		for j in g[i]:
			if j in bigx:
				t[i][j] = 1
	r = randrange(len(t))
	f = bfs(t, list(t.keys())[r])[0]

	t4 = {}
	for i in f:
		if f[i] != i:
			if i in t4:
				t4[i][f[i]] = 1
			else:
				t4[i] = {f[i]:1}
			if f[i] in t4:
				t4[f[i]][i] = 1
			else:
				t4[f[i]] = {i:1}
	fin = time.time()
	#proj = {}
	#for i in g:
	#	if i in bigx:
	#		proj[i] = (i, 0)
	#	else:
	#		proj[i] = (list(closest[i])[0], minDist[i])
	#print("t2---",t2)
	return(t4, fin-start)



