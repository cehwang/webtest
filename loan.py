# -*- coding: utf-8 -*-
import os
from time import sleep
from beautifultable import BeautifulTable
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from datetime import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
from gspreadAPI import GC, TESTCASE_LOAN_URL
import json

doc = GC.open_by_url(TESTCASE_LOAN_URL)
loan_tc = doc.worksheet("BEST 대출 TestCase")
sum_pass = 0
sum_fail = 0
total = len(loan_tc.col_values(1)) - 1
sum_nt = 0

key = loan_tc.row_values(1)
col = len(key)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")


def tc_to_json():
    value = loan_tc.row_values(i + 1)

    str_json = '{'
    for x in range(0, col):
        if x != 0:
            str_json += ", "
        str_json += '"' + key[x] + '": "' + value[x] + '"'
    str_json += "}"

    return json.loads(str_json)


def screenshot(x, web_driver):
    file_dir = "screenshots/loantest/"
    if x < 10:
        screenshot_name = "loantest00" + str(x) + "_fail.png_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"
    else:
        screenshot_name = "loantest0" + str(x) + "_fail.png_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"

    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
    except OSError:
        print("Error: Creating directory.")
        return False

    web_driver.save_screenshot(file_dir + screenshot_name)


def loan_select(i, web_driver):
    global sum_nt, sum_fail

    # 대출 금액 버튼 선택
    try:
        web_driver.find_element(By.XPATH, "//button[@class='tag_KCNXn' and contains(text(), '" + str(tc_json["대출금액"]) + "')]").click()
        sleep(1)
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 희망 대출 금액 선택 버튼을 찾지 못했습니다.")
        return False

    # 선택한 대출 금액이 입력항목에 정상 노출되는지 확인
    try:
        loan_result = driver.find_element(By.CSS_SELECTOR,".questions_3ScUv > li:nth-child(1) > .value_3k1fw").text.replace(",", "").replace("만원", "")
        loan_input = web_driver.find_element(By.CSS_SELECTOR, ".amount_3x6iq > .desktop_1HAhS > div > input").get_attribute('value')
        sleep(2)
        if loan_input != loan_result:
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 희망 대출 금액 버튼을 클릭했을 때, 입력 결과에 해당 금액이 정상적으로 노출되지 않습니다.")  # Fail 빨간색 글씨
            print("입력 값: " + str(loan_input) + ", 결과 값: " + str(loan_result))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 희망 대출 금액 버튼을 클릭했을 때, 입력 결과 항목을 찾지 못했습니다.")
        return False
    return True


def loan_credit(i, web_driver):
    global sum_nt, sum_fail

    # 신용등급 선택
    try:
        web_driver.find_element(By.CSS_SELECTOR, "label > span").click()
        sleep(1)
        web_driver.find_element(By.XPATH, "//span[@class='item_1x2gS' and contains(text(), '" + str(tc_json["신용등급"]) + "')]").click()
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 신용등급 선택창을 찾지 못했습니다.")
        return False

    # 신용등급 입력 결과 확인
    try:
        creditlevel = web_driver.find_element(By.CSS_SELECTOR, "label > span").text
        credit_result = web_driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(2) > .value_3k1fw").text
        if str(credit_result) != str(creditlevel):
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 신용등급 선택 시, 입력 결과에 선택 사항이 정상적으로 노출되지 않습니다.")  # Fail 빨간색 글씨
            print("입력: " + str(creditlevel) + ", 결과: " + str(credit_result))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 신용등급 선택창과 입력 결과 항목을 찾지 못했습니다.")
        return False

    return True


def loan_job(i, web_driver):
    global sum_nt, sum_fail

    # 직업 선택
    try:
        web_driver.find_element(By.CSS_SELECTOR, ":nth-child(6) > div > button").click()
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 직업 선택 버튼을 선택하지 못했습니다.")
        return False

    # 직업 선택 팝업이 5초 안에 노출되지 않으면 fail
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".list_2C8C4 > li:nth-child(1) > label"))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        sum_fail += 1
        screenshot(i, driver)
        print("\x1b[1;31mFail\x1b[1;m - 직업 선택 팝업이 정상적으로 노출되지 않았습니다.")
        driver.quit()
        return False

    try:
        driver.find_element(By.XPATH, "//label[contains(text(), '" + tc_json["직업"] + "')]").location_once_scrolled_into_view
        driver.find_element(By.XPATH, "//label[contains(text(), '" + tc_json["직업"] + "')]").click()
        driver.find_element(By.CSS_SELECTOR, ".accept_3yeys").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 직업 선택 버튼을 찾지 못했습니다.")
        return False

    # 선택한 직업이 입력항목에 정상 노출되는지 확인
    try:
        job_name = web_driver.find_element(By.CSS_SELECTOR, ":nth-child(6) > div > button").text
        job_result = web_driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(3) > .value_3k1fw").text
        if str(job_name) != str(job_result):
            print("\x1b[1;31mFail\x1b[1;m - 직업 선택 시, 입력 결과에 선택 사항이 정상적으로 노출되지 않습니다.")  # Fail 빨간색 글씨
            print("선택: " + str(job_name) + ", 결과: " + str(job_result))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 직업을 선택했을 때, 입력 결과 항목을 찾지 못했습니다.")
        return False

    return True


