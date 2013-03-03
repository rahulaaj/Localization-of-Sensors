from random import randint
import random
x_max=100000
y_max=100000
percent_beacon=0.01
total_nodes=10000
#def random_coordinate(x,y):
#        return (randint(x,y),randint(x,y))

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

#print generateGrid(0.2,20)
complete_list=generateGrid(percent_beacon,total_nodes)
beacon_list=complete_list[0]    #known co-ordinates
normal_list=complete_list[1]    #unknown co-ordinates
                

