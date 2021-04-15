from random import *
from distance import *
from conversion import *
from petalDec import *
from pruning import *
from randomGraphs import *
import time




# A BFS tree from a random vertex + pruning
def algoAbfs(g,k):
	start=time.time()
	#i = randrange(len(g))
	s = list(g.keys())[1]
	(f, d, r) = bfs(g, s)
	el = edgelistFromFather(f)

	t1 = graphFromEdgelist(el)

	t2 = {}
	for i in t1:
		t2[i] = {}
		for j in t1[i]:
			t2[i][j] = t1[i][j]


	(t,tc) = pruning(t2, k)

	fin = time.time()

	return(t, fin-start,f,tc)


# A petal decomposition from a random vertex + pruning
def algoBpetal(g,k):
	start = time.time()
	#i = randrange(len(g))
	s = list(g.keys())[1]

	el = decomposition(g, s)
	t1 = graphFromEdgelist(el)

	f = bfs(t1, s)[0]
	t2 = {}
	for i in t1:
		t2[i] = {}
		for j in t1[i]:
			t2[i][j] = t1[i][j]
	(t,tc) = pruning(t2, k)
	fin = time.time()
	# distance induced by the spanning tree
	#dt = distTree(f)
	#distt = lambda x,y : dt[min(x,y)][max(x,y)]
	#2 distance induced by shortest distances to the subtree
#	proj = {}
#	for i in g:
#		proj[i] = firstInSet(g, i, t)
#	distt = lambda x,y : proj[x][1] + dt[min(proj[x][0],proj[y][0])][max(proj[x][0],proj[y][0])] + proj[y][1]
	return(t, fin-start,f,tc)


# A random spanning tree + pruning
def algoCrst(g,k):
	start=time.time()
	t1 = randSpanTree(g)
	#i = randrange(len(t1))
	s = list(t1.keys())[1]
	f = bfs(t1, s)[0]
	t2 = {}
	for i in t1:
		t2[i] = {}
		for j in t1[i]:
			t2[i][j] = t1[i][j]
	(t,tc) = pruning(t2, k)
	fin = time.time()
	# distance induced by the spanning tree
	#dt = distTree(f)
	#distt = lambda x,y : dt[min(x,y)][max(x,y)]
	#2 distance induced by shortest distances to the subtree
#	proj = {}
#	for i in g:
#		proj[i] = firstInSet(g, i, t)
#	distt = lambda x,y : proj[x][1] + dt[min(proj[x][0],proj[y][0])][max(proj[x][0],proj[y][0])] + proj[y][1]
	return(t,fin-start,f,tc)




# A tree made greedily with the formula + pruning
def algoDformula1(g,k):
	start = time.time()
	depth = {}
	threemax = {}
	dt1 = {}
	father = {}
	kneigh = {}
	for i in g:
		kneigh[i] = bfsBounded(g, i, k-1)[1]
		depth[i] = {}
		threemax[i] = []
		for j in g[i]:
			depth[i][j] = 0
	i = randrange(len(g))
	s = list(g.keys())[i]
	t1 = {s:{}}
	dt1[s] = {s:0}
	father[s] = {} # father[y][x] is the last node before y on the path from x to y
	outedges = []
	for i in g[s]:
		outedges.append((s,i))
	while len(t1) < len(g):
		nodes = {}
		for e in outedges:
			x = e[0]
			if x not in nodes:
				nodes[x] = 1
			else:
				nodes[x] += 1
		gains = {}
		maxgain = 0
		l = mixlist(list(nodes.keys()))
		for x in l:
			gains[x] = 0
			if len(threemax[x]) >= 2:
				gains[x] = 1
			else:
				for y in kneigh[x]:
					if (y != x and len(threemax[y]) == 3 and dt1[x][y] == depth[y][father[y][x]] and dt1[x][y] < threemax[y][1]):
						gains[x] = 1
						break
			if gains[x] == 1:
				maxgain = 1
				break
		optedges = []
		for e in outedges:
			if e[0] in gains and gains[e[0]] == maxgain:
				optedges.append(e)
		r = randrange(len(optedges))
		(x,y) = optedges[r]
		dt1[y] = {y:0}
		father[y] = {}
		for z in t1:
			if z == x:
				depth[x][y] = 1
				dt1[x][y] = 1
				dt1[y][x] = 1
				father[x][y] = y
				father[y][x] = x
				if len(threemax[x]) <= 2:
					threemax[x].append(1)
			else:
				dt1[z][y] = dt1[z][x] + 1
				dt1[y][z] = dt1[z][x] + 1
				father[z][y] = father[z][x]
				father[y][z] = x
				if dt1[x][z] == depth[z][father[z][x]]:
					depth[z][father[z][x]] += 1
					#print("if1")
					if dt1[x][z] == threemax[z][0]:
						threemax[z][0] += 1
						#print("if2")
					elif dt1[x][z] == threemax[z][1]:
						threemax[z][1] += 1
						#print("if3")
					elif dt1[x][z] == threemax[z][2]:
						threemax[z][2] += 1
						#print("if4")
		t1[x][y] = 1
		t1[y] = {x:1}
		outedges2 = []
		for ed in outedges:
			if ed[1] != y:
				outedges2.append(ed)
		for i in g[y]:
			if i not in t1:
				outedges2.append((y,i))
		outedges = list(outedges2)
	i = randrange(len(t1))
	s = list(t1.keys())[i]
	t2 = {}
	for i in t1:
		t2[i] = {}
		for j in t1[i]:
			t2[i][j] = t1[i][j]
	t = pruning(t2, k)
	fin = time.time()
	# distance induced by the spanning tree
	#distt = lambda x,y : dt1[x][y]
	#2 distance induced by shortest distances to the subtree
