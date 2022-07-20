import numpy as np
import random
import threading

#----关联点(离散曲线阵)的蚁群算法---------------------------------------------------

#----static global---------
AdjacentList=[]     #邻接矩阵
visibility_graph=[] #能见度
num=0    #节点总数
alpha=1  #能见度权重
beta=15   #信息素权重
rho=0.8  #信息素挥发系数
tao=2    #初始信息素
Q=1
lock=threading.RLock()
#----variable global----------
#多线程时,全局变量需用线程锁进行保护
pheromone_graph=[]  #信息素(弗洛蒙)
min_return=[0,0]


def AntColony_init(distan,a,b,r,q):
    global AdjacentList
    global visibility_graph
    global pheromone_graph
    global alpha
    global beta
    global rho
    global num
    global Q
    global min_return
    min_return=[100000,0]
    num=len(distan)
    AdjacentList=distan
    pheromone_graph=np.ones((num,num))
    visibility_graph=np.zeros((num,num))
    for y in range(num):
        for x in range(num):
            if distan[y][x]!=0:
                visibility_graph[y][x]=round(1000/distan[y][x],2)
            else: pheromone_graph[y][x]=0
    alpha=a
    beta=b
    rho=r
    Q=q

class Ant:
    def __init__(self,ID):
        self.id=ID
        self.size=num
        self.start=random.randint(0,num-1)
        self.end=self.start+1 if self.start%2==0 else self.start-1  #偶加奇减
        self.choice_list=visibility_graph[self.start]*alpha+pheromone_graph[self.start]*beta
        self.prob_list=self.choice_list/sum(self.choice_list) if sum(self.choice_list)!=0 else 0
        self.present=self.start
        self.path=[self.start]
        self.path_len=0

    def go(self):
        global pheromone_graph
        global min_return
        if num<=2:
            self.path.append(self.end)
            self.path_len=0
            lock.acquire() #--------------上锁
            min_return[0]=self.path_len
            min_return[1]=self.path
            lock.release() #--------------解锁
            return
        if len(self.path)==num: return
        arrow=random.uniform(0,1) #概率箭
        target_disk=0   #靶盘
        tar=0
        for i in range(num): 
            target_disk+=self.prob_list[i]
            if arrow<=target_disk:break
            tar+=1
        self.path_len+=AdjacentList[tar][self.present]    
        self.path.append(tar)
        #print(self.path,"&",self.path_len)
        relate=tar+1 if tar%2==0 else tar-1  #偶加奇减
        self.path.append(relate)
        self.present=relate
        #决定选择的概率分布
        self.choice_list=pow(visibility_graph[self.present],alpha)*pow(pheromone_graph[self.present],beta)
        for i in self.path:
            self.choice_list[i]=0
        self.choice_list[self.end]=0
        if sum(self.choice_list)==0: #遍历结束
             self.path.append(self.end)
             self.path_len+=AdjacentList[self.end][self.present]  
             self.present=self.end

             lock.acquire() #--------------上锁
             pheromone_graph=pheromone_graph*rho
             i=0
             while i<len(self.path)-1:
                 pheromone_graph[self.path[i]][self.path[i+1]]+=round(num*Q/self.path_len,2)
                 pheromone_graph[self.path[i+1]][self.path[i]]+=round(num*Q/self.path_len,2)
                 i+=2
             pheromone_graph=np.around(pheromone_graph,decimals=2)
             lock.release() #--------------解锁

             if self.path_len<min_return[0]:
                 lock.acquire() #--------------上锁
                 min_return[0]=self.path_len
                 min_return[1]=self.path
                 lock.release() #--------------解锁
             return
        self.prob_list=self.choice_list/sum(self.choice_list)
        return

def catch_min(rate):
    if num<=2:
        return min_return
    global pheromone_graph

    lock.acquire() #--------------上锁
    pheromone_graph=pheromone_graph*rho
    #print("min:",min_return[0])
    i=0
    while i<len(min_return[1]):
        pheromone_graph[min_return[1][i]][min_return[1][i+1]]+=round(rate*num*Q/min_return[0],2)
        pheromone_graph[min_return[1][i+1]][min_return[1][i]]+=round(rate*num*Q/min_return[0],2)
        i+=2
    pheromone_graph=np.around(pheromone_graph,decimals=2)
    lock.release() #--------------解锁
    return min_return

