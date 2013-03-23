from __future__ import division
from random import randint
from itertools import combinations
from shapely.validation import explain_validity
from shapely.geometry import Point,Polygon,MultiPolygon
from math import sqrt
from scipy.optimize import fmin_cobyla
from dijikstra import *
import pylab
import random
import itertools
import numpy as np
import time
x_max=10000
y_max=10000
percent_beacon=0.3
total_nodes=5000
node_range=200

def mod(x):
        if (x>0):
                return x
        else:
                return (-x)

def generateGrid(percent_beacon,total_nodes):
        beacon_nodes=int(percent_beacon * total_nodes)
        beacon_list=[]
        normal_list=[]
        sqrt_beacon_nodes=int(sqrt(beacon_nodes))
        spaced_list=list(np.linspace(0,x_max,sqrt_beacon_nodes))
        beacon_list=[(int(x),int(y)) for (x,y) in list(itertools.product(spaced_list,spaced_list))]
        beacon_nodes=len(beacon_list)
        normal_nodes=total_nodes - beacon_nodes
        normal_list_x=random.sample(range(x_max),normal_nodes)
        normal_list_y=random.sample(range(y_max),normal_nodes)
        for i in range(0,normal_nodes):
                normal_list.append((normal_list_x[i],normal_list_y[i]))
        complete_list=[]
        complete_list.append(beacon_list)
        complete_list.append(normal_list)
        return complete_list

def oneHopNeighbor(nodes,sigRange):
	hopNeighbor={}
	nodes.sort()
	j=1
	nodeLen=len(nodes)
	for (p,q) in nodes:
		neighbor=[]
		low=j-sigRange
		high=j+sigRange
		if low <= 0:
			low=1
		if high > nodeLen:
			high = nodeLen
		for a in range(low,high+1):
			(x,y)=nodes[a-1]
			dis=(p-x)*(p-x) + (q-y)*(q-y)
			if (( dis <= sigRange*sigRange) and dis != 0):
				neighbor.append((x,y))
		hopNeighbor[(p,q)]=neighbor
		j=j+1
	return hopNeighbor

complete_list=generateGrid(percent_beacon,total_nodes)
beacon_list=complete_list[0]    #known co-ordinates
#print beacon_list
#files=open('beacon.txt','w')
#files.write(str(beacon_list))
#files.close()
normal_list=complete_list[1]    #unknown co-ordinates
#files=open('normal.txt','w')
#files.write(str(normal_list))
#files.close()
#print normal_list
normal_nodes=len(normal_list)
beacon_nodes=len(beacon_list)
start_time=time.time()
hop_dict=dict()
neighbor_dict=oneHopNeighbor(normal_list+beacon_list,node_range)
"""
def send_gradientNeighbor(node,i,value):
#        neighbors=neighbor_dict(node)
#        for nodes in neighbors:
        if(hop_dict.setdefault((node,i),0)> value+1 or hop_dict.setdefault((node,i),0)==0):
                hop_dict[(node,i)]=value+1

def send_gradient(i):
        not_send=normal_list
        not_send.remove(beacon_list[i])
        neighbors=neighbor_dict(beacon_list[i])
        sender=beacon_list[i]
        value=0
        while(sender in not_send):
                for elem in neighbors:
                       send_gradientNeighbor(node,i,value) 
                value=value+1
"""
def send_gradient(i):
        graph=dict()
        new_list=normal_list+beacon_list
        for node in new_list:
                temp={}
                neighbors=neighbor_dict[node]
                for neighbor in neighbors:
                        temp[neighbor]=1
                graph[node]=temp
        (distances,predecessors)=Dijkstra(graph,beacon_list[i],None)
        for key in distances:
                hop_dict[(key,i)]=distances[key]
        
def error_min(beacon_distance):
        if (len(beacon_distance)==0):
                return (x_max/2,y_max/2)
        sum_xi=0
        sum_yi=0
        sum_xisq=0
        sum_yisq=0
        sum_disq=0
        length=len(beacon_distance)
        for (i,distance) in beacon_distance:
                sum_xi=sum_xi+beacon_list[i][0]
                sum_yi=sum_yi+beacon_list[i][1]
                sum_xisq=sum_xisq+beacon_list[i][0]*beacon_list[i][0]
                sum_yisq=sum_yisq+beacon_list[i][1]*beacon_list[i][1]
                sum_disq=sum_disq+distance*distance        
        else:
                error=lambda x: mod(length*x[0]*x[0]+length*x[1]*x[1]-2*x[0]*sum_xi-2*x[1]*sum_yi+sum_xisq+sum_yisq-sum_disq)
                constrx=lambda x: x[0]
                constry=lambda x: x[1]
                coord_list=list(fmin_cobyla(error,[0,0],[constrx,constry],rhobeg=10,rhoend=1,maxfun=100000))
                return (coord_list[0],coord_list[1])
        
def find_min(normal_node):
        beacon_distance=[]
        for i in range(0,len(beacon_list)):
                if(hop_dict.setdefault((normal_node,i),0)!=0):
                        beacon_distance.append((i,(node_range*hop_dict[(normal_node,i)])/2))
        (x,y)=error_min(beacon_distance)
        return (x,y) 

for i in range(0,len(beacon_list)):
        #print i
        send_gradient(i)

error_x=0
error_y=0
for normal_node in normal_list:
        (x,y)=find_min(normal_node)
        diff_x=x-normal_node[0]
        diff_y=y-normal_node[1]
        error_x=error_x+mod(diff_x)            
        error_y=error_y+mod(diff_y)
        #print "\nActual Location\n"
        #print normal_node
        #print "\nEstimated Location\n"
        #print (x,y)
program_time=time.time() - start_time
average_time=program_time/normal_nodes
avgerror_x=(error_x)/normal_nodes
avgerror_y=(error_y)/normal_nodes
print "Average error in x-coordinate"
print avgerror_x
print "Average error in y-coordinate"
print avgerror_y
print "Average time required"
print average_time
files=open('result_gradient.txt','a')
files.write(str(node_range)+'    '+str(beacon_nodes)+'    '+str(normal_nodes)+'    '+str(x_max)+'    '+str(y_max)+'    '+str(avgerror_x)+'    '+str(avgerror_y)+'    '+str(average_time)+'\n')
files.close()
