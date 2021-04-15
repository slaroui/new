# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:08:42 2021

@author: Souwi
"""
import timeit
from random import *
from conversion import *
from petalDec import *
from pruning import *
from randomGraphs import *
import pickle
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

def bfs1(g, s,d):

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


def RelativeE(g,t,t2,outedges):




#Relative error our methods
#with refining

	DtR0=[]
	DtWR=[]
	RER=0

	RER0=0


#Distance Graph
	Dg1=[]
	startG=timeit.default_timer()
	for e in outedges:

		Dg1.append(bfs1(g, e[0],e[1]))

	finG=timeit.default_timer()




#distance Tree
	startT=timeit.default_timer()

	for e in outedges:
		distTotal=0
		distTotal0=0
		index=-1
		if e[0] in t and e[1] in t:
			distTotal= bfs1(t,e[0],e[1])
			DtWR.append(distTotal)
			DtR0.append(distTotal)
		elif e[0] in t and e[1] not in t:
# get the supernode of e1 then apply bfs1 from supernode to e0
			sy = -1
			while  sy == -1:
			#get  super  nodes
				for i in t2:
					if (e[1] in t2[i]):
						sy=i
# get index of e1 in the super node

			index= t2[sy].index(e[1])

#get the occ of 0 before e1
			occ=0
			dist=0
			occ=t2[sy][0:index].count(0)
			dist= occ+1

#bfs1 between sy and e0
			distTotal=bfs1(t,sy,e[0])+ dist
			DtWR.append(distTotal)
			DtR0.append(distTotal)
		elif e[1] in t and e[0] not in t:
# get the supernode of e1 then apply bfs1 from supernode to e0
			sx = -1
			while  sx == -1:
	#get  super  nodes
				for i in t2:
					if (e[0] in t2[i]):
						sx=i
# get index of e1 in the super node

			index= t2[sx].index(e[0])

#get the occ of 0 before e0
			occ=0
			dist=0
			occ=t2[sx][0:index].count(0)
			dist= occ+1
#bfs1 between sx and e1
			distTotal= dist+ bfs1(t,sx,e[1])
			DtWR.append(distTotal)
			DtR0.append(distTotal)
		else:
# get the supernode of e0 and e1 then apply bfs1 between supernodes 

			sx = -1 
			sy = -1
			while sx== -1 and sy == -1:
			#get Nb super  nodes
				for i in t2:
					if (e[0] in t2[i]):
						sx=i
					if (e[1] in t2[i]):
						sy=i
			indexX=0
			indexY=0

			dist=0
			if (sx == sy): # same supernode
				indexX= t2[sx].index(e[0])
				indexY= t2[sy].index(e[1])

				occX=t2[sx][0:indexX].count(0)
				occY=t2[sy][0:indexY].count(0)
				if (occX==0 and occY==0):
					distTotal=2
					DtWR.append(distTotal)
					DtR0.append(distTotal)
				else:
					distTotal= max (2*occX+1, 2*occY+1)
					DtWR.append(distTotal)
					DtR0.append(0)
			else:# not the same supernode
				dist1=0
				indexX= t2[sx].index(e[0])
				occX=t2[sx][0:indexX].count(0)
				dist= occX+1
				indexY= t2[sy].index(e[1])
				occY=t2[sy][0:indexY].count(0)
				dist1= occY+1
				distTotal=dist+bfs1(t,sx,sy)+dist1
				DtWR.append(distTotal)
				DtR0.append(distTotal)


	finT=timeit.default_timer()

#Relative Error
	for i in range (100):

		RER= RER+((abs(Dg1[i]- DtWR[i]))/Dg1[i])
#Relative Error
	for i in range (100):

		RER0= RER0+((abs(Dg1[i]- DtR0[i]))/Dg1[i])
	return(RER/100,RER0/100,finT-startT,finG-startG)


"""

graphs=["ia-reality","musae_crocodile_edges","musae_facebook_edges","ca-HepPh"]
outedges=["ia-reality1000","musae_crocodile_edges1000","musae_facebook_edges1000","ca-HepPh1000"]
letters = ["algoAbfs", "algoBpetal", "algoCrst", "algoEdirprun", "algoFgreedy"]

for gr in graphs:
    outedges=pickle.load( open( "RandomPaires/"+gr+"1000.p", "rb" ) )
    g=pickle.load( open( "RandomPaires/"+gr+".p", "rb" ) )

    for i in range(5):
        t=pickle.load(open( "ResultFev/t_"+letters[i]+str(gr)+"3.p", "rb" ) )
        t1=pickle.load( open("ResultFev/SN_"+letters[i]+str(gr)+"3.p", "rb" ) )
        (RE,RE0,TimeRE,TimeG)=RelativeE(g,t,t1,outedges)
        f = open("Res1000/Result"+letters[i]+str(gr)+"3.txt", "a")
        f.write("algo: "+letters[i]+gr+"\n")
        f.write("graph: "+str(gr)+"\n")
        f.write("RE: "+str(RE)+"\n")
        f.write("RE0: "+str(RE0)+"\n")
        f.write("TimeRE: "+str(TimeRE)+"\n")
        f.write("TimeG: "+str(TimeG)+"\n")
        f.close()
        print ("Fin: "+letters[i]+" Graph: "+str(gr))"""