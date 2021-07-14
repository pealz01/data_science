import cv2
import random
#참조 - https://www.youtube.com/watch?v=cUOcY9ZpKxw&t=490s

circles = []
counter =0
counter2 = 0
point=[]
point2=[]
mypoints =[]
mycolor = []

def mousepoints(event,x,y,flags,params):
    global  counter, point1 ,point2, counter2,circles, mycolor
    if event == cv2.EVENT_LBUTTONDOWN:
        if counter==0:
            #point1 = int(x//scale), int(y//scale);
            point1 = int(x), int(y);
            counter+=1
            mycolor = (random.randint(0,2)*200, random.randint(0,2)*200, random.randint(0,2)*200)
        elif counter ==1:
            #point2 = int(x//scale), int(y//scale)
            point2 = int(x), int(y)
            type = input('Enter Type ')
            name = input('Enter Name ')
            mypoints.append([point1, point2 , type, name])
            counter = 0
        circles.append([x,y,mycolor])
        counter2 +=1

img =  cv2.imread('경로입력')
#simg = cv2.resize(img,(0, 0), None, scale, scale)
grayA = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)




while True:

    for x,y,color in circles:
        cv2.circle(img,(x,y),3,color,cv2.FILLED)
    cv2.imshow("original image", grayA)
    cv2.setMouseCallback("original image",mousepoints)
    if cv2.waitKey(1) & 0xFF ==ord('s'):
        print(mypoints)
        break
