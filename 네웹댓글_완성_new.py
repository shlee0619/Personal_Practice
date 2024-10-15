import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    ElementNotInteractableException,
)
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)


def get_comment_text(element):
    try:
        return element.find_element(By.CLASS_NAME, "u_cbox_contents").text
    except NoSuchElementException:
        try:
            return element.find_element(By.CLASS_NAME, "u_cbox_cleanbot_contents").text
        except NoSuchElementException:
            return "comment else case"


try:
    driver.get("https://comic.naver.com/webtoon/detail?titleId=769209&no=84")
    time.sleep(1)
    u_cbox_sort = driver.find_element(
        By.CSS_SELECTOR, "#cbox_module > div > div.u_cbox_sort"
    )
    driver.execute_script("arguments[0].scrollIntoView();", u_cbox_sort)
    elements = driver.find_elements(
        By.CSS_SELECTOR,
        "#cbox_module_wai_u_cbox_content_wrap_tabpanel > ul > li.u_cbox_comment",
    )

    for element in elements[:2]:
        try:
            # 답글 펼치기
            u_cbox_btn_reply = element.find_element(
                By.CSS_SELECTOR,
                "div.u_cbox_comment_box > div > div.u_cbox_tool > a",
            )
            u_cbox_btn_reply.click()
            driver.execute_script("arguments[0].scrollIntoView();", u_cbox_btn_reply)
            time.sleep(1)
            # 답글의 더보기 버튼 클릭
            while True:
                try:
                    u_cbox_btn_more = element.find_element(
                        By.CSS_SELECTOR,
                        "div.u_cbox_reply_area > div:nth-child(3) > a",
                    )
                    u_cbox_btn_more.click()
                    driver.execute_script(
                        "arguments[0].scrollIntoView();", u_cbox_btn_more
                    )
                    time.sleep(1)
                except (ElementNotInteractableException, NoSuchElementException):
                    break
        except (StaleElementReferenceException, NoSuchElementException):
            elements = driver.find_elements(
                By.CSS_SELECTOR,
                "#cbox_module_wai_u_cbox_content_wrap_tabpanel > ul > li.u_cbox_comment",
            )
            time.sleep(0.5)
            continue

    for comment in elements:
        print("- " * 70)
        print(get_comment_text(comment))
        try:
            replies = comment.find_element(
                By.CLASS_NAME, "u_cbox_reply_area"
            ).find_elements(By.CLASS_NAME, "u_cbox_comment")
            for reply in replies:
                print("ㄴ" + get_comment_text(reply))
        except NoSuchElementException:
            pass
        print()
except Exception as ex:
    print("에러이유", ex)

driver.quit()
