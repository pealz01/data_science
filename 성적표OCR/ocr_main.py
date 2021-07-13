import cv2
import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from fuzzywuzzy import process
import os
from perspective_scan import get_perspective_scan

#https://www.youtube.com/watch?v=W9oRTI6mLnU

def get_table(img):
    if img is None:
        print('Image load failed')
        sys.exit()
    else:
        tmp = get_perspective_scan(img)
        tmp.callback()
        samp_table_path = 'imgs/samp_table.png'
        img_samp = cv2.imread(samp_table_path)
        h, w, c = img_samp.shape
        tmp.result = cv2.resize(tmp.result, (w, h))
        #cv2.destroyAllWindows()
        return tmp.result

#sample 데이터 기준 각 영영 별 정보
roi =  [[(4, 45), (85, 77), 'text', 'idnum'],
       [(92, 46), (190, 77), 'text', 'name'],
       [(291, 46), (375, 76), 'text', 'bday'],
       [(384, 46), (463, 79), 'text', 'area'],
       [(474, 46), (792, 80), 'text', 'sclnm'],
       [(93, 255), (191, 289), 'int', 'hist_grd'],
       [(198, 130), (287, 164), 'text', 'kornm'],
       [(201, 170), (283, 204), 'int', 'kor_sig'],
       [(200, 213), (282, 244), 'int', 'kor_100'],
       [(200, 255), (282, 288), 'int', 'kor_grd'],
       [(290, 131), (376, 161), 'text', 'mathnm'],
       [(290, 171), (376, 203), 'int', 'math_sig'],
       [(294, 213), (375, 247), 'int', 'math_100'],
       [(294, 256), (378, 286), 'int', 'math_grd'],
       [(387, 255), (465, 286), 'int', 'eng_grd'],
       [(476, 131), (627, 160), 'text', 'tam1nm'],
       [(477, 173), (619, 202), 'int', 'tam1_sig'],
       [(479, 213), (626, 245), 'int', 'tam1_100'],
       [(479, 257), (627, 290), 'int', 'tam1_grd'],
       [(641, 131), (798, 164), 'tam2nm', 'tam2nm'],
       [(640, 173), (792, 202), 'int', 'tam2_sig'],
       [(644, 215), (798, 245), 'int', 'tam2_100'],
       [(644, 256), (794, 289), 'int', 'tam2_grd'],
       [(804, 130), (893, 161), 'text', 'fore_nm'],
       [(808, 256), (895, 288), 'int', 'fore_grd']]


if __name__=='__main__':
    mydata=[]
    path ='2a85a615-3a44-493a-aebf-b658b4b3218a'
    img = cv2.imread('imgs/{}'.format(path))
    imgtbl = get_table(img)
    imgshow = imgtbl.copy()
    imgmask = np.zeros_like(imgtbl)
    mydata = []


    #워터마크 제거
    #_, imgtbl_thresh = cv2.threshold(imgtbl, 150, 255, cv2.THRESH_BINARY)
    imgtbl = cv2.cvtColor(imgtbl, cv2.COLOR_BGR2GRAY)

    for x, r in enumerate(roi):
        cv2.rectangle(imgmask, (r[0][0],r[0][1]),(r[1][0],r[1][1]),(0,255,0),cv2.FILLED)
        imgshow = cv2.addWeighted(imgshow,0.99,imgmask,0.1,0)
        """
        if r[3] not in ['mat_grd','eng_grd','tam1nm','tam1_sig','tam1_grd']:
            imgcrop = imgtbl[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        else:
            imgcrop = imgtbl_thresh[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        """
        imgcrop = imgtbl[r[0][1]:r[1][1], r[0][0]:r[1][0]]

        if r[3][-3:] in ['grd','sig','100']:
            lang_opt = 'eng'
            config_opt = '--psm 6 --oem 1 -c tessedit_char_whitelist={}123456789'.format('' if r[3][-3:] == 'grd' else 0)
        else:
            lang_opt = 'kor'
            config_opt = '-c preserve_interword_spaces=1 --psm 4'


        mydata.append(pytesseract.image_to_string(imgcrop,lang=lang_opt, config=config_opt).strip())
    print(mydata)
    cv2.imshow("block",imgshow)
    cv2.waitKey(0)

#,config = '-c preserve_interword_spaces=1 --psm 4'