#	proj = {}
#	for i in g:
#		proj[i] = firstInSet(g, i, t)
#	distt = lambda x,y : proj[x][1] + dt1[min(proj[x][0],proj[y][0])][max(proj[x][0],proj[y][0])] + proj[y][1]
	return(t,fin-start, dt1,t1)






# A tree made greedily with the formula + pruning
def algoDformula(g,k):
	start = time.time()
	depth = {}
	threemax = {}
	dt1 = {}
	father = {}
#	kneigh = {}
	for i in g:
#		kneigh[i] = bfsBounded(g, i, k-1)[1]
		depth[i] = {}
		threemax[i] = []
		for j in g[i]:
			depth[i][j] = 0
	i = randrange(len(g))
	s = list(g.keys())[i]
	t1 = {s:{}}
	dt1[s] = {s:0}
	father[s] = {} # father[y][x] is the last node before y on the path from x to y
	outedges = []
	for i in g[s]:
		outedges.append((s,i))
	while len(t1) < len(g):
		nodes = {}
		for e in outedges:
			x = e[0]
			if x not in nodes:
				nodes[x] = 1
			else:
				nodes[x] += 1
		gains = {}
		l = mixlist(list(nodes.keys()))
		for x in l:
			gains[x] = 0
			maxgain = gains[x]
			for y in l:

				if y == x and len(threemax[x]) >= 2:
					gains[x] = 1
				elif (y != x and dt1[x][y] == depth[y][father[y][x]] and dt1[x][y] < k):
					for v in g[y]:
						count=0
						if v in t1  and v!= x and v!= y and x in g[y]:

							if depth[y][v] > depth[y][x]:
								count +=1
								if count >= 2:
									gains[x] += 1
									break
			if maxgain < gains[x]:
				maxgain = gains[x]

		optedges = []
		for e in outedges:
			if e[0] in gains and gains[e[0]] == maxgain:
				optedges.append(e)
		r = randrange(len(optedges))
		(x,y) = optedges[r]
		dt1[y] = {y:0}
		father[y] = {}
		for z in t1:
			if z == x:
				depth[x][y] = 1

				dt1[x][y] = 1
				dt1[y][x] = 1
				father[x][y] = y
				father[y][x] = x
    
				if len(threemax[x]) <= 2:
					threemax[x].append(1)
			else:
				dt1[z][y] = dt1[z][x] + 1
				dt1[y][z] = dt1[z][x] + 1
				father[z][y] = father[z][x]
				father[y][z] = x
				depth[z][father[z][x]]= depth[z][father[z][x]]+1

		#		if dt1[x][z] == depth[z][father[z][x]]:
		#			depth[z][father[z][x]] += 1
		#			if dt1[x][z] == threemax[z][0]:
		#				threemax[z][0] += 1
		#			elif dt1[x][z] == threemax[z][1]:
		#				threemax[z][1] += 1
		#			elif dt1[x][z] == threemax[z][2]:
		#				threemax[z][2] += 1
		t1[x][y] = 1
		t1[y] = {x:1}
		outedges2 = []
		max=0
		for j in g[x]:
			if j in t1 and j != y and x!= j:

				if max < depth[x][j]+1:
					max = depth[x][j]+1
		depth[y][x] = max
		for ed in outedges:
			if ed[1] != y:
				outedges2.append(ed)
		for i in g[y]:
			if i not in t1:
				outedges2.append((y,i))
		outedges = list(outedges2)
	i = randrange(len(t1))
	s = list(t1.keys())[i]
	t2 = {}
	for i in t1:
		t2[i] = {}
		for j in t1[i]:
			t2[i][j] = t1[i][j]
	t = pruning(t2, k)
	fin = time.time()
	# distance induced by the spanning tree
	#distt = lambda x,y : dt1[x][y]
	#2 distance induced by shortest distances to the subtree
