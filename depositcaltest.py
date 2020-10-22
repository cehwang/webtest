# -*- coding: utf-8 -*-
import math
import os
from beautifultable import BeautifulTable
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from gspreadAPI import GC, TESTCASE_CAL_URL
import json

doc = GC.open_by_url(TESTCASE_CAL_URL)
deposit_tc = doc.worksheet('예금계산기')
sum_pass = 0
sum_fail = 0
total = len(deposit_tc.col_values(1)) - 1
sum_nt = 0

key = deposit_tc.row_values(1)
col = len(key)

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://banksalad.com/deposits/calculator')


def screenshot(x, web_driver):
    file_dir = "screenshots/depositcaltest/"
    if x < 10:
        screenshot_name = "deposit_cal_test00" + str(x) + "_fail.png_" + datetime.today().strftime(
            "%Y%m%d%H%M") + ".png"
    else:
        screenshot_name = "deposit_cal_test0" + str(x) + "_fail.png_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"

    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
    except OSError:
        print("Error: Creating directory.")
        return False
    web_driver.save_screenshot(file_dir + screenshot_name)


def tc_to_json():
    value = deposit_tc.row_values(i + 1)

    str_json = '{'

    for x in range(0, col):
        if x != 0:
            str_json += ", "
        str_json += '"' + key[x] + '": "' + value[x] + '"'
    str_json += "}"

    return json.loads(str_json)


def page_load():
    global sum_nt, sum_fail

    timeout = 10
    try:
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(1) > div > div > input[type=text]"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        sum_fail += 1
        screenshot(i, driver)
        print("\x1b[1;31mFail\x1b[1;m - 예금계산기 화면이 정상적으로 로드되지 않았습니다.")
        return False


