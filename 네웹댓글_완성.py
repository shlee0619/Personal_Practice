
import time
from selenium  import webdriver
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions( )
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)


def is_element_present_by_class_name(driver, element):
    try:
        driver.find_element(By.CLASS_NAME, element)
        return True
    except Exception as ex:
        return False


def move_to_element(driver, element):
    try:
        actions = ActionChains(driver).move_to_element(element)
        actions.perform()
    except Exception as ex:
        print(ex)

try:
    driver.get('https://comic.naver.com/webtoon/detail?titleId=769209&no=84')
    time.sleep(1)
    u_cbox_sort = driver.find_element(by=By.CSS_SELECTOR, value='#cbox_module > div > div.u_cbox_sort')
    driver.execute_script("arguments[0].scrollIntoView();", u_cbox_sort)
    elements =  driver.find_elements(by=By.CSS_SELECTOR, value='#cbox_module_wai_u_cbox_content_wrap_tabpanel > ul > li.u_cbox_comment')

    for i in range(2):  # 모두 펼치려면 오래걸려서 2개만  원본 for i in range(len(elements)):
        try:
            # 답글 펼치기
            u_cbox_btn_reply = elements[i].find_element(By.CSS_SELECTOR, value='div.u_cbox_comment_box > div > div.u_cbox_tool > a')
            u_cbox_btn_reply.click()
            driver.execute_script('arguments[0].scrollIntoView();', u_cbox_btn_reply)
            time.sleep(1)
            

            # 각댓글의 (15개의 베스트 탯글) 펼쳐놓은 '답글'의 더보기 버튼이 안나올때까지 모두 펼치기
            while True:
                try:
                    u_cbox_btn_more = elements[i].find_element(By.CSS_SELECTOR, value='div.u_cbox_reply_area > div:nth-child(3) > a')
                    u_cbox_btn_more.send_keys(Keys.ENTER)
                    driver.execute_script("arguments[0].scrollIntoView();", u_cbox_btn_more)
                    time.sleep(1)

                except StaleElementReferenceException:
                    elements =  driver.find_elements(by=By.CSS_SELECTOR, value='#cbox_module_wai_u_cbox_content_wrap_tabpanel > ul > li.u_cbox_comment')
                    time.sleep(1)

                except ElementNotInteractableException:
                    break
        except StaleElementReferenceException:
            elements =  driver.find_elements(by=By.CSS_SELECTOR, value='#cbox_module_wai_u_cbox_content_wrap_tabpanel > ul > li.u_cbox_comment')
            time.sleep(0.5)

        except NoSuchElementException:
            elements =  driver.find_elements(by=By.CSS_SELECTOR, value='#cbox_module_wai_u_cbox_content_wrap_tabpanel > ul > li.u_cbox_comment')
            time.sleep(0.5)

    
    for comment in elements:
        print('- ' * 70)
        # 댓글 출력
        if is_element_present_by_class_name(comment, 'u_cbox_contents'):
            print(comment.find_element(By.CLASS_NAME, value='u_cbox_contents').text)
        elif is_element_present_by_class_name(comment, 'u_cbox_cleanbot_contents'):
            print(comment.find_element(By.CLASS_NAME, value='u_cbox_cleanbot_contents').text)
        else:
            print('comment else case')

        # 답글
        u_cbox_reply_area = comment.find_element(By.CLASS_NAME, value='u_cbox_reply_area')

        # 답글 박스
        u_cbox_comment = u_cbox_reply_area.find_elements(By.CLASS_NAME, value='u_cbox_comment')

        # 답글 출력. 댓글과 요소 모양같음
        for c in u_cbox_comment:
            if is_element_present_by_class_name(c, 'u_cbox_contents'):
                print('ㄴ' + c.find_element(By.CLASS_NAME, value='u_cbox_contents').text)
            elif is_element_present_by_class_name(c, 'u_cbox_cleanbot_contents'):
                print('ㄴ' + c.find_element(By.CLASS_NAME, value='u_cbox_cleanbot_contents').text)
            else:
                print('comment else case')
        print()
except Exception as ex:
   print('에러이유 ' , ex)

driver.quit()
print()         

