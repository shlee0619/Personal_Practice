import time
import sys;
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def show_replies(parent):
    comment_entry=[]
    replies=parent.find_elements("xpath", "//li[contains(@class, 'u_cbox_comment cbox_module__comment_')]") 
    for reply in replies:
         # 클린봇 필터가 있는 답글 패스
         if reply.find_elements(By.CLASS_NAME, 'u_cbox_cleanbot_contents'):
             continue

         reply_nick = reply.find_element(By.CLASS_NAME, 'u_cbox_nick').text
         reply_content = reply.find_element(By.CLASS_NAME, 'u_cbox_contents').text
         reply_date = reply.find_element(By.CLASS_NAME, 'u_cbox_date').text
         print(f"  └ 답글 닉네임: {reply_nick}")
         print(f"  └ 답글 내용: {reply_content}")
         print(f"  └ 답글 날짜: {reply_date}\n")
         # 답글 정보 저장
         comment_entry.append({
                    '답글 닉네임': reply_nick,
                    '답글 내용': reply_content,
                    '답글 날짜': reply_date
          })
    return comment_entry 

#프로그램 시작
print('네이버 웹툰 댓글 및 답글 크롤링 시작')

# 드라이버 설정 및 초기화
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome()
url = "https://comic.naver.com/webtoon/detail?titleId=777767&no=162&week=fri"
driver.get(url)
from selenium import webdriver
  

# 페이지 로딩을 기다립니다.
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "u_cbox_list")))

# 페이지 스크롤 (필요에 따라 조정)
driver.execute_script('window.scrollTo(0, (document.body.scrollHeight)-2300);')
time.sleep(3)  # 추가 로딩 시간 대기

# 전체 댓글 리스트
comments = driver.find_elements("xpath", "//li[contains(@class, 'u_cbox_comment cbox_module__comment_')]") 
comments_data = []

for idx, comment in enumerate(comments, start=1):
    comment_id=comment.get_attribute('class')
    #print(comment_id);break
    # 클린봇 필터가 있는 댓글 패스
    if comment.find_elements(By.CLASS_NAME, 'u_cbox_cleanbot_contents'):
        print(f"{idx}번째 댓글은 '클린봇'이 부적절한 표현을 감지하여 패스합니다.\n")
        continue

    # 댓글 정보 추출
    u_cbox_nick = comment.find_element(By.CLASS_NAME, 'u_cbox_nick').text
    u_cbox_contents = comment.find_element(By.CLASS_NAME, 'u_cbox_contents').text
    u_cbox_date = comment.find_element(By.CLASS_NAME, 'u_cbox_date').text
    u_cbox_cnt_recomm = comment.find_element(By.CLASS_NAME, 'u_cbox_cnt_recomm').text
    u_cbox_reply_cnt = comment.find_element(By.CLASS_NAME, 'u_cbox_reply_cnt').text
    # 댓글 데이터 구조에 답글 포함
    comment_entry = {
        '닉네임': u_cbox_nick,
        '내용': u_cbox_contents,
        '날짜': u_cbox_date,
        '추천 수': u_cbox_cnt_recomm,
        '답글': []  # 답글 리스트 추가
    }

    print(f"{idx}번째 댓글:")
    print(f"닉네임: {u_cbox_nick}")
    print(f"내용: {u_cbox_contents}")
    print(f"날짜: {u_cbox_date}")
    print(f"답글수: {u_cbox_reply_cnt}")
    print(f"추천 수: {u_cbox_cnt_recomm}\n")
    
    reply_button = comment.find_element(By.CLASS_NAME, 'u_cbox_btn_reply')
    driver.execute_script("arguments[0].click();", reply_button)  # 답글 버튼 클릭
    #time.sleep(3)  # 답글 목록 로딩 대기
    driver.implicitly_wait(3)
    
    #close()
    replies=[]
    #reply_area=driver.find_element(By.CLASS_NAME, 'u_cbox_reply_area')
    #print(reply_area.text)
    #break
    #.get_attribute('innerHTML')
    
    while True :    
        try:
            more_button = WebDriverWait(driver, 10).until(
                  EC.element_to_be_clickable((By.XPATH, "//div[@class='u_cbox_paginate']//span[text()='더보기']/ancestor::a"))
             )
            more_button.click()
            try:
                # 3초 동안 새로운 li 태그가 나타날 때까지 대기
                driver.implicitly_wait(3)
                comment=driver.find_element(By.XPATH, f'//li[@class="{comment_id}"]')               
            except:
                print("새로운 요소 로드 실패")
        except:
            #print("답글 더보기 클릭 실패")
            break
    
    comment=driver.find_element(By.XPATH, f'//li[@class="{comment_id}"]')
    show_replies(comment)
    #print(comment.text)
    break
print('종료')
#driver.close()