def input():
    global sum_nt, sum_fail

    # 입력 값 초기화
    try:
        money = driver.find_element(By.CSS_SELECTOR,
                                    ".calculatorWrap_Fqfwi > div > div:nth-child(1) > div > div > input[type=text]")
        while True:
            if money.get_attribute("value") != '0':
                money.send_keys(' \b')
            if money.get_attribute("value") == '0':
                break
        period = driver.find_element(By.CSS_SELECTOR,
                                     ".calculatorWrap_Fqfwi > div > div:nth-child(2) > div > div > input[type=text]")
        while True:
            if period.get_attribute("value") != '0':
                period.send_keys(Keys.BACK_SPACE)
            if period.get_attribute("value") == '':
                break
        interest = driver.find_element(By.CSS_SELECTOR,
                                       ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.inputForm_LqSYE > div > input[type=text]")
        while True:
            if interest.get_attribute("value") != '0':
                interest.send_keys(Keys.BACK_SPACE)
            if interest.get_attribute("value") == '':
                break

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 값을 초기화하기 위한 항목을 찾지 못했습니다.")
        return False

    # 값 입력
    try:
        money.send_keys(tc_json["예치금"])
        period.send_keys(tc_json["가입기간"])
        interest.send_keys(tc_json["이자율"])

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 값을 입력하기 위한 항목을 찾지 못했습니다.")
        return False
    return True


def drop_select():
    global sum_nt
    # 단리/복리 버튼 클릭
    try:
        select_button = tc_json["단/복리"]
        driver.find_element(By.CSS_SELECTOR,
                            ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.dropDownContainer_3NNNi > div > label").click()
        driver.find_element(By.CSS_SELECTOR,
                            ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.dropDownContainer_3NNNi > div > ul > li:nth-child(" + str(
                                select_button) + ") > button").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 단리/복리 클릭 버튼을 찾지 못했습니다.")
        return False
    return True


def result_confirm():
    # 원금 및 만기지급금액 일치 여부 확인
    global sum_fail, sum_nt, sum_pass
    try:
        result_interest = driver.find_element(By.CSS_SELECTOR,
                                              ".calculatorWrap_Fqfwi > div > div.resultContainer_1uMhk > div:nth-child(2) > div").text.replace(
            ",", "").replace("원", "")  # 하단 이자 값
        interest = driver.find_element(By.CSS_SELECTOR,
                                       ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.inputForm_LqSYE > div > input[type=text]").get_attribute(
            "value")  # 이자 입력 값
        money = driver.find_element(By.CSS_SELECTOR,
                                    ".calculatorWrap_Fqfwi > div > div:nth-child(1) > div > div > input[type=text]").get_attribute(
            "value").replace(",", "")  # 예치금 입력 값
        result_money = driver.find_element(By.CSS_SELECTOR,
                                           ".calculatorWrap_Fqfwi > div > div.resultContainer_1uMhk > div:nth-child(1) > div").text.replace(
            ",", "").replace("원", "")  # 원금 값

        # 예치금액 입력값과 하단 원금 일치여부 확인
        if result_money != money:
            print("\x1b[1;31mFail\x1b[1;m - 원금이 일치하지 않습니다.")
            print("기대결과 : " + result_money)
            print("실제결과 : " + money)
            sum_fail += 1
            return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 원금 확인을 위한 항목을 찾지 못했습니다.")
        return False

    try:
        select_button_text = driver.find_element(By.CSS_SELECTOR,
                                                 ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.dropDownContainer_3NNNi > div > label").text  # 복리, 단리 클릭
        period = driver.find_element(By.CSS_SELECTOR,
                                     ".calculatorWrap_Fqfwi > div > div:nth-child(2) > div > div > input[type=text]").get_attribute(
            "value")  # 기간 입력 값
        expired_payment_amount = driver.find_element(By.CSS_SELECTOR,
                                                     ".calculatorWrap_Fqfwi > div > div.option_VmIHA.resultAmount_3pRs4 > div > div > input[type=text]").get_attribute(
            "value").replace(",", "")  # 만기 지급금액 값

        monthlyInterestRate = float(interest) / 12 / 100

        # 만기금액 결과 일치여부 확인
        if select_button_text == '단리':
            simple = (int(money) * (1 + int(period) * float(monthlyInterestRate)))
            if round(simple) != int(expired_payment_amount):
                print("\x1b[1;31mFail\x1b[1;m - 만기지급금액이 일치하지 않습니다.")
                print("기대결과 : " + str(simple))
                print("실제결과 : " + expired_payment_amount)
                sum_fail += 1
                return False

        if select_button_text == '복리':
            compound = (int(money) * (1 + (math.pow((1 + float(monthlyInterestRate)), int(period)) - 1)))
            if round(compound) != int(expired_payment_amount):
                print("\x1b[1;31mFail\x1b[1;m - 만기지급금액이 일치하지 않습니다.")
                print("기대결과 : " + str(compound))
                print("실제결과 : " + expired_payment_amount)
                sum_fail += 1
                return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 만기지급금액 결과 확인을 위한 항목을 찾지 못했습니다.")
        return False

    try:
        # 이자 금액 확인
        if (int(expired_payment_amount) - int(result_money)) != int(result_interest):
            print("\x1b[1;31mFail\x1b[1;m - 이자금액이 일치하지 않습니다.")
            print("기대결과 : " + str(result_interest))
            print("실제결과 : " + str(int(expired_payment_amount) - int(result_money)))
            sum_fail += 1
            return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 만기지급금액 결과 확인을 위한 항목을 찾지 못했습니다.")
        return False
    return True


def saving_cal_button():
    # 적금계산기도 써보기 버튼 클릭
    global sum_nt, sum_fail, sum_pass, total
    try:
        print("적금 계산기도 써보기 페이지 클릭 Running...")
        driver.find_element(By.CSS_SELECTOR,
                            "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.bottom_3nZP1 > div > a").click()
        saving_cal_tab = driver.window_handles[1]
        driver.switch_to.window(window_name=saving_cal_tab)
        total += 1

        if driver.current_url != "https://banksalad.com/savings/calculator":
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 적금 계산기도 써보기 버튼 클릭시 잘못된 url로 이동합니다.")
            print("기대결과값: https://banksalad.com/savings/calculator")
            print("실제결과값: " + driver.current_url)
            first_tab = driver.window_handles[0]
            driver.switch_to.window(window_name=first_tab)
            return False

        first_tab = driver.window_handles[0]
        driver.switch_to.window(window_name=first_tab)
        print("\x1b[1;34mPass\x1b[1;m")
        sum_pass += 1

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 적금계산기도 써보기 버튼을 찾지 못했습니다.")
    return True


def deposit_button():
    # 지금 추천받기 버튼 클릭
    global sum_fail, sum_nt, sum_pass, total
    try:
        print("지금 추천받기 클릭 Running...")
        driver.find_element(By.CSS_SELECTOR,
                            "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.bottom_3nZP1 > a").click()
        deposit_tab = driver.window_handles[2]
        driver.switch_to.window(window_name=deposit_tab)
        total += 1

        if driver.current_url != "https://banksalad.com/deposits/questions":
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 지금 추천받기 버튼 클릭시 잘못된 url로 이동합니다.")
            print("기대결과값: https://banksalad.com/deposits/questions")
            print("실제결과값: " + driver.current_url)
            first_tab = driver.window_handles[0]
            driver.switch_to.window(window_name=first_tab)
            return False

        print("\x1b[1;34mPass\x1b[1;m")
        sum_pass += 1

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 지금 추천받기 버튼을 찾지 못했습니다.")
    return True


if not page_load():
    driver.refresh()

start = time.time()
print("------------------------테스트 시작------------------------")
for i in range(1, total + 1):

    if i < 10:
        print("depositcaltest00" + str(i) + " Running...")
    else:
        print("depositcaltest0" + str(i) + " Running...")

    tc_json = tc_to_json()

    if not input():
        continue
    if not drop_select():
        continue
    if not result_confirm():
        continue

    sum_pass += 1
    print("\x1b[1;34mPass\x1b[1;m")

saving_cal_button()
deposit_button()
driver.quit()

table = BeautifulTable()
table.column_headers = ["Total", "Pass", "Fail", "N/T"]
table.append_row([total, sum_pass, sum_fail, sum_nt])

print("------------------------테스트 결과------------------------")
print("실행 날짜: " + datetime.today().strftime("%Y-%m-%d"))
print("총 실행시간: " + str(int(time.time() - start)) + "s")
print("한 케이스당 평균 실행시간: " + str(int((time.time() - start) / total)) + "s")
print(table)
