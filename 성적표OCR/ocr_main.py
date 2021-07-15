import cv2
import sys
import numpy as np
import pytesseract
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import re
from perspective_scan import get_perspective_scan
import warnings

warnings.filterwarnings("ignore")

def get_table(img):
    if img is None:
        print('Image load failed')
        sys.exit()
    else:
        tmp = get_perspective_scan(img)
        tmp.callback()
        tmp.result = cv2.resize(tmp.result, (899, 337))
        cv2.imwrite("imgs/table.png", tmp.result)
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
       [(476, 131), (627, 160), 'text', 'tamnm1'],
       [(477, 173), (619, 202), 'int', 'tam1_sig'],
       [(479, 213), (626, 245), 'int', 'tam1_100'],
       [(479, 257), (627, 290), 'int', 'tam1_grd'],
       [(641, 131), (798, 164), 'tam2nm', 'tamnm2'],
       [(640, 173), (792, 202), 'int', 'tam2_sig'],
       [(644, 215), (798, 245), 'int', 'tam2_100'],
       [(644, 256), (794, 289), 'int', 'tam2_grd'],
       [(804, 130), (893, 161), 'text', 'forenm'],
       [(808, 256), (895, 288), 'int', 'fore_grd']]

#fuzz
fuzz_area = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
fuzz_kor = ['언어와 매체', '화법과 작문']
fuzz_mat = ['확률과 통계', '미적분', '기하']
fuzz_tam = ['한국지리', '세계지리', '세계사', '동아시아사', '경제', '정치와 법', '사회･문화', '생활과 윤리', '윤리와 사상', '물리학Ⅰ', '화학Ⅰ', '생명과학Ⅰ', '지구과학Ⅰ', '물리학Ⅱ', '화학Ⅱ', '생명과학Ⅱ', '지구과학Ⅱ', '성공적인 직업 생활', '농업 기초 기술', '공업 일반', '상업 경제', '수산·해운 산업 기초', '인간 발달']
fuzz_fore = ['독일어Ⅰ', '프랑스어Ⅰ', '스페인어Ⅰ', '중국어Ⅰ', '일본어Ⅰ', '러시아어Ⅰ', '아랍어Ⅰ', '베트남어Ⅰ', '한문Ⅰ']

#워터마크 제거 참조 - https://answer-id.com/ko/61913147
def back_rm(img):
    # 그레이스케일로 변화
    gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 그레이스케일 이미지 copy
    bg = gr.copy()

    # 워터마크 morphological transformations
    for i in range(6):
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                            (2 * i + 1, 2 * i + 1))
        bg = cv2.morphologyEx(bg, cv2.MORPH_CLOSE, kernel2)
        bg = cv2.morphologyEx(bg, cv2.MORPH_OPEN, kernel2)
    cv2.imwrite("imgs/bg.png", bg)
    # 그레이스케일 이미지에서 워터마크 subtract
    dif = cv2.subtract(bg, gr)
    cv2.imwrite("imgs/dif.png",dif)
    # dif, bg 이미지 threshold
    bw = cv2.threshold(dif, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    dark = cv2.threshold(bg, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # dark 이미지 내 검은 부분 gr 이미지에서 추출해서 Threshold로 0으로 바꾸기
    darkpix = gr[np.where(dark > 0)]
    darkpix = cv2.threshold(darkpix, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    bw[np.where(dark > 0)] = darkpix.T
    cv2.imwrite("imgs/bw.png", bw)

    # 이미지에 지정된 필터 마스크 이용해서 필터 먹이기
    # 참조 - https://pythonq.com/so/python/1756300
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    dst = cv2.filter2D(bw, -1, sharpen_kernel)
    return dst



if __name__=='__main__':
    mydata=[]
    path ='imgs/89d42daa-1ae8-49e2-9680-ea4750fc1c29'
    img = cv2.imread(path)
    imgtbl = get_table(img)
    imgtbl_trash = back_rm(imgtbl)
    imgshow = imgtbl.copy()
    imgmask = np.zeros_like(imgtbl)
    mydata = []

    cv2.imwrite("imgs/imgtbl_trash.png", imgtbl_trash)
    for x, r in enumerate(roi):
        txt = None
        cv2.rectangle(imgmask, (r[0][0],r[0][1]),(r[1][0],r[1][1]),(0,255,0),cv2.FILLED)
        imgshow = cv2.addWeighted(imgshow,0.99,imgmask,0.1,0)

        if r[3][-3:] in ['grd','sig','100']:
            lang_opt = 'digits'
            #
            config_opt = '--psm 6 --oem 1 -c tessedit_char_whitelist={}123456789'.format('' if r[3][-3:] == 'grd' else 0)
            #config_opt = r'--oem 1 --psm 6 outputbase digits'
        else:
            lang_opt = 'kor'
            config_opt = '-c preserve_interword_spaces=1 --psm 10'


        imgcrop = imgtbl_trash[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        imgcopy = imgcrop.copy()

        #지정된 박스 영역 내 세로줄 없애기
        thresh = cv2.threshold(imgcopy, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

        cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 500:
                cv2.drawContours(opening, [c], -1, (0, 0, 0), -1)
        result = cv2.bitwise_xor(imgcrop, opening)

        cv2.imwrite("imgs/imgcrop_{}.png".format(x), result)

        txt = pytesseract.image_to_string(result,lang=lang_opt, config=config_opt).strip()

        #txt 내 결과 토대로 비슷한 단어 찾기
        if txt is not None:
            if r[3] == 'area':
                txt =  process.extractOne(txt, fuzz_area, scorer=fuzz.ratio)[0]
            elif r[3] == 'kornm':
                txt = process.extractOne(txt, fuzz_kor,scorer=fuzz.ratio)[0]
            elif r[3] == 'mathnm':
                txt = process.extractOne(txt, fuzz_mat, scorer=fuzz.ratio)[0]
            elif r[3][:5] == 'tamnm':
                #로마자로 변경
                print(txt)
                txt = txt.replace("1", "|")
                txt = txt.replace("!", "|")
                txt =  txt.replace("||","Ⅱ")
                txt = txt.replace("|", "Ⅰ")

                txt = process.extractOne(txt, fuzz_tam,scorer=fuzz.ratio)[0]
            elif r[3] == 'forenm' :
                try:
                    print(txt)
                    txt = process.extractOne(txt, fuzz_fore,scorer=fuzz.ratio, score_cutoff=20)[0]
                except:
                    txt = ""
            else:
                txt = re.sub("[ ]*|","",txt)
                txt = txt.replace("|", "")
        mydata.append([r[3],txt])

    mydata = dict(mydata)
    print(mydata)
    cv2.imshow("block",imgshow)
    cv2.imwrite("imgs/sample_img.png", imgshow)
    cv2.waitKey(0)

