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
x_max=10000
y_max=10000
total_nodes=1000
node_range=100
num_iter=1000*10

def random_coordinate():
        return (randint(x_max,y_max),randint(x_max,y_max))

def mod(x):
        if (x>0):
                return x
        else:
                return (-x)

def generateGrid(total_nodes):
        normal_list=[]
        normal_nodes=total_nodes
        normal_list_x=random.sample(range(x_max),normal_nodes)
        normal_list_y=random.sample(range(y_max),normal_nodes)
        for i in range(0,normal_nodes):
                normal_list.append((normal_list_x[i],normal_list_y[i]))
        complete_list=[]
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

def walk(num_iter):
        first_point=random_coordinate()
        walk_list=[]
        walk_list.append(first_point)
        for i in range(0,num_iter-1):
                new_point=distance_d(first_point,node_range)
                walk_list.append(new_point)
                first_point=new_point
        return walk_list

def sequence_walk(num_iter):
        sqrt_num_iter=int(sqrt(num_iter))
        spaced_list=list(np.linspace(1,sqrt_num_iter,sqrt_num_iter))
        xprime=x_max/(sqrt_num_iter+1)
        yprime=y_max/(sqrt_num_iter+1)
        walk_list=[(x*xprime,y*yprime) for (x,y) in list(itertools.product(spaced_list,spaced_list))]
        return walk_list
                
def all_rectangles(walk_list):
        rectangle_list=[]
        for (x,y) in walk_list:
                temp=[]
                temp.append((x-node_range,y-node_range))
                temp.append((x+node_range,y-node_range))
                temp.append((x+node_range,y+node_range))
                temp.append((x-node_range,y+node_range))
                rectangle_list.append(temp)
        return rectangle_list
        

complete_list=generateGrid(total_nodes)
normal_list=complete_list[0]    #unknown co-ordinates
normal_nodes=len(normal_list)
error_x=0
error_y=0
error_x2=0
error_y2=0
start_time=time.time()
#walk_list=walk(num_iter)
walk_list=sequence_walk(num_iter)
#print walk_list
rectangle_list=all_rectangles(walk_list)
#print rectangle_list
for normal_node in normal_list:
        inside_set=[]
        for rectangle in rectangle_list:
                if (point_inside_polygon(normal_node[0],normal_node[1],rectangle)):
                        inside_set.append(rectangle)
        #print len(inside_set)
        #centroid=centroid_set(inside_set)
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
files=open('result_moving_sensor.txt','a')
files.write(str(node_range)+'    '+str(num_iter)+'    '+str(normal_nodes)+'    '+str(x_max)+'    '+str(y_max)+'    '+str(avgerror_x)+'    '+str(avgerror_y)+'    '+str(average_time)+'    '+str(avgstd)+'\n')
files.close()
