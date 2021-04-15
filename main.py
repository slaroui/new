from randomGraphs import *
from conversion import *
from algorithms import *
from pruning2test import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
import pickle
# g = Grille l x l
#l = 50
#g = {}
#for i in range(l*l):
#	g[i] = {}
#for i in range(l):
#	for j in range(l):
#		if i != 0:
#			g[l*i+j][l*(i-1)+j] = 1
#		if i != l-1:
#			g[l*i+j][l*(i+1)+j] = 1
#		if j != 0:
#			g[l*i+j][l*i+j-1] = 1
#		if j != l-1:
#			g[l*i+j][l*i+j+1] = 1

algos = [algoEdirprun]
letters = ["algoEdirprun"]
klist=[1]
graphs=["road-usroads-48"]



#dg = allPairDists(g)
#distg = lambda x,y : dg[x][y]

#		def circle(x,y,r):
#			theta = np.linspace(0, 2*np.pi, 100)
#			a = r*np.cos(theta)+x
#			b = r*np.sin(theta)+y
#			plt.plot(a, b, color="green")
	



for k in klist:
    for gr in graphs:
        g = pickle.load( open( "RandomPaires/"+gr+".p", "rb" ) )
        outedges=pickle.load( open( "RandomPaires/"+gr+"100.p", "rb" ) )
        for i in range(1):

            if letters[i]=="algoAbfs" or letters[i]=="algoBpetal" or letters[i]=="algoCrst":
                (t, time,father,t1) = algos[i](g, k)
                Total=0
                for m in t:
                    Total=Total+len (t[m])
                (RE,RE0,TimeRE,TimeG)=RelativeE(g,t,t1,outedges)
                f = open("Results/Result"+letters[i]+str(gr)+str(k)+".txt", "a")
                f.write("algo: "+letters[i]+"\n")
                f.write("graph: "+str(gr)+"\n")
                f.write("K: "+str(k)+"\n")
                f.write("str(t)"+ str( len(t))+"\n")
                f.write("NB edge:"+ str( Total/2)+"\n")
                f.write("Time compression: "+ str(time)+"\n")
                f.write("Relative Err*2k: "+ str(RE)+"\n")
                f.write("Relative Err0: "+ str(RE0)+"\n")
                f.write("Time after compression: "+ str(TimeRE)+"\n")
                f.write("Time in G: "+ str(TimeG)+"\n")

                f.close()
                pickle.dump( t, open( "ResultFev/t_"+letters[i]+str(gr)+str(k)+".p", "wb" ) )
                                #pickle.dump( t1, open( "pEcro3.p", "wb" ) )
                pickle.dump( father, open( "ResultFev/Father_"+letters[i]+str(gr)+str(k)+".p", "wb" ) )
                pickle.dump( t1, open( "ResultFev/SN_"+letters[i]+str(gr)+str(k)+".p", "wb" ) )

            else:
                (t, time) = algos[i](g, k)
                Total=0
                #or m in t:
                #    Total=Total+len (t[m])
                #(RE,RE0,TimeRE,TimeG)=RelativeE(g,t,t1,outedges)
                f = open("Results/Result"+letters[i]+str(gr)+str(k)+".txt", "a")
                f.write("algo: "+letters[i]+"\n")
                f.write("graph: "+str(gr)+"\n")
                f.write("K: "+str(k)+"\n")
                f.write("str(t)"+ str( len(t))+"\n")

                f.close()
