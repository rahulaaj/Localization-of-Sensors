from __future__ import division
from random import randint
from itertools import combinations
from shapely.validation import explain_validity
from shapely.geometry import Point,Polygon,MultiPolygon
from math import sqrt,log10,pi
import random
import itertools
import numpy as np
import time
x_max=10000
y_max=10000
percent_beacon=0.01
percent_obstacles=0.1
total_nodes=1000
height_node=1000                 # in m
obst_height_range=100            # in m
initial_power=10000              # in dB
frequency=1000000                # in Hz
n=3
#strength_dict=dict()            #key is sensor_coordinate and beacon_coordinate as tuple of tuples to get strength

def mod(x):
        if (x>0):
                return x
        else:
                return (-x)

def neighbor(x,y):
        temp=[]
        temp.append((x-1,y-1))
        temp.append((x,y-1))
        temp.append((x+1,y-1))
        temp.append((x-1,y))
        temp.append((x+1,y))
        temp.append((x-1,y+1))
        temp.append((x,y+1))
        temp.append((x+1,y+1))
        return temp

def normalWithNeighbors(normal_list):
        final_list=[]
        for (x,y) in normal_list:
                final_list.append((x,y))
                neighbors=neighbor(x,y)
                final_list=final_list+neighbors
        return final_list
                

def generateGrid(percent_beacon,percent_obstacles,total_nodes):
        beacon_nodes=int(percent_beacon * total_nodes)
        obstacles=int(percent_obstacles * total_nodes)
        beacon_list=[]
        normal_list=[]
        obstacles_list=[]
        sqrt_beacon_nodes=int(sqrt(beacon_nodes))
        spaced_list=list(np.linspace(0,x_max,sqrt_beacon_nodes))
        beacon_list=[(int(x),int(y)) for (x,y) in list(itertools.product(spaced_list,spaced_list))]
        beacon_nodes=len(beacon_list)
        normal_nodes=total_nodes - beacon_nodes
        total=normal_nodes+obstacles
        total_list_x=random.sample(range(x_max),total)
        total_list_y=random.sample(range(y_max),total)
        for i in range(0,normal_nodes):
                normal_list.append((total_list_x[i],total_list_y[i]))
        for i in range(normal_nodes,total):
                height=randint(0,height_node+obst_height_range)
                obstacles_list.append(((total_list_x[i],total_list_y[i]),height))
        complete_list=[]
        complete_list.append(beacon_list)
        complete_list.append(normal_list)
        complete_list.append(obstacles_list)
        return complete_list
"""
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
"""

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

def all_triangles(xy_list):
        temp_list=[]
        for triplet in combinations(xy_list,3):
                #print list(triplet)
                #triplet_list=[]
                #triplet_list.append(triplet)
                temp_list.append(list(triplet))
        return temp_list

def findIntersect(inside_set):
        if (len(inside_set)==0):
                return [(0,0),(x_max,0),(x_max,y_max),(0,y_max),(0,0)]
        elif (len(inside_set)==1):
                #print "In 1"
                p1=Polygon(inside_set[0])
                return list(p1.exterior.coords)
        elif (len(inside_set)==2):
                #print "In 2"
                p1=Polygon(inside_set[0])
                p2=Polygon(inside_set[1])
                #if (p1.intersection(p2).area !=0):
                        #print p1.intersection(p2).area
                return list(p1.intersection(p2).exterior.coords)
                #else:
                #        return ([])
        else:
                #print "In >2"
                p1=Polygon(inside_set[0])
                p2=Polygon(inside_set[1])
                a=inside_set.pop(0)
                b=inside_set.pop(0)
                #if (p1.intersection(p2).area !=0):
                        #print p1.intersection(p2).area
                        #explain_validity(p1.intersection(p2))
                inside_set.insert(0,list(p1.intersection(p2).exterior.coords))
                return findIntersect(inside_set)
                #else:
                #        return ([])
