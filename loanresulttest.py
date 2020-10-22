# -*- coding: utf-8 -*-
import os
from time import sleep
from beautifultable import BeautifulTable
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from datetime import datetime
import time
from gspreadAPI import GC, TESTCASE_LOAN_URL
import json

doc = GC.open_by_url(TESTCASE_LOAN_URL)
loan_result_tc = doc.worksheet('대출 Result TestCase')
sum_pass = 0
sum_fail = 0
total = len(loan_result_tc.col_values(1)) - 1
sum_nt = 0

key = loan_result_tc.row_values(1)
col = len(key)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")


def tc_to_json():
    value = loan_result_tc.row_values(i + 1)

    str_json = '{'
    for x in range(0, col):

        if x != 0:
            str_json += ", "
        str_json += '"' + key[x] + '": "' + value[x] + '"'
    str_json += "}"
    return json.loads(str_json)


def loan_select():
    global sum_nt
    try:
        # 희망 대출금액
        driver.find_element(By.CSS_SELECTOR, ":nth-child(2) > :nth-child(1) > ul > :nth-child(7) > button").click()
        # 신용등급 선택
        driver.find_element(By.CSS_SELECTOR, "label > span").click()
        driver.find_element(By.CSS_SELECTOR, "ul > :nth-child(1) > span").click()
        # 직업 선택
        driver.find_element(By.CSS_SELECTOR, ":nth-child(6) > div > button").click()
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".list_2C8C4 > li:nth-child(5) > label").click()
        driver.find_element(By.CSS_SELECTOR, ".accept_3yeys").click()
        # 연소득 선택
        driver.find_element(By.CSS_SELECTOR, ".preset_guXx3 > li:nth-child(7)").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 대출 입력화면의 버튼을 찾지 못했습니다.")
        return False
    return True


def check_reset():
    global sum_nt
    try:
        # 결과페이지 체크 초기화
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(1) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(2) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(4) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(5) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(8) > ul > :nth-child(1) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(8) > ul > :nth-child(2) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(10) > ul > :nth-child(1) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(10) > ul > :nth-child(2) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(10) > ul > :nth-child(3) > div").click()

    except NoSuchElementException:
        sum_nt += 1
        screenshot(i, driver)
        print("NT - 대출 결과화면 초기화 시 버튼을 찾지 못했습니다.")
        return False
    return True


def check_fin():
    global sum_nt
    try:
        # 금융사 선택
        fin = tc_json["금융사"].split(", ")
        for x in range(0, len(fin)):
            driver.find_element(By.XPATH, "//label[@class='label_fpNum' and contains(text(), '" + fin[x] + "')]").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 금융사 선택 버튼을 찾지 못했습니다.")
        return False
    return True


def check_add_select():
    global sum_nt

    try:
        add_select = tc_json["추가선택"].split(", ")
        for x in range(0, len(add_select)):
            driver.find_element(By.XPATH, "//label[@class='label_fpNum' and contains(text(), '" + add_select[x] + "')]").click()
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 추가사항 선택 버튼을 찾지 못했습니다.")
        return False
    return True


def check_rate_method():
    global sum_nt

    try:
        # 금리방식 선택
        rate = tc_json["금리방식"].split(", ")
        for x in range(0, len(rate)):
            driver.find_element(By.XPATH, "//label[@class='label_fpNum' and contains(text(), '" + rate[x] + "')]").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 금리방식 선택 버튼을 찾지 못했습니다.")
        return False
    return True


def check_repayment_method():
    global sum_nt

    try:
        # 상환방법 선택
        re_method = tc_json["상환방법"].split(", ")
        for x in range(0, len(re_method)):
            driver.find_element(By.XPATH, "//label[@class='label_fpNum' and contains(text(), '" + re_method[x] + "')]").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 상환방법 선택 버튼을 찾지 못했습니다.")
        return False
    return True


def check_primerate():
    global sum_nt

    try:
        # 우대금리 선택
        prime = tc_json["우대금리"].split(", ")
        for x in range(0, len(prime)):
            driver.find_element(By.XPATH,"//label[@class='label_fpNum' and contains(text(), '" + prime[x] + "')]").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 우대금리 선택 버튼을 찾지 못했습니다.")
        return False
    return True


def screenshot(x, web_driver):
    file_dir = "screenshots/loanresulttest/"
    screenshot_name = "loanresulttest" + str(x) + "_fail.png_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"

    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
    except OSError:
        print("Error: Creating directory.")
        return False

    web_driver.save_screenshot(file_dir + screenshot_name)


