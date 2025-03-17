import PixelSequence as ps
import AntColony as ac
import numpy as np
import base64
import cv2 #openCV
import math

pixelQueue=[]
endpoints=[]
scannedimg=[]
pos=[0,0]
min_R=[]
finalPath=[]

def getimg(url): 
    #print('url:',url)
    url=url[url.index(",")+1:]

    # with open('imcode.txt', 'w', encoding='utf-8') as file:
    #     file.write(url)

    data=base64.b64decode(url)
    imgarray=np.fromstring(data,np.uint8)
    img=cv2.imdecode(imgarray,cv2.COLOR_RGB2BGR)
    print('img.shape:',np.array(img).shape)
    return np.array(img)

def sendimg(img,name=None):
    _,jpgdata=cv2.imencode('.jpg',img)
    if name!=None:
        with open('./'+name+'.jpg','wb')as fs:
            fs.write(jpgdata)
            fs.close
    data=base64.b64encode(jpgdata)
    return "data:image/jpg;base64,"+str(data)[2:-1]

def saveimg(img,name='tempoImg'):
    _,jpgdata=cv2.imencode('.jpg',img)
    with open('./'+name+'.jpg','wb')as fs:
        fs.write(jpgdata)
        fs.close

def get_light_contour(url):
    global pixelQueue
    global endpoints
    global scannedimg
    global pos

    thresH=245
    thresL=105
    minArea=50 #小于此值的连通域将被去除
    minJudgeLen=42 #小于此值的轮廓将不参与判定
    minSaveRatio=5 #评判比大于此比值的连通域将在夹层判定中保留

    pos=[0,0] #全局初始化
    pixelQueue=[]
    endpoints=[]
    scannedimg=[]

    img=getimg(url)

    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    
    grey=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) #灰度化
    filted=cv2.bilateralFilter(grey,4,75,100) #双边滤波,平滑整体的同时尽可能保留边缘细节

    edge=cv2.Canny(filted,thresL,thresH)#边缘检测
    
    edge=np.array(edge,np.uint8)

#---------------形态学运算--------------------------------------------------------------
    kernel=np.ones((4,4),np.uint8)#卷积核       
    back=cv2.morphologyEx(edge,cv2.MORPH_CLOSE,kernel)#闭运算，先膨胀后腐蚀
    back=back[1:,1:] #错位补偿
    back=np.insert(np.insert(back,(back.shape[0]),0,1),(back.shape[1]),0,0)-edge #黑帽运算提取夹层区
    back=cv2.morphologyEx(back,cv2.MORPH_CLOSE,kernel)  #闭运算减少连通分量
    back=back[1:,1:]
    back=np.insert(np.insert(back,(back.shape[0]),0,1),(back.shape[1]),0,0) #补零
    dense=cv2.morphologyEx(back,cv2.MORPH_OPEN,kernel) #开运算，先腐蚀后膨胀,得到高密部分
    dense=dense[1:,1:]
    dense=np.insert(np.insert(dense,(dense.shape[0]),0,1),(dense.shape[1]),0,0)
    gap=back-dense #顶帽运算去除夹角高密区, 得到狭长区
    del(back)
#--------------------------------------------------------------------------------------
    dense=cv2.erode(dense,kernel)
    light=edge*(255-dense)/2 #去除复杂部分
    _,light=cv2.threshold(light*10,1,255,cv2.THRESH_BINARY) #阈值化调整
    light=np.array(light,np.uint8)
    del(dense)

    # cv2.imshow('edge', edge)
    # cv2.waitKey(0)

    conimg=np.zeros_like(edge,np.uint8)

    contour,_=cv2.findContours(255-gap,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)#提取gap的轮廓
    contour=np.array(contour,dtype=object)
    del(gap)

    #cntNum 连通域个数
    #labels 连通域标记图
    #states 连通域信息[x,y,width,height,area]
    cntNum,labels,states,_=cv2.connectedComponentsWithStats(light,connectivity=8)#提取连通域
    states=np.array(states) #连通域array
