# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:54:26 2019

시작 창에서 cmd 실행 - pip install selenium 설치 이후 진행

Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Firefox: https://github.com/mozilla/geckodriver/releases
Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/
사용할 브라우저에 따라 위의 url로 들어가 적절한 버전 드라이브 다운로드(selenium과 브라우저의 버전 확인)

@author: 윤영한
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time 



options = webdriver.ChromeOptions()

# headless 옵션 설정
#options.add_argument('headless')
options.add_argument("no-sandbox")

# 브라우저 윈도우 사이즈
options.add_argument('window-size=1920x1080')

# 사람처럼 보이게 하는 옵션들
#options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
# UserAgent값 변경
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")


def get_page_info():
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='btn_result']")))
        btn_result = driver.find_elements_by_class_name('btn_result')
        result = []
        err_unit = []
       
        for i in btn_result: #입시결과 버튼 클릭, 페이지 오픈
            i.click()
            driver.switch_to.window(driver.window_handles[-1]) #오픈된 창으로 이동
            #driver.implicitly_wait(1)
            flg = True
  
            try:
                while flg:
                    tmp = []
                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='align_l pdl5']")))
                    #일정 시간이상 ajax reponse가 없으면 에러 발생
                    
                    html=driver.page_source
                    soup=BeautifulSoup(html,'lxml')
                    unit_info_div= soup.find('div',{'class':'d_right'})
                    unit_info = unit_info_div.find('h3').get_text().replace('\t','').replace('\n','') # 모집단위 / 대학명 긁기
                    unit_info = unit_info.split(' / ')
                    tbody=soup.find('tbody',{'id':'tbResult'})
                    tr=tbody.findAll('tr')
    
                    for j in tr:
                        td = j.findAll('td')
                        if (len(td) >= 6) & (td[6].get_text() != '미제출') & (td[6].get_text() != '-'): #미제출 혹은 없는 경우 제외하고 긁어오기
                            tmp = [k.get_text() for k in td]
                            tmp.insert(0, unit_info[1])
                            tmp.insert(1, unit_info[0])
                            
                            result.append(tmp)
                        else:
                            tmp = [k.get_text() for k in td]
                            tmp.insert(0, unit_info[1])
                            tmp.insert(1, unit_info[0])
                            rng = range((len(tmp))-1,13)
                            for idx in rng:
                                tmp.append('없음')
                            result.append(tmp)
                            pass
                    
                    flg = get_next_page()

                    
            except Exception as e:
                html=driver.page_source
                soup=BeautifulSoup(html,'lxml')
                unit_info_div= soup.find('div',{'class':'d_right'})
                unit_info = unit_info_div.find('h3').get_text().replace('\t','').replace('\n','')
                unit_info = unit_info.split(' / ')
                
                print('에러 : {0} / {1}_{2}'.format(str(e),unit_info[1],unit_info[0]))
                err_unit.append(unit_info) 
                driver.close()
                pass
                
            finally:
                driver.switch_to.window(driver.window_handles[0]) #다시 리스트 페이지로 focus 이동     
        return result, err_unit

def get_next_page():
    if len(driver.find_elements_by_css_selector("[class='next disabled']")) > 0 :
    #마지막 페이지일 경우 창 닫기
        #driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return False
    else:
    #마지막 페이지가 아닐 경우 페이지 넘기기
        driver.find_element_by_css_selector("[class='next']").click()
        time.sleep(1) #ajax 응답이 늦은 관계로 페이지 넘어간 이후 1초 쉬기
        return True
    
if __name__=='__main__':
    start_time=time.time()
    dir = "Chrome webdriver 경로 설정"
    driver=webdriver.Chrome(dir, chrome_options=options)
    year = '2019' #입시결과 수집 대상 년도
    driver.get('https://www.adiga.kr/')
    
    #그냥 손으로 로그인하기 / 키보드 보안 프로그램 때문에 send_keys 메소드 안먹음 자동 로그인 포기
    input("▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒직접 로그인 한 이후 아무 키나 입력▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
    
    #검색창으로 이동
    driver.get('https://www.adiga.kr/PageLinkAll.do?link=/kcue/ast/eip/eis/inf/sjinf/eipSjinfGnrl.do&p_menu_id=PG-EIP-05101')

    #라디오 버튼 내 년도 설정
    radio=driver.find_elements_by_xpath('//*[@id="sch_year"]')[1]
    select = Select(radio)
    select.select_by_value(year)
    
    driver.find_element_by_class_name('search_box_btn').click()   

    result=[]
    err=[]
    err_page=[]
    flg = True
    page = 1
    while flg:
        
        for i in [1,2,3]: # 모집단위 별로 페이지 이동 시 ajax call이 경우에 따라 늦게 받아오는 경우가 있어  총 3회 까지 시도
            try:
                tmp, tmp2 = get_page_info()
                if len(tmp) > 0:
                    result+=tmp
                    
                if len(tmp2) > 0:
                    err+=tmp2
                    
                flg = get_next_page()
                print('▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒{}페이지 완료▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'.format(page))
                page+=1
                element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='btn_result']")))
                break
            except:
                if i==3: 
                    #3차까지 시도한 이후 안되면 page pass
                    pass_y_n = ' - Pass'
                    err_page.append(page)
                    flg = get_next_page()
                    page+=1
                else:
                    pass_y_n = ''
                    print('▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒{0}페이지 {1}차 시도{2}▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'.format(page, i, pass_y_n))
                    time.sleep(1)
                pass
            

        
    
    col_nm=['대학명','모집단위','모집시기','전형유형','전형명','모집인원','모집인원','경쟁률','기준','학생부_환산점','등급','수능_환산점','수능_백분위','수능_등급']
    
    df = pd.DataFrame(data=result,columns=col_nm)
    df = df.sort_values(by=['대학명','모집시기','전형유형','모집단위'])
    
    df2 = pd.DataFrame(data=err,columns=['모집단위','대학명'])
    df2 = df2.sort_values(by=['대학명','모집단위'])
    df2 = df2[['대학명','모집단위']]
    
    df3 = pd.DataFrame(data=err_page,columns=['pass페이지']) if len(err_page) >0  else pd.DataFrame()
    
    #저장할 위치 확인
    save_dir = '저장 경로 설정'
    writer = pd.ExcelWriter('{}/2019_대학알리미_입결.xlsx'.format(save_dir))
    df.to_excel(writer, sheet_name="입시결과",index=False)
    df2.to_excel(writer, sheet_name="오류모집단위",index=False)
    df3.to_excel(writer, sheet_name="오류페이지",index=False)
    writer.save()
    
    print('▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒{0} mins - {1} to {2}▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒'.format((time.time()-start_time)/60),start_time,time.time())
