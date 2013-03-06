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
x_max=1000
y_max=1000
percent_beacon=0.3
total_nodes=1000
node_range=50

def mod(x):
        if (x>0):
                return x
        else:
                return (-x)

def generateGrid(percent_beacon,total_nodes):
        beacon_nodes=int(percent_beacon * total_nodes)
        normal_nodes=total_nodes - beacon_nodes
        beacon_list=[]
        normal_list=[]
        total_list_x=random.sample(range(x_max),total_nodes)
        total_list_y=random.sample(range(y_max),total_nodes)
        for i in range(0,beacon_nodes):
                beacon_list.append((total_list_x[i],total_list_y[i]))
        for i in range(beacon_nodes,total_nodes):
                normal_list.append((total_list_x[i],total_list_y[i]))
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
start_time=time.time()
neighbor_dict=oneHopNeighbor(normal_list+beacon_list,node_range)
final_coordinates=dict()
for beacon in beacon_list:
        final_coordinates[beacon]=beacon

def averageNeighbors(neighbors):
        sum_x=0
        sum_y=0
        if (len(neighbors)>0):
                for neighbor in neighbors:
                       (x,y)=final_coordinates.setdefault(neighbor,(0,0))
                       sum_x=sum_x+x
                       sum_y=sum_y+y
                return (sum_x/len(neighbors),sum_y/len(neighbors))
        else: 
                return (0,0)

old_x=0
new_x=x_max+1
flag=1000
for normal_node in normal_list:
        while(flag):
                neighbors=neighbor_dict[normal_node]
                (new_x,new_y)=averageNeighbors(neighbors)
                #print new_x
                old_x=new_x
                final_coordinates[normal_node]=(new_x,new_y)
                flag=flag-1
        flag=1000
        #print "Done"                

error_x=0
error_y=0
for normal_node in normal_list:
        (x,y)=final_coordinates[normal_node]
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
files=open('result_diffusion.txt','a')
files.write(str(node_range)+'    '+str(beacon_nodes)+'    '+str(normal_nodes)+'    '+str(x_max)+'    '+str(y_max)+'    '+str(avgerror_x)+'    '+str(avgerror_y)+'    '+str(average_time)+'\n')
files.close()
