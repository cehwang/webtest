# -*- coding: utf-8 -*-
import os
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from beautifultable import BeautifulTable
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from datetime import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait

sum_pass = 0
sum_fail = 0
total = 0
sum_nt = 0
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
Fail = "\x1b[1;31mFail\x1b[1;m"
Pass = "\x1b[1;34mPass\x1b[1;m"
Date = datetime.today().strftime("%Y%m%d%H%M")


def screenshot():
    file_dir = "screenshots/card10test/"

    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
    except OSError:
        print("Error: Creating directory.")
        return False

    driver.save_screenshot(file_dir + screenshot_name)


def filter_credit_check():
    global sum_nt, sum_fail
    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > label").location_once_scrolled_into_view  # 필터 위치까지 스크롤
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > label").click()  # 필터 선택
        sleep(1)
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 필터 버튼을 찾지 못했습니다.")
        return False

    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > ul > li:nth-child(1) > button"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        sum_fail += 1
        screenshot()
        print(f"{Fail} - 필터가 정상적으로 로드되지 않았습니다.")
        return False

    try:
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > ul > li:nth-child(1) > button").click()  # 신용/체크카드 필터 선택
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 필터 버튼을 선택하지 못했습니다.")
        return False
    return True


def filter_check():
    global sum_nt, sum_fail

    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > label").location_once_scrolled_into_view  # 필터 위치까지 스크롤
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > label").click()  # 필터 선택
        sleep(1)
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 필터 버튼을 찾지 못했습니다.")
        return False

    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > ul > li:nth-child(3) > button"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        sum_fail += 1
        screenshot()
        print(f"{Fail} - 필터가 정상적으로 로드되지 않았습니다.")
        return False

    try:
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > ul > li:nth-child(3) > button").click()  # 신용카드 필터 선택
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 필터 버튼을 선택하지 못했습니다.")
        return False
    return True


def title(i):
    global sum_fail, sum_nt
    try:
        driver.find_element(By.CSS_SELECTOR, f".cards_2AMVH > li:nth-child({str(i)}) >  div > section > div.buttons_2Q2OW > a").location_once_scrolled_into_view
        card_name = driver.find_element(By.CSS_SELECTOR, ".wrap_1y4z9 > div:nth-child(2) > ul > li:nth-child(" + str(i) + ") > div > h4").text
        driver.find_element(By.CSS_SELECTOR, f".cards_2AMVH > li:nth-child({str(i)}) >  div > section > div.buttons_2Q2OW > a").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 페이지 이동 버튼을 찾지 못했습니다.")
        return False

    timeout = 20
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "#wrap > div > div:nth-child(1) > div.back_u8cSA > section.cover_s55z6 > div > h4"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        sum_fail += 1
        screenshot()
        print(f"{Fail} - 카드 상세 페이지가 정상적으로 로드되지 않았습니다.")
        driver.back()
        return False
    try:
        sleep(1)
        title = driver.title.replace(" - ", "").replace(" 혜택 | 뱅크샐러드", "")
        if str(card_name) != str(title):  # 카드명과 상세페이지의 title이 불일치할 경우 fail
            sum_fail += 1
            screenshot()
            print(f"{Fail} - 올바른 상세 페이지로 이동하지 않습니다.")
            print(f"카드 명 : {card_name}")
            print(f"페이지 title : {title}")
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 상세보기 버튼을 찾지 못했습니다.")
        return False
    return True


def main(i):
    global sum_nt, sum_fail

    try:
        driver.find_element(By.LINK_TEXT, "뱅크샐러드 메인으로").location_once_scrolled_into_view

        if i == 10:
            driver.find_element(By.LINK_TEXT, "뱅크샐러드 메인으로").click()
            if driver.current_url != "https://banksalad.com/":
                screenshot()
                sum_fail += 1
                print(f"{Fail} - 뱅크샐러드 메인으로 버튼 클릭시 잘못된 url로 이동합니다.")
                print("기대결과값: https://banksalad.com/")
                print(f"실제결과값: {driver.current_url}")
                return False
            driver.back()

        driver.back()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - \'뱅크샐러드 메인으로\' 버튼을 찾지 못했습니다.")
        return False
    return True


def page_load():
    global sum_fail
    timeout = 20
    try:
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".wrap_1y4z9 > div:nth-child(2) > ul > li:nth-child(1) > div > span"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        sum_fail += 1
        screenshot()
        print(f"{Fail} - 페이지가 정상적으로 로드되지 않았습니다.")
        driver.refresh()
        return False
    return True


def card_type():
    global sum_fail, sum_nt
    try:
        driver.find_element(By.CSS_SELECTOR, f".wrap_1y4z9 > div:nth-child(2) > ul > li:nth-child({str(j)}) > div > h4").location_once_scrolled_into_view
        card_type = driver.find_element(By.CSS_SELECTOR, f".wrap_1y4z9 > div:nth-child(2) > ul > li:nth-child({str(j)}) > div > span").text
        if i == 1:
            if card_type != '신용':
                screenshot()
                print(f"신용카드 {str(j)}위 {Fail} - 카드 종류가 일치하지 않습니다.")
                print(f"기대결과 : 신용")
                print(f"실제결과 : {card_type}")
                sum_fail += 1
                return False

        if i == 2:
            if card_type == '신용' or card_type == '체크':
                return True
            else:
                screenshot()
                print(f"신용카드 {str(j)}위 {Fail} - 카드 종류가 일치하지 않습니다.")
                print("기대결과 : 신용 또는 체크")
                print(f"실제결과 : {card_type}")
                sum_fail += 1
                return False

        if i == 3:
            if card_type != '체크':
                screenshot()
                print(f"체크카드 {str(j)}위 {Fail} - 카드 종류가 일치하지 않습니다.")
                print("기대결과 : 체크")
                print(f"실제결과 : {card_type}")
                sum_fail += 1
                return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 인기카드10 항목을 찾지 못했습니다.")
        return False
    return True


driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://banksalad.com/cards/ranking')
start = time.time()
print("------------------------테스트 시작------------------------")
for i in range(1, 4):
    for j in range(1, 11):
        total += 1
        if not page_load():
            continue
        if i == 1:
            print(f"card10test00{str(j)} (credit) Running...")
            screenshot_name = f"card10test00{str(j)} (credit)_fail_{Date}.png"
        if i == 2:
            print(f"card10test0{str(j+10)} (credit/check) Running...")
            screenshot_name = f"card10test00{str(j+10)} (credit/check)_fail_{Date}.png"
        if i == 3:
            print(f"card10test0{str(j+20)} (check) Running...")
            screenshot_name = f"card10test00{str(j+20)} (check)_fail_{Date}.png"

        if i == 2:  # i가 2일 경우: 신용/체크카드 필터 선택
            if not filter_credit_check():
                continue
            if not page_load():
                continue

        if i == 3:  # i가 3일 경우: 체크카드 필터 선택
            if not filter_check():
                continue
            if not page_load():
                continue

        if not card_type():
            continue

        if not title(j):
            continue

        if not main(j):
            continue

        sum_pass += 1
        print(Pass)
driver.quit()

table = BeautifulTable()
table.column_headers = ["Total", "Pass", "Fail", "N/T"]
table.append_row([total, sum_pass, sum_fail, sum_nt])
print("------------------------테스트 결과------------------------")
print(f"실행 날짜: {Date}")
print(f"총 실행시간: {str(int(time.time() - start))}s")
print(f"한 케이스당 평균 실행시간: {str(int((time.time() - start)/total))}s")
print(table)
