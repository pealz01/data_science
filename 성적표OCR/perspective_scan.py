import cv2
import numpy as np

"""
참조
https://bkshin.tistory.com/entry/OpenCV-14-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%92%A4%ED%8B%80%EA%B8%B0%EC%96%B4%ED%95%80-%EB%B3%80%ED%99%98-%EC%9B%90%EA%B7%BC-%EB%B3%80%ED%99%98
"""

#성적표 내 성적 테이블 꼭지점 4개 설정 시 위상 변화하는 클래스
class get_perspective_scan:
    def __init__(self, img):
        self.win_name = "scanning"
        self.h,self.w,self.c = img.shape
        self.img= cv2.resize(img,(self.w//3,self.h//3))
        self.rows, self.cols = img.shape[:2]
        self.draw = self.img.copy()
        self.pts_cnt = 0
        self.pts = np.zeros((4, 2), dtype=np.float32)
        cv2.imshow(self.win_name, self.img)
        self.result = None

    def onMouse(self, event, x, y, flags, param):  # 마우스 이벤트 콜백 함수 구현 ---①
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.draw, (x, y), 10, (0, 255, 0), -1)  # 좌표에 초록색 동그라미 표시
            cv2.imshow(self.win_name, self.draw)

            self.pts[self.pts_cnt] = [x, y]  # 마우스 좌표 저장
            self.pts_cnt += 1
            if self.pts_cnt == 4:  # 좌표가 4개 수집됨
                # 좌표 4개 중 상하좌우 찾기 ---②
                sm = self.pts.sum(axis=1)  # 4쌍의 좌표 각각 x+y 계산
                diff = np.diff(self.pts, axis=1)  # 4쌍의 좌표 각각 x-y 계산

                topLeft = self.pts[np.argmin(sm)]  # x+y가 가장 값이 좌상단 좌표
                bottomRight = self.pts[np.argmax(sm)]  # x+y가 가장 큰 값이 우하단 좌표
                topRight = self.pts[np.argmin(diff)]  # x-y가 가장 작은 것이 우상단 좌표
                bottomLeft = self.pts[np.argmax(diff)]  # x-y가 가장 큰 값이 좌하단 좌표

                # 변환 전 4개 좌표
                pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])

                # 변환 후 영상에 사용할 서류의 폭과 높이 계산 ---③
                w1 = abs(bottomRight[0] - bottomLeft[0])  # 상단 좌우 좌표간의 거리
                w2 = abs(topRight[0] - topLeft[0])  # 하당 좌우 좌표간의 거리
                h1 = abs(topRight[1] - bottomRight[1])  # 우측 상하 좌표간의 거리
                h2 = abs(topLeft[1] - bottomLeft[1])  # 좌측 상하 좌표간의 거리
                width = max([w1, w2])  # 두 좌우 거리간의 최대값이 서류의 폭
                height = max([h1, h2])  # 두 상하 거리간의 최대값이 서류의 높이

                # 변환 후 4개 좌표
                pts2 = np.float32([[0, 0], [width - 1, 0],
                                   [width - 1, height - 1], [0, height - 1]])

                # 변환 행렬 계산
                mtrx = cv2.getPerspectiveTransform(pts1, pts2)
                # 원근 변환 적용
                self.result = cv2.warpPerspective(self.img, mtrx, (int(width), int(height)))
                cv2.destroyWindow(self.win_name)
                #cv2.imshow('scanned', self.result)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

    def callback(self,):
        cv2.setMouseCallback(self.win_name, self.onMouse)  # 마우스 콜백 함수를 GUI 윈도우에 등록 ---④
        #cv2.imshow("scaned", self.result)
        #self.result = cv2.resize(self.result,(w,h))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__=='__main__':
    img_path = '성적표경로입력'
    img = cv2.imread('imgs/{}'.format(img_path))
    tmp = get_perspective_scan(img)
    tmp.callback()
    samp_table_path = 'imgs/samp_table.png'
    img_samp = cv2.imread(samp_table_path)
    h, w, c = img_samp.shape
    tmp.result = cv2.resize(tmp.result,(w, h))


