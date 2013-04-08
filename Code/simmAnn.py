from __future__ import division
from random import randint
from itertools import combinations
from shapely.validation import explain_validity
from shapely.geometry import Point,Polygon,MultiPolygon
from math import sqrt,sin,cos,pi,exp
from scipy.optimize import fmin_cobyla
from dijikstra import *
import pylab
import random
import itertools
import numpy as np
import time
x_max=10000
y_max=10000
percent_beacon=0.01
total_nodes=1000
node_range=100
Temprature=400.0
alpha=0.75
disp=50.0
beta=0.9
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


def Cost_function(correct_list,estimated_list):
	cost=0
	for node in correct_list:
		measured_distance=node_range  #can be improved
		estimated_node = estimated_list[correct_list.index(node)]
		neighbors=neighbor_dict[node]
		for neighbor in neighbors:
			if(neighbor not in beacon_list):
				estimated_neighbor = estimated_list[correct_list.index(neighbor)]
			else:
				estimated_neighbor=neighbor
			estimated_distance = cal_distance(estimated_node,estimated_neighbor)
			
			cost=cost+((measured_distance-estimated_distance)*(measured_distance-estimated_distance))
	
	return cost

def cal_distance(node1,node2):
	dis=(node1[0]-node2[0])*(node1[0]-node2[0])+(node1[1]-node2[1])*(node1[1]-node2[1])
	return sqrt(dis)

def displace_node(node,d):
	x=node[0]
	y=node[1]
	random_float=random.uniform(0,2*pi)
	return((x+d*cos(random_float)),(y+d*sin(random_float)))

complete_list=generateGrid(percent_beacon,total_nodes)
estimated_list=generateGrid(percent_beacon,total_nodes)[1] # estimated unknown co-ordinates
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

p=5
q=1

normal_nodes=len(normal_list)
beacon_nodes=len(beacon_list)
start_time=time.time()
neighbor_dict=oneHopNeighbor(normal_list+beacon_list,node_range)
displace_index=0
while(Temprature>1):
	CF_old=Cost_function(normal_list,estimated_list)
	new_estimated_list=estimated_list
	for j in range(0,int(q*normal_nodes/2)):
		displace_index=(displace_index+1)%normal_nodes
		for i in range(0,p):
			new_estimated_list[displace_index]=displace_node(new_estimated_list[displace_index],disp)
			CF_new=Cost_function(normal_list,new_estimated_list)
			if(CF_new < CF_old):
				#print "\n diff negative \n"				
				estimated_list=new_estimated_list
			else:
				diff_cf=CF_new-CF_old
				#print "diff "+str(diff_cf)
				prob=exp((-diff_cf)/float(Temprature))
				#print "prob: "+str(prob)
				if(random.uniform(0,1)<prob):
					estimated_list=new_estimated_list
	Temprature=alpha*Temprature
	print "Temprature: " +str(Temprature)
	disp=beta*disp
	#print "disp: " +str(disp)

error_x=0
error_y=0
for i in range(0,len(normal_list)):
        diff_x=estimated_list[i][0]-normal_list[i][0]
        diff_y=estimated_list[i][1]-normal_list[i][1]
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
print "hi"
files=open('result_simmAnn.txt','a')
files.write(str(node_range)+'    '+str(beacon_nodes)+'    '+str(normal_nodes)+'    '+str(x_max)+'    '+str(y_max)+'    '+str(avgerror_x)+'    '+str(avgerror_y)+'    '+str(average_time)+'\n')
files.close()
