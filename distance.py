from math import *
from randomGraphs import *

def bfs(g, s):
	father = {}
	dist = {}
	toVisit = [s]
	seen = {s:1}
	dist[s] = 0
	father[s] = s
	while toVisit != []:
		current = toVisit[0]
		del toVisit[0]
		l = list(g[current].keys())
		l2 = mixlist(l)
		for neigh in l2:
			if neigh not in seen:
				dist[neigh] = dist[current] + 1
				father[neigh] = current
				toVisit.append(neigh)
				seen[neigh] = 1
	return(father, dist, dist[current])



# g dictionary of dictionaries of weights
# s source of shortest paths
def dijkstra(g, s):
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
		visited[current] = 1
		del toVisit[current]
	return(father, dist, dist[current])


def bfsBounded(g, s, rmax):
	n = len(g)
	dist = {}
	toVisit = [s]
	seen = {s:1}
	visited = {}
	dist[s] = 0
	while toVisit != [] and dist[toVisit[0]] <= rmax:
		current = toVisit[0]
		del toVisit[0]
		for neigh in g[current]:
			if neigh not in seen:
				dist[neigh] = dist[current] + 1
				toVisit.append(neigh)
				seen[neigh] = 1
		visited[current] = 1
	return(dist, visited)



# g : dictionary of dictionaries of weights
# s : source of shortest paths
# rmax : radius to reach
def dijkstraBounded(g, s, rmax):  # O(|V(g)|^2)
	n = len(g)
	dist = {}
	toVisit = {s:1}
	visited = {}
	for i in g:
		dist[i] = 2*n
	dist[s] = 0
	mindist = 0
	while mindist <= rmax:
		mindist = rmax + 0.1
		for i in toVisit:
			if i not in visited and dist[i] < mindist:
				current = i
				mindist = dist[i]
		if mindist <= rmax:
			for neigh in g[current]:
				if dist[current] + g[current][neigh] < dist[neigh]:
					dist[neigh] = dist[current] + g[current][neigh]
					toVisit[neigh] = 1
			visited[current] = 1
			del toVisit[current]
	return(dist, visited)



# g dictionary of dictionaries
# returns whether the induced subgraph g[V(t-x)] is connected
def isConnected(g, t, x):
	l = list(t.keys())
	neighbs = {}
	for i in g[x]:
		if i in t:
			neighbs[i] = 1
	first = list(neighbs.keys())[0]
	toVisit = [first]
	del neighbs[first]
	seen = {x:1, first:1}
	while neighbs != {} and toVisit != []:
		current = toVisit[0]
		del toVisit[0]
		for neigh in g[current]:
			if neigh not in seen and neigh in t:
				seen[neigh] = 1
				toVisit.append(neigh)
				if neigh in neighbs:
					del neighbs[neigh]
	return(neighbs == {})


# list of nodes of the connected component of s in t
def connectedComponent(t, s):
	toVisit = {s:1}
	visited = {}
	while toVisit != {}:
		current = list(toVisit.keys())[0]
		for neigh in t[current]:
			if neigh not in visited:
				toVisit[neigh] = 1
		del toVisit[current]
		visited[current] = 1
	return(list(visited.keys()))


# returns the list of the sizes of the connected components of the graph with a list of members of each
def sizeCC(g):
	visited = {}
	compo = []
	sources = []
	source = 0
	finished = False
	while not finished:
		(f, d, r) = bfs(g, source)
		sources.append(source)
		if i in dist:
			visited[i] = 1
		finished = True
		for i in g:
			if i not in visited:
				finished = False
				source = i
				break
		compo.append(len(dist))
	return(compo, sources)


# returns the list of the sizes of the connected components of the graph with a list of members of each
def maxCC(g):
	visited = {}
	maxi = 0
	sourcemax = 0
	source = 0
	finished = False
	while not finished:
		(f, d, r) = bfs(g, source)
		if len(d) > maxi:
			maxi = len(d)
			sourcemax = source
		for i in d:
			visited[i] = 1
		finished = True
		for i in g:
			if i not in visited:
				finished = False
				source = i
				break
	(f,d,r) = bfs(g, sourcemax)
	l = list(g.keys())
	for i in l:
		if i not in d:
			del g[i]
	return(g)



# returns the first element of t met in a bfs from x
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
	

# returns a minimum spanning tree of a weighted graph g
def prim(g):
	s = list(g.keys())[0]
	t = {s:1}
	edgelist = []
	sortedges = []
	while len(t) != len(g):
		l = []
		for i in g[s]:
			if i not in t:
				l.append(((s,i),g[s][i]))

		f = lambda x : x[1]
		l.sort(key = f)
		i = 0
		j = 0
		while j != len(l):
			if i == len(sortedges) or f(l[j]) < f(sortedges[i]):
				sortedges.insert(i, l[j])
				j += 1
			i += 1

		(e,w) = sortedges[0]

		del sortedges[0]
		(x,y) = e
		while x in t and y in t:
			(e,w) = sortedges[0]
			del sortedges[0]
			(x,y) = e	
		if x not in t:
			s = x
		else:
			s = y
		t[s] = 1
		edgelist.append((e,w))
	return(edgelist)


# renvoie d matrice de distances
def allPairDists(g):
	d = {}
	for i in g:
		d[i] = bfs(g, i)[1]
	return(d)


# computes all-pair distances in a rooted tree represented by father
def distTree(father):
	d = {}
	for x in father:
		d[x] = {}
		for y in father:
			if x <= y:
				lx = [x]
				a = x
				while father[a] != a:
					lx.append(father[a])
					a = father[a]
				ly = [y]
				b = y
				while father[b] != b:
					ly.append(father[b])
					b = father[b]
				i = 1
				while i <= len(lx) and i <= len(ly) and lx[-i] == ly[-i]:
					i += 1
				d[x][y] = len(lx)+len(ly)-2*i+2
	return(d)

# computes the average distortion
def avgdistor(g, distg, distt):
	c = 0
	s = 0
	for i in g:
		for j in g:
			if i < j:
				s += distt(i,j)/distg(i,j)
				c += 1
	return(s/c)

# computes the average stretch
def avgstretch(g, distg, distt):
	c = 0
	s = 0
	for i in g:
		for j in g[i]:
			if i < j:
				s += distt(i,j)/distg(i,j)
				c += 1
	return(s/c)
	

def iskdom(g, t, k): # tests whether t is a k-dominating subtree of g
	booleen = True
	for i in g:
		v = bfsBounded(g, i, k)[1]
		booleen = False
		for j in v:
			if j in t:
				booleen = True
				break
		if not booleen:
			break
	return(booleen)


