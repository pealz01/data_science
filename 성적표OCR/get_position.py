import cv2
import random
#참조 - https://www.youtube.com/watch?v=cUOcY9ZpKxw&t=490s

scale=0.5
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

img =  cv2.imread('imgs/samp_table.png')
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
"""
    [[(4, 45), (88, 77), 'text', 'idnum'],
       [(92, 46), (190, 77), 'text', 'name'],
       [(291, 46), (375, 76), 'text', 'bday'],
       [(384, 46), (463, 79), 'text', 'area'],
       [(474, 46), (792, 80), 'text', 'sclnm'],
       [(93, 255), (191, 289), 'int', 'hist_grd'],
       [(198, 130), (287, 164), 'text', 'kornm'],
       [(201, 170), (283, 204), 'int', 'kor_sig'],
       [(200, 213), (282, 244), 'int', 'kor_100'],
       [(200, 255), (282, 288), 'int', 'kor_grd'],
       [(293, 131), (376, 161), 'text', 'mathnm'],
       [(293, 171), (376, 203), 'int', 'math_sig'],
       [(294, 213), (375, 247), 'int', 'math_100'],
       [(294, 256), (378, 286), 'int', 'math_grd'],
       [(387, 255), (468, 286), 'int', 'eng_grd'],
       [(476, 131), (627, 160), 'text', 'tam1nm'],
       [(477, 173), (619, 202), 'int', 'tam1_sig'],
       [(479, 213), (626, 245), 'int', 'tam1_100'],
       [(479, 257), (631, 290), 'int', 'tam1_grd'],
       [(641, 131), (798, 164), 'tam2nm', 'tam2nm'],
       [(640, 173), (792, 202), 'int', 'tam2_sig'],
       [(644, 215), (798, 245), 'int', 'tam2_100'],
       [(644, 256), (794, 289), 'int', 'tam2_grd'],
       [(804, 130), (893, 161), 'text', 'fore_nm'],
       [(808, 256), (895, 288), 'int', 'fore_grd']]
"""