def loan_income(i, web_driver):
    global sum_nt, sum_fail

    # 연소득 선택
    try:
        web_driver.find_element(By.XPATH, "//button[@class='tag_G72-i' and contains(text(), '" + str(tc_json["연소득"]) + "')]").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 연소득 선택 항목을 찾지 못했습니다.")
        return False

    # 선택한 연소득이 입력항목에 정상 노출되는지 확인
    try:
        input_income = int(web_driver.find_element(By.CSS_SELECTOR, ".amount_1_jHL > .desktop_1HAhS > div > input").get_attribute('value'))
        income_result = web_driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(4) > .value_3k1fw").text.replace(",", "")
        income_result = income_result.replace("만원", "")
        if input_income != int(income_result):
            print("\x1b[1;31mFail\x1b[1;m - 연소득 선택 시, 입력 결과에 선택 사항이 정상적으로 노출되지 않습니다.")  # Fail 빨간색 글씨
            print("입력값: " + str(input_income) + ", 결과값: " + str(income_result))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 연소득을 선택했을 때, 입력 결과를 찾지 못했습니다.")
        return False
    return True


# 선택한 희망 대출금액이 상단 금액과 일치하는지 확인
def loan_hope(i, web_driver):
    global sum_nt, sum_fail

    try:
        loan_text = web_driver.find_element(By.CSS_SELECTOR, "#amount").get_attribute('value')
        if get_loan_result != loan_text:
            print("\x1b[1;31mFail\x1b[1;m - 희망 대출금액이 결과 페이지 상단 금액과 일치하지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(get_loan_result) + ", 실제결과값: " + str(loan_text))
            screenshot(i, driver)
            return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과 페이지 상단 금액을 찾지 못했습니다.")
        return False
    return True


# 예상한도가 결과페이지 첫번째 상품에 노출되는 금액과 동일한지 확인
def expect_limit():
    global sum_nt
    try:
        loan_expect_result_list = driver.find_element(By.CSS_SELECTOR, ".calculatedInterest_2MmE7").text.replace(",", "").replace("예상한도 ", "").replace("만원", "")  # 결과 페이지의 첫번째 상품 한도
        sleep(1)
        if int(loan_expect) != int(loan_expect_result_list):
            print("\x1b[1;31mFail\x1b[1;m - 희망 대출금액이 결과 페이지 상단 금액과 일치하지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(loan_expect) + ", 실제결과값: " + str(loan_expect_result_list))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과페이지 첫 번째 상품의 예상한도를 찾지 못했습니다.")
        return False
    return True


# 결과 리스트 로드 timeout 시 fail처리
def load_loan():
    global sum_nt, sum_fail
    wait = 0
    for x in range(1, 4):
        while True:
            # 20번 기다렸는데도 load되지 않았을때, timeout처리
            if wait > 20:
                screenshot(i, driver)
                print("\x1b[1;31mFail\x1b[1;m - 결과 리스트 로드 timeout")
                sum_fail += 1
                return False
            elements = driver.find_elements(By.CSS_SELECTOR, ".resultItem_2jgVP")
            num = len(elements)
            if num > 0:
                break
            sleep(1)
            wait += 1
        if num == x * 10:
            elements[x * 10 - 1].location_once_scrolled_into_view
            sleep(2)
        else:
            elements[num - 1].location_once_scrolled_into_view
            sleep(2)
            break
    return True


# 상품 상세페이지 확인
def confirm_detail():
    global sum_fail, sum_nt
    num = len(driver.find_elements(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol:nth-child(2) > li"))
    wait = 0
    if num > 2:
        num = 2
    for x in range(0, num):
        while True:
            if wait > 20:
                screenshot(i, driver)
                print("\x1b[1;31mFail\x1b[1;m - 결과 리스트 로드 timeout")
                sum_fail += 1
                return False
            lst_loan = driver.find_elements(By.CSS_SELECTOR, ".resultItem_2jgVP")

            if len(lst_loan) > 0:
                break

            sleep(1)
            wait += 1

        loan_name1 = driver.find_elements(By.CSS_SELECTOR, ".headerText_SOgCc > h1")[x].text.replace("고정금리", "").replace("변동금리", "")
        loan_detail = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(x + 1) + ") > div > div.body_cYC3y > div > div.linkButtons_3eD-d > a.linkDetail_2YWx8.linkButton_3mX1p")
        lst_loan[x].location_once_scrolled_into_view
        sleep(1)
        loan_detail.click()

        # 상품 상세페이지 10초동안 로드되지 않은 경우 fail처리
        timeout = 10
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".head_25kNF > h1"))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            sum_fail += 1
            screenshot(i, driver)
            print("\x1b[1;31mFail\x1b[1;m - 상품 상세 페이지가 정상적으로 로드되지 않았습니다.")
            driver.quit()
            return False

        try:
            loan_name2 = driver.find_element(By.CSS_SELECTOR, ".head_25kNF > h1").text

            if loan_name1 != loan_name2:
                screenshot(i, driver)
                sum_fail += 1
                print("\x1b[1;31mFail\x1b[1;m - 잘못된 상세페이지로 이동")
                print("기대결과값: " + loan_name1 + "의 상세페이지, 실제결과값: " + loan_name2 + "의 상세페이지")
                return False

            # 결과리스트가 10초동안 로드되지 않은 경우 fail 처리
            wait = 0
            if wait > 10:
                screenshot(i, driver)
                print("\x1b[1;31mFail\x1b[1;m - 결과 리스트 로드 timeout")
                sum_fail += 1
                return False

            if len(driver.find_elements(By.CLASS_NAME, "resultItem_2jgVP")) > 0:
                break

            driver.find_element(By.LINK_TEXT, "결과 리스트로").click()
            sleep(2)
            if driver.current_url != "https://banksalad.com/credit-loans/profits":
                screenshot(i, driver)
                sum_fail += 1
                print("\x1b[1;31mFail\x1b[1;m - 결과 리스트로 버튼 클릭시 잘못된 url로 이동")
                print("기대결과값: https://banksalad.com/credit-loans/profits")
                print("실제결과값: " + driver.current_url)
                return False

        except NoSuchElementException:
            sum_nt += 1
            print("N/T - 상품 상세보기 페이지 내 결과 리스트로 버튼 또는 상품 요소를 찾지못함")
            return False
    return True