#	proj = {}
#	for i in g:
#		proj[i] = firstInSet(g, i, t)
#	distt = lambda x,y : proj[x][1] + dt1[min(proj[x][0],proj[y][0])][max(proj[x][0],proj[y][0])] + proj[y][1]
	return(t,fin-start,dt1,t1)


# pruning on general graphs
def algoEdirprun(g,k):
	start=time.time()
	#i = randrange(len(g))
	s = list(g.keys())[1]
	fin =time.time()
	(t, time1) = pruning2(g, s, k)
	#i = randrange(len(t))
	#s = list(t.keys())[i]
	#f = bfs(t, s)[0]
	#dt = distTree(f)
	#distt = lambda x,y : p[x][1] + dt[min(p[x][0],p[y][0])][max(p[x][0],p[y][0])] + p[x][1]
	return(t,fin-start+time1)


# greedy algo from set cover applied to k-dominating set + naive Steiner tree
def algoFgreedyNicolas(g,k):
	start=time.time()
	gk = {}
	for i in g:
		gk[i] = bfsBounded(g, i, k)[1]
	covered = {}
	kdomset = {}
	neighsize = {}
	proj = {}
	for i in g:
		neighsize[i] = len(gk[i])
	while len(covered) != len(g):
		maxi = 0
		maxindex = -1
		for i in g:
			if i not in kdomset:
				if neighsize[i] > maxi:
					maxi = neighsize[i]
					maxindex = i
		kdomset[maxindex] = 1
		proj[maxindex] = (maxindex, 0)
		for j in gk[maxindex]:
			if j not in covered:
				covered[j] = 1
				for l in g:
					if j in gk[l]:
						neighsize[l] -= 1
	gdom = {}
	for i in kdomset:
		gdom[i] = {}
	for i in kdomset:
		kdomset[i] = bfsBounded(g, i, 2*k+1)[0]
		for j in kdomset:
			if j in kdomset[i] and kdomset[i][j] <= 2*k+1 and j != i:
				gdom[i][j] = kdomset[i][j]
				gdom[j][i] = kdomset[i][j]
	if len(kdomset) == 1:
		s = list(kdomset.keys())[0]
		proj = {}
		(f,d,r) = bfs(g, s)
		for i in g:
			proj[i] = d[i]
		distt = lambda x,y : proj[x] + proj[y]
		return({s:{}}, distt)
	el = prim(gdom)
	t = {}
	for i in range(len(el)):
		(e,w) = el[i]
		(x,y) = e
		if x not in t:
			t[x] = {}
		if y not in t:
			t[y] = {}
		d = kdomset[x][y]
		while d != 1:
			for z in g[y]:
				if kdomset[x][z] == d-1:
					u = z
					break
			if u not in t:
				t[u] = {y:1}
			else:
				t[u][y] = 1
			t[y][u] = 1
			y = u
			d -= 1
		t[y][x] = 1
		t[x][y] = 1
	i = randrange(len(kdomset))
	s = list(kdomset.keys())[i]
	father = bfs(t, s)[0]
	t = graphFromEdgelist(edgelistFromFather(father))
	children = {}
	for i in father:
		if father[i] != i:
			if father[i] not in children:
				children[father[i]] = {i:1}
			else:
				children[father[i]][i] = 1
	leaves = []
	for i in children:
		if len(children[i]) == 0 and i not in kdomset:
			leaves.append(i)
	while leaves != []:
		leaf = leaves[0]
		del leaves[0]
		for neigh in t[leaf]:
			del t[neigh][leaf]
		del t[leaf]
		dad = father[leaf]
		del children[dad][leaf]
		if len(children[dad]) == 0 and dad not in kdomset:
			leaves.append(dad)
	fin = time.time()
	#i = randrange(len(t))
	#s = list(t.keys())[i]
	#f = bfs(t, s)[0]
	#dt = distTree(f)
	#proj = {}
	#for i in g:
	#	proj[i] = firstInSet(g, i, t)
	#distt = lambda x,y : proj[x][1] + dt[min(proj[x][0],proj[y][0])][max(proj[x][0],proj[y][0])] + proj[y][1]
	return(t, fin-start,f)


