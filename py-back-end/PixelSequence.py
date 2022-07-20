import numpy as np

class ConnectArea:
     '边缘图像连通域分析(8连通)'
     #Circle for orientation
     cU=[(0,-1),(-1,-1),(1,-1),(1,0),(-1,0),(-1,1),(1,1),(0,1)]
     cD=[(0,1),(1,1),(-1,1),(-1,0),(1,0),(1,-1),(-1,-1),(0,-1)]
     cL=[(-1,0),(-1,1),(-1,-1),(0,-1),(0,1),(1,1),(1,-1),(1,0)]
     cR=[(1,0),(1,1),(1,-1),(0,-1),(0,1),(-1,1),(-1,-1),(-1,0)]
     cUL=[(-1,-1),(-1,0),(0,-1),(1,-1),(-1,1),(0,1),(1,0),(1,1)]
     cUR=[(1,-1),(1,0),(0,-1),(-1,-1),(1,1),(0,1),(-1,0),(-1,1)]
     cDL=[(-1,1),(0,1),(-1,0),(-1,-1),(1,1),(1,0),(0,-1),(1,-1)]
     cDR=[(1,1),(1,0),(0,1),(-1,1),(1,-1),(0,-1),(-1,0),(-1,-1)]
     #方向与检测顺序的对应字典，使得检测的移动方向倾向于不改变。由于栈的特性，故对应方向均取反向
     oris={(0,-1):cD,(0,1):cU,(-1,0):cR,(1,0):cL,(-1,-1):cDR,(1,-1):cDL,(-1,1):cUR,(1,1):cUL}

     def __init__(self,img,x,y):
         PixelStack=["@"]#分支像素栈
         self.size=0     #连通域总像素数
         img2=np.array(img,np.uint8)
         back=np.zeros_like(img,np.uint8)
         img=np.insert(np.insert(img,(0,img2.shape[0]),0,1),(0,img2.shape[1]),0,0)#先补一圈0,防止边缘无法检测
         self.ori=ConnectArea.cU #首次取下方优先
         self.x=x
         self.y=y
         self.data=[]
         databox=[]

         def seekBranch(x,y,ori):
             if img[y][x]>200:
                img[y][x]=200 #已检测标记
                back[y-1][x-1]=255
                databox.append((x-1,y-1))
                priorlen=len(PixelStack)
                RetagStack=[]
                if img2.shape[0]<30:
                   minsize=round(img2.shape[0]/16)
                else: minsize=50
                
                for devia in ori:#遍历8个方向,deviate：偏移量
                   if img[y+devia[1]][x+devia[0]]==255:
                      img[y+devia[1]][x+devia[0]]=240 #入栈标记
                      PixelStack.append((x+devia[0],y+devia[1],(devia[0],devia[1])))#位置+方向
                   if len(PixelStack)==priorlen and img[y+devia[1]][x+devia[0]]==240:
                      [RetagStack.append(PixelStack.index(m)) for m in PixelStack if m[0]==x+devia[0] and m[1]==y+devia[1]]
                #print("#",x-1,y-1,PixelStack)
                if len(PixelStack)==priorlen:
                   if len(RetagStack)==0: #真·末梢
                      if len(databox)>minsize:  #----------------除杂度！！！！！
                         self.data.append(tuple(databox))#list不能append,tuple可以
                         self.size+=len(databox) 
                      databox.clear()
                   elif (len(PixelStack)-len(RetagStack)>RetagStack[-1]):#构成环的情况
                      PixelStack.append(PixelStack.pop(RetagStack[-1]))#环尾置为优先

                   
             if len(PixelStack)>1:
                self.x=PixelStack[-1][0]
                self.y=PixelStack[-1][1]
                self.ori=ConnectArea.oris[PixelStack[-1][2]]
             PixelStack.pop()
             return 

         seekBranch(self.x+1,self.y+1,self.ori)
         while not(len(PixelStack)==0): #这里为了防止函数栈溢出，不采用递归
             seekBranch(self.x,self.y,self.ori)
         
         self.data=[list(x) for x in self.data]
         #[print(len(t),t[0],t[-1],self.data.index(t)) for t in self.data]
         self.left=img2-back
         back=np.zeros((img.shape[0]-2,img.shape[1]-2),np.uint8)
         for a in self.data:
               for b in a:
                  back[b[1]][b[0]]=255
         self.img=back
         del(img) #释放img空间       

'''timg=np.zeros((5,5))
timg[2][2]=255
timg[2][3]=255
timg[1][2]=255
timg[3][1]=255
timg[2][4]=255
timg[0][0]=255
timg[0][1]=255
timg[4][0]=255
timg[4][3]=255
timg[4][1]=255
timg[2][0]=255
timg[1][0]=255

print(timg)
p=ConnectArea(timg,2,2)
print(p.img,p.size)
print(p.data,len(p.data))
print(p.left)'''