# 금리 낮은 순 선택
def confirm_filter1(n):
    global sum_nt, sum_fail

    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div > ul > li:nth-child(1) > button").click()

        for i in range(1, n):
            sleep(2)
            result_list = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl  dd.interestInfo_r017q > ul > li:nth-child(1) > div > strong").text.replace("평균 ", "").replace("%", "")
            result_list2 = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i + 1) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl  dd.interestInfo_r017q > ul > li:nth-child(1) > div > strong").text.replace("평균 ", "").replace("%", "")
            if float(result_list) > float(result_list2):
                print("\x1b[1;31mFail\x1b[1;m - 금리 낮은 순 필터가 정상적으로 동작하지 않습니다.")
                sum_fail += 1
                return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 금리 낮은 순 필터 관련 항목을 찾지 못했습니다.")
        return False
    return True


# 한도 높은 순 선택
def confirm_filter2(n):
    global sum_fail, sum_nt

    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div > ul > li:nth-child(2) > button").click()

        for i in range(1, n):
            sleep(2)
            result_list = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl > dd.interestInfo_r017q > ul > li.calculatedInterestWrap_1QJa1 > span.calculatedInterest_2MmE7").text.replace("예상한도 ", "").replace(",", "").replace("만원", "")
            result_list2 = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i + 1) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl > dd.interestInfo_r017q > ul > li.calculatedInterestWrap_1QJa1 > span.calculatedInterest_2MmE7").text.replace("예상한도 ", "").replace(",", "").replace("만원", "")
            if int(result_list) < int(result_list2):
                print("\x1b[1;31mFail\x1b[1;m - 한도 높은 순 필터가 정상적으로 동작하지 않습니다.")
                sum_fail += 1
                return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 한도 높은 순 필터 관련 항목을 찾지 못했습니다.")
        return False
    return True


