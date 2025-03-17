
import base64
import cv2 #openCV
import numpy as np

with open('imcode.txt', 'r', encoding='utf-8') as file:
    url = file.read()

    #url=url[url.index(","):]

    with open('./base64.jpg','wb') as file:
        img = base64.b64decode(url)
        file.write(img)
    data=base64.b64decode(url)
    imgarray=np.frombuffer(data,np.uint8)
    #imgarray = imgarray.astype(np.uint8)
    img=cv2.imdecode(imgarray,1)

    print(f'shape:{img.shape}')

    cv2.imshow('img', img)
    cv2.waitKey(0)