#----------------------------------------------------------------------------------------------
    deletstack=[]

    for rm in range(states.shape[0]): #删去过小的连通域
        if states[rm][4]<minArea:
            deletstack.append(rm)

    for single in contour: #遍历轮廓
        if len(single)>= minJudgeLen: #忽略小轮廓
            judgelist=[]
            overlap_dic={}
            downdivide=3

            for pixel in single[::downdivide]: #遍历轮廓中的像素
                px=pixel[0][0]
                py=pixel[0][1]
                ca_index=labels[py][px] #该像素点所在连通域的索引值
                conimg[py][px]=255
                #选取所有与该轮廓重合的连通域
                if ca_index!=0: #轮廓与连通域有重合
                    if len(overlap_dic)==0 or (ca_index not in overlap_dic.keys()): #初次存入
                        overlap_dic[ca_index]=[1,states[ca_index][4]]
                        #保存间隙轮廓所覆盖到的所有连通域
                    else:
                        overlap_dic[ca_index][0]+=1

            for key in overlap_dic:
                #计算评判值,为连通域总面积和覆盖有轮廓的面积之比。
                judgevalue=overlap_dic[key][1]/overlap_dic[key][0]/downdivide-1 
                judgelist.append([key,judgevalue])
            judgelist.sort(key=lambda x:x[1],reverse=True)
            #print('judgelist:',judgelist)
                        
            if len(judgelist)>1:
                mean=np.average(judgelist,axis=0)
                for n in range(len(judgelist)):
                    if judgelist[n][1]<mean[1]:
                        meanindex=n
                        break
                for x in judgelist[meanindex:]: 
                    #将评值小于均值且小于minSaveRatio的连通域索引放入回收栈
                    if x[0] not in deletstack and x[1]<minSaveRatio: 
                        deletstack.append(x[0])
                        #print('**delet:{} **state:{}'.format(x[0],states[x[0]]))
         
#------------------------------------------------------------------------------------------
    remove=np.zeros_like(light,np.uint8)
    cntNum=cntNum-len(deletstack)

    for rm in deletstack: 
        for y in range(states[rm][1],states[rm][1]+states[rm][3]):
            for x in range(states[rm][0],states[rm][0]+states[rm][2]):
                if labels[y][x]==rm:
                    remove[y][x]=255
    
    return sendimg(light-remove,'contour'),cntNum

def contour_to_path():
    global pixelQueue
    global endpoints
    global scannedimg
    global finalPath
    global pos

    finalPath=[]

    x=pos[0]
    y=pos[1]
    if x==0 & y==0:
       pixelQueue=[]
       endpoints=[] 
       #img=np.array(getimg(url))
       #img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) #灰度化
       img=cv2.imread('./contour.jpg',0)
       #img=np.array(np.swapaxes(img,0,2)[0]).T
       print('@img.shape:',np.array(img).shape)
       _,img=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
       
       edge=np.zeros(img.shape,np.uint8)
    
    else: 
       edge=cv2.imread('./contour.jpg',0)
       _,edge=cv2.threshold(edge,127,255,cv2.THRESH_BINARY)
       img=np.array(scannedimg)
       #img=np.array(cv2.imdecode(np.frombuffer(base64.b64decode(data),np.uint8),0))
       _,img=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
       x=int(x)
       y=int(y)

    psize=0  
    while psize==0:
         if img[y][x]==255:
             path=ps.ConnectArea(img,x,y)
             psize=path.size
         if x==img.shape[0]-1:
            if y==img.shape[1]-1:
                scannedimg=[] #free it
                pos=[0,0] #re-init
                return 0
            x=0 #回车
            y+=1 #换行
         else: x+=1

    scannedimg=path.left
    
    for queue in path.data:
        pixelQueue.append(queue)
        endpoints.append([list(queue[0]),list(queue[-1]),[len(queue),len(pixelQueue)-1]])
    edge+=np.array(path.img)   

    pos[0]=x
    pos[1]=y

    return {'x':x,'y':y,'url':sendimg(edge,'contour')}