# 결과 화면에 금리방식 노출 확인
def confirm_rate_method(i):
    global sum_nt, sum_fail
    try:
        num = len(i)
        rate = tc_json["금리방식"].split(", ")
        if rate != "":
            if num > 1:
                for x in range(1, 3):
                    for y in range(1, len(rate)):
                        if str(rate) not in i[x].text:
                            sum_fail += 1
                            print("\x1b[1;31mFail\x1b[1;m - 선택한 금리방식이 결과에 노출되지 않습니다.")  # Fail 빨간색 글씨
                            screenshot(i, driver)
                            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과페이지에 노출되는 금리방식 항목을 찾지 못했습니다.")
        return False

    return True


# 결과 화면에 상환방법 노출 확인
def confirm_repayment_method(i):
    global sum_nt, sum_fail
    num = len(i)

    try:
        re_method = tc_json['상환방법'].split(", ")
        if num > 1:
            if re_method != "":
                for x in range(1, 3):
                    for y in range(1, len(re_method)):
                        if str(re_method) not in i[x].text:
                            sum_fail += 1
                            print("\x1b[1;31mFail\x1b[1;m - 선택한 상환방법이 결과에 노출되지 않습니다.")  # Fail 빨간색 글씨
                            screenshot(i, driver)
                            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과페이지에 노출되는 상환방법 항목을 찾지 못했습니다.")
        return False
    return True


# 결과 화면에 중도상환수수료 노출 확인
def confirm_prepayment(i):
    global sum_fail, sum_nt
    num = len(i)
    add_select = tc_json["추가선택"].split(", ")
    try:
        if num > 1:
            if add_select != "":
                for x in range(1, 3):
                    for y in range(1, len(add_select)):
                        if str(add_select) not in i[x].text:
                            sum_fail += 1
                            print("\x1b[1;31mFail\x1b[1;m - 선택한 중도상환수수료가 결과에 노출되지 않습니다.")  # Fail 빨간색 글씨
                            screenshot(i, driver)
                            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과페이지에 노출되는 추가선택(이벤트/당일대출/중도상환수수료) 항목을 찾지 못했습니다.")
        return False
    return True


start = time.time()
print("------------------------테스트 시작------------------------")

for i in range(1, total + 1):

    if i < 10:
        print("loanresulttest00" + str(i) + " Running...")
    else:
        print("loanresulttest0" + str(i) + " Running...")

    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
    driver.get('https://banksalad.com/credit-loans/questions')

    tc_json = tc_to_json()

    if not loan_select():
        driver.quit()
        continue

    sleep(1)

    loan_result = driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(1) > .value_3k1fw").text.replace(",", "")
    loan_result = loan_result.replace("만원", "")
    loan_expect = driver.find_element(By.CSS_SELECTOR, "div.preview_Qee0B > div.foot_2aDGD > section > span.resultValue_rynW5 > span").text.replace(",", "").replace("예상 대출한도 ", "").replace("만원", "")

    try:
        alert = driver.find_element(By.LINK_TEXT, "결과보기").click()
        sleep(1)

    except NoSuchElementException:
        print("N/T - \'결과보기\' 버튼을 찾지 못했습니다.")
        sum_nt += 1
        driver.quit()
        continue

    # 희망 대출금액이 예상 한도보다 낮은 경우 노출되는 alert 처리
    if int(loan_result) > int(loan_expect):

        try:
            alert_switch = driver.switch_to.alert
            alert_text = alert_switch.text.replace(",", "")  # alert에 노출되는 문구
            alert_switch.accept()
            sleep(1)

        except NoSuchElementException:
            print("N/T - \'alert\' 항목을 찾지 못했습니다.")
            sum_nt += 1
            driver.quit()
            continue

        if not check_reset():
            driver.quit()
            continue

    else:
        # 희망 대출금액이 예상한도보다 높은 경우 동작
        if not check_reset():
            driver.quit()
            continue

    check_fin()
    check_add_select()
    check_rate_method()
    check_repayment_method()
    check_primerate()

    sleep(2)
    loan_div = driver.find_elements(By.CLASS_NAME, "resultItem_2jgVP")

    if len(loan_div) == 0:
        screenshot(i, driver)
        sum_nt += 1
        print("NT - 상품이 노출되지 않습니다.")
        driver.quit()
        continue

    loan_div[0].location_once_scrolled_into_view

    if not confirm_rate_method(loan_div):
        driver.quit()
        continue

    if not confirm_repayment_method(loan_div):
        driver.quit()
        continue

    if not confirm_prepayment(loan_div):
        driver.quit()
        continue

    sleep(1)
    sum_pass += 1
    print("\x1b[1;34mPass\x1b[1;m")

    driver.quit()
table = BeautifulTable()
table.column_headers = ["Total", "Pass", "Fail", "N/T"]
table.append_row([total, sum_pass, sum_fail, sum_nt])

print("------------------------테스트 결과------------------------")
print("실행 날짜: " + datetime.today().strftime("%Y-%m-%d"))
print("총 실행시간: " + str(int(time.time() - start)) + "s")
print("한 케이스당 평균 실행시간: " + str(int((time.time() - start)/total)) + "s")
print(table)