#print generateGrid(0.2,20)
complete_list=generateGrid(percent_beacon,percent_obstacles,total_nodes)
beacon_list=complete_list[0]    #known co-ordinates
beacon_nodes=len(beacon_list)
#print beacon_list
normal_list=complete_list[1]    #unknown co-ordinates
normal_nodes=len(normal_list)
#print normal_list
obstacles_list=complete_list[2] #obstacles with first element coordinates and second the height
obstacles=len(obstacles_list)
#print obstacles_list
triangle_list=all_triangles(beacon_list)        #list of list of triangles
#print normal_nodes
#for x in combinations([1,2,3,4,5],3):
#        print x
#print point_inside_polygon(1,1,[(0,0),(0,2),(2,2),(2,0)])
triangle_list=all_triangles(beacon_list)        #list of list of triangles
triangle_centroid=dict()
start_time=time.time()
for triangle in triangle_list:
        p=Polygon(triangle)
        centroid=list(p.centroid.coords)
        area=p.area
        triangle_centroid[str(triangle)]=(centroid,area)

def centroid_set(inside_set):
        if (len(inside_set)==0):
                return [[x_max/2,y_max/2]]
        else:   
                sum_x=0
                sum_y=0
                a=0
                for triangle in inside_set:
                        centroid=triangle_centroid[str(triangle)][0]
                        area=triangle_centroid[str(triangle)][1]
                        sum_x=sum_x+((centroid[0][0])/area)
                        sum_y=sum_y+((centroid[0][1])/area)
                        a=a+(1/area)
                return [[sum_x/a,sum_y/a]]

def create_strength_dict(beacon_list,obstacles_list,normal_list):
        strength_dict=dict()
        new_normal_list=normalWithNeighbors(normal_list)      
        for beacon in beacon_list:
                for normal in new_normal_list:
                        distance=sqrt((normal[0]-beacon[0])*(normal[0]-beacon[0])+(normal[1]-beacon[1])*(normal[1]-beacon[1]))
                        new_strength=initial_power+(n*10*log10(frequency/(4*pi*distance)))
                        for (obstacle,height) in obstacles_list:
                                d1=sqrt((obstacle[0]-beacon[0])*(obstacle[0]-beacon[0])+(obstacle[1]-beacon[1])*(obstacle[1]-beacon[1]))/1000
                                d2=sqrt((obstacle[0]-normal[0])*(obstacle[0]-normal[0])+(obstacle[1]-normal[1])*(obstacle[1]-normal[1]))/1000
                                d=distance/1000
                                f=frequency
                                f1=17.3*sqrt((d1*d2*1000000)/(f*d))
                                hl=height_node
                                ho=height
                                h=hl-ho
                                cn=h/f1
                                a=10-20*cn
                                new_strength=new_strength+a
                        strength_dict[(normal,beacon)]=new_strength
        return strength_dict

#print triangle_list
strength_dict=create_strength_dict(beacon_list,obstacles_list,normal_list)
print "Dictionary created"

def point_inside_triangle(x,y,triangle):
        neighbor_list=neighbor(x,y)
        strength1=strength_dict[((x,y),triangle[0])]
        strength2=strength_dict[((x,y),triangle[1])]
        strength3=strength_dict[((x,y),triangle[2])]
        #in_triangle=True
        for neighbors in neighbor_list:
                strength1_n=strength_dict[(neighbors,triangle[0])]
                strength2_n=strength_dict[(neighbors,triangle[0])]
                strength3_n=strength_dict[(neighbors,triangle[0])]
                if((strength1>strength1_n and strength2>strength2_n and strength3>strength3_n) or (strength1<strength1_n and strength2<strength2_n and strength3<strength3_n)):
                        #print neighbors
                        #in_triangle=False
                        return False
        #print in_triangle
        #return in_triangle
        return True

#print list(p1.centroid.coords)
#print point_inside_polygon(1,1,[(0,0),(10,0),(0,10)])
error_x=0
error_y=0
error_x2=0
error_y2=0
for normal_node in normal_list:
        inside_set=[]
        for triangle in triangle_list:
                if (point_inside_triangle(normal_node[0],normal_node[1],triangle)):
                        inside_set.append(triangle)
        centroid=centroid_set(inside_set)
        #common_region=findIntersect(inside_set)
        #p1=Polygon(common_region)
        #centroid=list(p1.centroid.coords)
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
avgstd=sqrt(error_x2+error_y2)/(2*normal_nodes)
"""
print "Average error in x-coordinate"
print avgerror_x
print "Average error in y-coordinate"
print avgerror_y
"""
files=open('result_centroid.txt','a')
files.write(str(obstacles)+'    '+str(beacon_nodes)+'    '+str(normal_nodes)+'    '+str(x_max)+'    '+str(y_max)+'    '+str(avgerror_x)+'    '+str(avgerror_y)+'    '+str(average_time)+'    '+str(avgstd)+'\n')
files.close()
