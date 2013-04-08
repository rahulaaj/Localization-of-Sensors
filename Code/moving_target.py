from random import randint,uniform
from itertools import combinations
from shapely.validation import explain_validity
from shapely.geometry import Point,Polygon,MultiPolygon
from math import sqrt
from math import sin, cos, pi,radians
import random
import itertools
import numpy as np
import time
x_max=5000
y_max=5000
total_nodes=500
node_range=100
percentage_beacon=0.5
walk_length=x_max/2
def random_coordinate():
        return (randint(x_max,y_max),randint(x_max,y_max))

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

def point_inside_polygon(x,y,poly):
    n = len(poly)
    inside =False
    px,py = poly[0]
    for i in range(n+1):
        p_x,p_y = poly[i % n]
        if y > min(py,p_y):
            if y <= max(py,p_y):
                if x <= max(px,p_x):
                    if py != p_y:
                        inter_x = (y-py)*(p_x-px)/(p_y-py)+px
                    if px == p_x or x <= inter_x:
                        inside = not inside
        px,py = p_x,p_y
    return inside

def findIntersect(inside_set):
        if (len(inside_set)==0):
                print "single" 
                return [(0,0),(x_max,0),(x_max,y_max),(0,y_max),(0,0)]
        elif (len(inside_set)==1):
                p1=Polygon(inside_set[0])
                return list(p1.exterior.coords)
        elif (len(inside_set)==2):
                p1=Polygon(inside_set[0])
                p2=Polygon(inside_set[1])
                return list(p1.intersection(p2).exterior.coords)
        else:
                p1=Polygon(inside_set[0])
                p2=Polygon(inside_set[1])
                a=inside_set.pop(0)
                b=inside_set.pop(0)
                inside_set.insert(0,list(p1.intersection(p2).exterior.coords))
                return findIntersect(inside_set)

def distance_d((x,y),d):
        while(1):
                angle=uniform(0,360)
                rangle=radians(angle)
                x_new=x+(d*cos(rangle))
                y_new=y+(d*cos(rangle))
                if(0<x_new<x_max and 0<y_new<y_max):
                        return (x_new,y_new)




def super_imposed(rectangle,i,j):
	temp=[]
	for (x,y) in rectangle:
		temp.append((x-(i*node_range),y-(j*node_range)))
		
	return temp
                
def all_rectangles(beacon_list):
        rectangle_list=[]
        for (x,y) in beacon_list:
                temp=[]
                temp.append((x-node_range,y-node_range))
                temp.append((x+node_range,y-node_range))
                temp.append((x+node_range,y+node_range))
                temp.append((x-node_range,y+node_range))
                rectangle_list.append(temp)
        return rectangle_list
        

complete_list=generateGrid(percentage_beacon,total_nodes)
normal_list=complete_list[1]    #unknown co-ordinates
beacon_list=complete_list[0]
normal_nodes=len(normal_list)
beacon_nodes=len(beacon_list)
error_x=0
error_y=0
error_x2=0
error_y2=0
start_time=time.time()
#walk_list=walk(num_iter)

#print walk_list
rectangle_list=all_rectangles(beacon_list)
#print rectangle_list
big_box=[(0,0),(x_max,0),(x_max,y_max),(0,y_max)]
for normal_node in normal_list:
		print str(normal_node)
		inside_set=[big_box]
		for i in range(1-(x_max/(4*node_range)),x_max/(4*node_range)):
			for rectangle in rectangle_list:
				if (point_inside_polygon(normal_node[0]+i*node_range,normal_node[1],rectangle)):
					inside_set.append(super_imposed(rectangle,i,0))
				if (point_inside_polygon(normal_node[0],normal_node[1]+i*node_range,rectangle)):
					inside_set.append(super_imposed(rectangle,0,i))
        
		common_region=findIntersect(inside_set)
		p1=Polygon(common_region)
		centroid=list(p1.centroid.coords)
		diff_x=centroid[0][0]-normal_node[0]
		diff_y=centroid[0][1]-normal_node[1]
		error_x=error_x+mod(diff_x)            
		error_x2=error_x2+diff_x*diff_x            
		error_y=error_y+mod(diff_y)
		error_y2=error_y2+diff_y*diff_y
        #print "\nActual Location\n"
        #print normal_node
        #print "\nEstimated Location\n"
        #print centroid
program_time=time.time() - start_time
average_time=program_time/normal_nodes
avgerror_x=(error_x)/normal_nodes
avgerror_y=(error_y)/normal_nodes
print "Average error in x-coordinate"
print avgerror_x
print "Average error in y-coordinate"
print avgerror_y
print "Average time for each node"
print average_time
avgstd=sqrt(error_x2+error_y2)/(2*normal_nodes)
files=open('result_moving_target.txt','a')
files.write(str(node_range)+'    '+str(beacon_nodes)+'    '+str(normal_nodes)+'    '+str(x_max)+'    '+str(y_max)+'    '+str(avgerror_x)+'    '+str(avgerror_y)+'    '+str(average_time)+'    '+str(avgstd)+'\n')
files.close()