def compute_adjacency_matrix():
    global endpoints
    dotlist=np.array(endpoints)[:,:2,:]

    mSize=2*len(dotlist)
    endpoints=np.array(dotlist).reshape((mSize,2))
    ajm=np.zeros((mSize,mSize)) 

    for j in range(mSize):
        for i in range(round(j/2+0.8)*2,mSize):
            d=round(np.sqrt((endpoints[i][0]-endpoints[j][0])**2+(endpoints[i][1]-endpoints[j][1])**2))
            ajm[j][i]=d
            ajm[i][j]=d
    #print(ajm)
    ac.AntColony_init(ajm,4,1,0.7,10)

    return {'dotlist':dotlist.tolist()}

def antseek():
    global endpoints
    global min_R

    ant=[]
    min=[100000,-1]
    for i in range(round(np.sqrt(len(endpoints))/1.2)):
        p=ac.Ant(i)
        ant.append(p)
        for x in range(p.size):
            p.go()
        if p.path_len<min[0]:
            min=[p.path_len,p.id] #当前最短路径
        #print(min[0])
    min_R=ac.catch_min(3)

    min_path=[]
    min_return_list=min_R[1]
    print(min_return_list)
    for index in min_return_list:
        min_path.append(list(endpoints[index]))

    return {'path':np.array(min_path).tolist(),'info':str(min_R[0]),'pres':str(min[0])}

def compress_by_curvity(path,downrate=4,thres=-0.2):
    if len(path)<30:
        return path
    else:
        #img=np.zeros((940,940))
        curvityQueue=np.ones((1,5))
        judgeQueue=np.zeros((1,5))

        if downrate<=1:
            downrate=2

        pointer=len(path)-4
        while pointer>-8:
            #7+1队列
            head=pointer-3
            end=pointer+3
            deljudge=end+1
            x1=path[head][0]-path[pointer][0]
            x2=path[end][0]-path[pointer][0]
            y1=path[head][1]-path[pointer][1]
            y2=path[end][1]-path[pointer][1]
            distan1=math.sqrt(x1**2+y1**2)
            distan2=math.sqrt(x2**2+y2**2)
            #cos值作为曲率,cos值大则曲率大,该点倾向于保留
            cosin=(x1*x2+y1*y2)/(distan1*distan2) 
            #尾添头删
            curvityQueue=np.append(curvityQueue,cosin)[1:]
            judgeQueue=np.append(judgeQueue,0)[1:]

            if curvityQueue[0]+judgeQueue[0]<thres: #判断为要删去
                path=np.delete(path,deljudge,0)
                #print('delet:',deljudge)
                fit_downrate=downrate*((thres-curvityQueue[0])/(thres+1))-1
                if fit_downrate>=1:
                    judgeQueue+=(thres+1)/fit_downrate
                else:
                    judgeQueue+=thres+1
            pointer-=1

        path=path[::2]
        #for pos in path:
        #    img[pos[1]][pos[0]]=255
        #saveimg(img,'path')

        return path

def path_fft(downrate=1,path=None):
    global finalPath
    if path==None:
        path=finalPath
    path=np.array(path[::int(downrate)])
    num=len(path)
    cpxpath=np.zeros(len(path),dtype=np.complex64)
    cpxpath.real=path[:,:1].flatten()
    cpxpath.imag=path[:,1:].flatten()
    fftresult=np.fft.fft(cpxpath)/num
    
    adjust=np.zeros(num).astype(np.complex64)
    for i in range(num):
        adjust[i]=adjust[i-1]+fftresult[(-1)**i*round(i/2+0.2)] #交错重排

    result=np.dstack((adjust.real,adjust.imag))
    return result[0]

def optim_and_fft():
    global pixelQueue
    global min_R
    global endpoints
    global finalPath

    endpoints=[] #free it
    finalPath=[]

    for i in range(round(len(min_R[1])/2-0.2)):
        #min_R[1]中的index两两一组,各位首尾
        sort_index=min_R[1][2*i+1]
        #偶数为首,正序接入.奇数为尾,逆序接入.
        if sort_index%2==0:
            finalPath.extend(pixelQueue[round(sort_index/2-0.2)])
        else: 
            finalPath.extend(pixelQueue[round(sort_index/2-0.2)][::-1])
    min_R=[] #free it        
    pixelQueue=[] #free it

    finalPath=compress_by_curvity(finalPath)
    result=path_fft()

    return {'result':result.tolist()}