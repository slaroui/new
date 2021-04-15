from distance import *
from math import *
import numpy as np

log2 = lambda x : log(x)/log(2)


# computes g[V(g)\subset]
# g is a dictionary of dictionaries of weights
# subset is an indicator dictionary
def complement(g, subset):  # O(|E(g)|)
	g2 = {}
	for u in g.keys():
		if subset[u] == 0:
			g2[u] = {}
			for v in g[u].keys():
				if subset[v] == 0:
					g2[u][v] = g[u][v]
	return(g2)


# computes g[V(l)]
# g is a dictionary of dictionaries of weights
# l is a list of vertices of g
def subgraph(g, l):
	indic = {}
	g2 = {}
	for i in g.keys():
		indic[i] = 0
	for i in l:
		indic[i] = 1
	for i in g.keys():
		if indic[i] == 1:
			g2[i] = {}
			for j in g[i].keys():
				if indic[j] == 1:
					g2[i][j] = g[i][j]
	return(g2)


# g is a dictionary of dictionaries of weights
# rad = R
# p = P_{x0t}, a list from x_0 to t
# d is the dictionary of d_X(x0, _)
# n = |X|
# m = |E(X)|
def create_petal(g, x0, t, rad, px0t, d, n, m): # O(|E(g)| log(log(|V(g)|)) + |V(g)|^2)
	l	= ceil(log2(log2(n)))
	gtilde = {}
	for u in g.keys():
		gtilde[u] = {}
		for v in g[u].keys():
			gtilde[u][v] = g[u][v] + d[u] - d[v]
	i = 1
	while d[t] - d[px0t[-i-1]] <= rad:
		gtilde[px0t[-i]][px0t[-i-1]] /= 2
		gtilde[px0t[-i-1]][px0t[-i]] /= 2
		i += 1
	dist = dijkstraBounded(gtilde, t, (1+1/l)*rad/2)[0]
	p = 1
	r = (1+1/l)*rad/4
	oldr = rad/4
	cpt = 0
	for u in gtilde.keys():
		if dist[u] <= r:
			for v in gtilde[u].keys():
				if dist[v] <= r:
					cpt += 1
	nbrEdges = cpt/2
	while (nbrEdges > 2*m/pow(2,pow(log2(m),1-p/l))):
		p += 1
		oldr = r
		r = (1+p/l)*rad/4
		oldNbrEdges = nbrEdges
		if(floor(2*oldr) < floor(2*r)):
			cpt = 0
			for u in gtilde.keys():
				if dist[u] > oldr and dist[u] <= r:
					for v in gtilde[u].keys():
						if dist[v] <= oldr:
							cpt += 2
						elif dist[v] <= r:
							cpt += 1
			nbrEdges += cpt/2
	a = floor(2*oldr)/2 # Warning, this is half of the a of the algorithm
	if p == 1:
		cpt = 0
		for u in gtilde.keys():
			if dist[u] <= oldr:
				for v in gtilde[u].keys():
					if dist[v] <= oldr:
						cpt += 1
		oldNbrEdges = cpt/2
	if oldNbrEdges != 0:
		lnchi = 64*log(2)*log(m/oldNbrEdges)
	else:
		lnchi = 64*log(2)*log(m)
		print("Be careful, could have divided by 0!")
		print(r)
	r = a
	cpt = 0
	for u in gtilde.keys():
		if dist[u] <= r:
			for v in gtilde[u].keys():
				if dist[v] > r:
					cpt += 1
	border = cpt
	while (border >= nbrEdges*l*lnchi/(8*log(2)*rad)):
		r += 0.5
		cpt1 = 0 # for edges of E(W_r)
		cpt2 = 0 # for edges of \partial(W_r)
		for u in gtilde.keys():
			if dist[u] > r-0.5 and dist[u] <= r:
				for v in gtilde[u].keys():
					if dist[v] <= r-0.5:
						cpt1 += 2
					elif dist[v] <= r:
						cpt1 += 1
			if dist[u] > r:
				for v in gtilde[u].keys():
					if dist[v] <= r:
						cpt2 += 1
		nbrEdges += cpt1/2
		border += cpt2
	inwr = {}
	for i in gtilde.keys():
		if dist[i] <= r:
			inwr[i] = 1
		else:
			inwr[i] = 0
	i = -1
	while dist[px0t[i]] <= r:
		i -= 1
	return(inwr, px0t[i+1], px0t[i])
	# returns an indicator dictionary and two vertices