def algoFgreedy(g,k):
	start=time.time()
	gk = {}
	gkdistance = {}

	for i in g:
		(gkdistance[i],gk[i]) = bfsBounded(g, i, k)

	covered = {}
	kdomset = {}
	neighsize = {}
	proj = {}
	t2 = {}
	for i in g:
		neighsize[i] = len(gk[i])

	while len(covered) != len(g):

		maxi = 0
		maxindex = -1
		for i in g:
			if i not in kdomset:

				if neighsize[i] > maxi:


					maxi = neighsize[i]
					maxindex = i
		kdomset[maxindex] = 1
		proj[maxindex] = (maxindex, 0)
		CovredJ = {}
		for j in gk[maxindex]:

			if j not in covered:
#---------------- 
				if gkdistance[maxindex][j] not in CovredJ:
					CovredJ[gkdistance[maxindex][j]]={j:1}
				else:
					CovredJ[gkdistance[maxindex][j]][j]=1

				covered[j] = 1


				for l in g:
					if j in gk[l]:
						neighsize[l] -= 1


		t2[maxindex]=[]
		for i in CovredJ:
			for q in range (i-1):

				t2[maxindex].append(0)
			for j in CovredJ[i]:
				if j!=maxindex:
					t2[maxindex].append(j)


	gdom = {}
	for i in kdomset:
		gdom[i] = {}
	for i in kdomset:
		kdomset[i] = bfsBounded(g, i, 2*k+1)[0]

		for j in kdomset:
			if j in kdomset[i] and kdomset[i][j] <= 2*k+1 and j != i:
				gdom[i][j] = kdomset[i][j]
				gdom[j][i] = kdomset[i][j]
	if len(kdomset) == 1:
		s = list(kdomset.keys())[0]
		proj = {}
		(f,d,r) = bfs(g, s)
		for i in g:
			proj[i] = d[i]
		distt = lambda x,y : proj[x] + proj[y]
		return({s:{}}, distt)

	el = prim(gdom)
	t = {}
	for i in range(len(el)):
		(e,w) = el[i]
		(x,y) = e
		if x not in t:
			t[x] = {}
		if y not in t:
			t[y] = {}
		d = kdomset[x][y]

		while d != 1:
			for z in g[y]:
				if kdomset[x][z] == d-1:
					u = z
#---------Remove u from t2
					#get the supernode of u
					for i in t2:
						if u in t2[i]:
							index=t2[i].index(u)

							del t2[i][index]

					break
			if u not in t:
				t[u] = {y:1}
			else:
				t[u][y] = 1
			t[y][u] = 1
			y = u
			d -= 1
		t[y][x] = 1
		t[x][y] = 1
	#i = randrange(len(kdomset))
	s = list(kdomset.keys())[1]
	father = bfs(t, s)[0]
	t = graphFromEdgelist(edgelistFromFather(father))


	children = {}
	for i in father:
		if father[i] != i:
			if father[i] not in children:
				children[father[i]] = {i:1}
			else:
				children[father[i]][i] = 1
	leaves = []
	for i in children:
		if len(children[i]) == 0 and i not in kdomset:
			leaves.append(i)

	while leaves != []:

		leaf = leaves[0]
		del leaves[0]
		for neigh in t[leaf]:
			del t[neigh][leaf]
		del t[leaf]
		dad = father[leaf]
		del children[dad][leaf]
		if len(children[dad]) == 0 and dad not in kdomset:
			leaves.append(dad)

	fin = time.time()
	#i = randrange(len(t))
	#s = list(t.keys())[i]
	#f = bfs(t, s)[0]
	#dt = distTree(f)
	#proj = {}
	#for i in g:
	#	proj[i] = firstInSet(g, i, t)
	#distt = lambda x,y : proj[x][1] + dt[min(proj[x][0],proj[y][0])][max(proj[x][0],proj[y][0])] + proj[y][1]
	return(t, fin-start,t2)