# 최장 기간 순 선택
def confirm_filter3(n):
    global sum_nt, sum_fail
    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR,
                            ".desktop_1HAhS > ul > li:nth-child(3) > div > ul > li:nth-child(3) > button").click()

        for i in range(1, n):
            sleep(2)
            result_list = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl > dd:nth-child(4) > ul > li > span").text
            result_list2 = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i + 1) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl > dd:nth-child(4) > ul > li > span").text
            split1 = result_list.split('~', 2)
            split2 = split1[1].split('개월', 2)
            split3 = result_list2.split('~', 2)
            split4 = split3[1].split('개월', 2)
            if int(split2[0]) < int(split4[0]):
                print("\x1b[1;31mFail\x1b[1;m - 한도 높은 순 필터가 정상적으로 동작하지 않습니다.")
                sum_fail += 1
                return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 최장기간 순 필터 관련 항목을 찾지 못했습니다.")
        return False
    return True


def result_credit():
    global sum_nt, sum_fail
    # 선택한 신용등급과 결과페이지 상단 신용등급 일치 여부 확인
    try:
        result_creditlevel = driver.find_element(By.CSS_SELECTOR,".desktop_1HAhS > ul > li:nth-child(1) > div > ""label").text
        if creditlevel != result_creditlevel:
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 신용등급이 결과 페이지 상단과 일치하지 않습니다.")
            print("기대결과값: " + str(creditlevel) + ", 실제결과값: " + str(result_creditlevel))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과페이지 상단 신용등급을 찾지 못했습니다.")
        driver.quit()
        return False
    return True


start = time.time()
print("------------------------테스트 시작------------------------")
for i in range(1, total + 1):
    if i < 10:
        print("loantest00" + str(i) + " Running...")
    else:
        print("loantest0" + str(i) + " Running...")

    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    driver.get('https://banksalad.com/credit-loans/questions')

    tc_json = tc_to_json()

    if not loan_select(i, driver):
        driver.quit()
        continue

    get_loan_result = driver.find_element(By.CSS_SELECTOR,".questions_3ScUv > li:nth-child(1) > .value_3k1fw").text.replace(",", "").replace("만원", "")

    if not loan_credit(i, driver):
        driver.quit()
        continue

    if not loan_job(i, driver):
        driver.quit()
        continue

    if not loan_income(i, driver):
        driver.quit()
        continue

    sleep(1)

    # 희망 대출 금액, 예상 대출 한도
    creditlevel = driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(2) > .value_3k1fw").text
    loan_expect = driver.find_element(By.CSS_SELECTOR, "div.preview_Qee0B > div.foot_2aDGD > section > span.resultValue_rynW5 > span").text.replace(",", "").replace("예상 대출한도 ", "").replace("만원", "")

    try:
        driver.find_element(By.LINK_TEXT, "결과보기").click()
        sleep(1)

    except NoSuchElementException:
        print("N/T - \'결과보기\' 버튼을 찾지 못했습니다.")
        sum_nt += 1
        driver.quit()
        continue

    # 희망 대출금액이 예상 한도보다 낮은 경우 노출되는 alert 처리
    if int(get_loan_result) > int(loan_expect):

        try:
            alert_switch = driver.switch_to.alert
            alert_text = alert_switch.text.replace(",", "")  # alert에 노출되는 문구
            alert_switch.accept()
            sleep(1)
            loan_text = int(driver.find_element(By.CSS_SELECTOR, "#amount").get_attribute('value'))  # 결과 페이지 상단 노출 금액

            # 결과 상단 희망금액이 alert 워딩에 포함되는지 확인
            if str(loan_text) not in alert_text:
                sum_fail += 1
                print("\x1b[1;31mFail\x1b[1;m - 희망 대출금액이 결과 페이지 상단 금액과 일치하지 않습니다.")  # Fail 빨간색 글씨
                print("\x1b[1;31malert 워딩에\x1b[1;m " + str(alert_text) + "\x1b[1;31m결과 페이지 상단 금액\x1b[1;m " + str(loan_text) + " 이 포함되지 않습니다.")
                screenshot(i, driver)
                continue

        except NoSuchElementException:
            print("N/T - \'결과페이지 상단 금액\' 항목을 찾지 못했습니다.")
            sum_nt += 1
            driver.quit()
            continue

    else:
        # 희망 대출금액이 예상한도보다 높은 경우 동작
        sleep(1)
        if not loan_hope(i, driver):
            driver.quit()
            continue

    if not expect_limit():
        driver.quit()
        continue

    if not result_credit():
        driver.quit()
        continue

    if not load_loan():
        driver.quit()
        continue

    if not confirm_detail():
        driver.quit()
        continue

    loan_div = driver.find_elements(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol:nth-child(2) > li")

    if not confirm_filter1(len(loan_div)):
        driver.quit()

    if not confirm_filter2(len(loan_div)):
        driver.quit()

    if not confirm_filter3(len(loan_div)):
        driver.quit()

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