# g: dictionary of dictionaries of weights
# father: dictionary giving the father in the BFS tree
# dist: dictionary of distances to x0
# ecc: eccentricity of x0
# next: name of the next vertex to add
def petal_decomposition(g, x0, t, father, dist, ecc, next):
	m = 0
	for i in g.keys():
		m += len(g[i])
	m = m/2
	r0 = ceil(ecc/2)
	xsets = []
	xnodes = []
	ynodes = []
	tnodes = []
	j = 2
	if dist[t] < r0:
		g[t][next] = 1
		g[next] = {t:1}
		l = r0 - dist[t] # not well-defined: l may not be an integer
		dist[next] = dist[t]+1
		father[next] = t
		px0t1p = [next]
		next += 1
		for i in range(1, ceil(l)): # addition of l-1 new vertices
			g[next] = {}
			father[next] = next-1
			if i < ceil(l)-1:
				g[next-1][next] = 1
				g[next][next-1] = 1
				dist[next] = dist[t]+i+1
			else:
				g[next-1][next] = l+1-ceil(l)
				g[next][next-1] = l+1-ceil(l)
				dist[next] = dist[t]+i+l+1-ceil(l)
			px0t1p.append(next)
			next += 1
		t1 = next-1
		t1p = t1
	else:
		t1 = t
		t1p = t
		while dist[t1p] > r0:
			t1p = father[t1p]
		px0t1p = []
	u = t
	tnodes.append(t1)
	while u != x0:
		px0t1p.insert(0, u)
		u = father[u]
	px0t1p.insert(0, x0)
	(x1set, x1node, y1node) = create_petal(g, x0, t1p, ecc/4, px0t1p, dist, len(g), m)
	xnodes.append(x1node)
	ynodes.append(y1node)
	g2 = complement(g, x1set)
	for u in list(x1set.keys()):
		if x1set[u] == 0:
			del x1set[u]
	xsets.append(list(x1set.keys()))
	empty = False
	while not empty:
		empty = True
		radius = 2*r0
		for i in g2.keys():
			if dist[i] >= r0 and dist[i] < radius:
				radius = dist[i]
				u = i
		if radius < 2*r0:
			empty = False
			tj = u
			tnodes.append(tj)
			px0tj = []
			cur = tj
			while cur != x0:
				px0tj.insert(0, cur)
				cur = father[cur]
			px0tj.insert(0, x0)
			(xjset, xjnode, yjnode) = create_petal(g2, x0, tj, ecc/8, px0tj, dist, len(g), m)
			xnodes.append(xjnode)
			ynodes.append(yjnode)
			g2 = complement(g2, xjset)
			for u in list(xjset.keys()):
				if xjset[u] == 0:
					del xjset[u]
			xsets.append(list(xjset.keys()))
			j += 1
	s = j-1
	xsets.insert(0, list(g2.keys()))
	xnodes.insert(0, -1)  # fake value
	ynodes.insert(0, -1)  # fake value
	tnodes.insert(0, ynodes[1])
	edges = []
	for i in range(1, s+1):
		edges.append((xnodes[i], ynodes[i]))
	return(xsets, edges, tnodes, next)



# g dictionary of dictinaries of weights
# next: name of the next vertex to add
def hierarchical_petal_decomposition(g, x0, t, next):
	n = len(g)
	(father, dist, ecc) = dijkstra(g, x0)
	if ecc <= 8 or ecc <= 2*log2(n)*log2(log2(n)):
		tree = []
		for i in father.keys():
			if father[i] != i:
				tree.append((i, father[i]))
		return(tree)
	else:
		(xsets, edges, tnodes, next) = petal_decomposition(g, x0, t, father, dist, ecc, next)
		tree = edges
		for j in range(len(xsets)):
			cur = tnodes[j]
			if j == 0:
				xj = x0
			else:
				xj = edges[j-1][0]
			while cur != xj:
				f = father[cur]
				g[f][cur] = 0.5
				g[cur][f] = 0.5
				cur = f
			if j == 0:
				treej = hierarchical_petal_decomposition(subgraph(g, xsets[0]), x0, tnodes[0], next)
			else:
				treej = hierarchical_petal_decomposition(subgraph(g, xsets[j]), edges[j-1][0], tnodes[j], next)
			tree += treej
		return(tree)


# g dictionary of dictionaries
# vertices must be 0, 1, ..., n-1
def decomposition(g, x0):
	n = len(g)
	tree = hierarchical_petal_decomposition(g, x0, x0, n)
	tree2 = []
	for i in range(len(tree)):
		if tree[i][0] <= n and tree[i][1] <= n:
			tree2.append(tree[i])
	return(tree2)


