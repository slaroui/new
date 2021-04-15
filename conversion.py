from randomGraphs import *

def edgelistFromFather(father):
	l = []
	for i in father.keys():
		if father[i] != i:
			l.append((father[i], i))
	return(l)

def graphFromEdgelist(edgelist):
	g = {}
	for e in edgelist:
		(u,v) = e
		if u in g:
			g[u][v] = 1
		else:
			g[u] = {v:1}
		if v in g:
			g[v][u] = 1
		else:
			g[v] = {u:1}
	return(g)

# rename the vertices of g such that they become 0, 1, ..., n-1
def rename(g):
	n = len(g)
	cor = {}
	cor2 = {}
	j = 0
	l = mixlist(list(g.keys()))
	for i in l:
		cor[i] = j
		cor2[j] = i
		j += 1
	g2 = {}
	for i in g.keys():
		g2[cor[i]] = {}
		for j in g[i].keys():
			g2[cor[i]][cor[j]] = 1
	return(g2, cor2)


