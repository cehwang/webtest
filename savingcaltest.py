# -*- coding: utf-8 -*-
import math
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from gspreadAPI import GC, TESTCASE_CAL_URL
from testresult import Test, result_table

doc = GC.open_by_url(TESTCASE_CAL_URL)
saving_tc = doc.worksheet('적금계산기')

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://banksalad.com/savings/calculator')


def tc_to_json(i: int) -> dict:
    key = saving_tc.row_values(1)
    col = len(key)
    value = saving_tc.row_values(i + 1)

    return {
        key[x]: value[x] for x in range(col)
    }


def deposit_cal_button(driver: webdriver, saving_cal_test: Test) -> bool:
    try:
        print("예금 계산기도 써보기 페이지 버튼 Running...")
        driver.find_element(By.CSS_SELECTOR,
                            "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.bottom_1qFyD > div > a").click()
        tab = driver.window_handles[1]
        driver.switch_to.window(window_name=tab)
        saving_cal_test.result_total()

        if driver.current_url != "https://banksalad.com/deposits/calculator":
            result = "예금 계산기도 써보기 버튼 클릭시 잘못된 url로 이동합니다.\n" \
                     "기대결과값: https://banksalad.com/deposits/calculator\n" \
                     f"실제결과값: {driver.current_url}"
            saving_cal_test.result_fail_no_quit(driver, result)
            first_tab = driver.window_handles[0]
            driver.switch_to.window(window_name=first_tab)
            return False

        first_tab = driver.window_handles[0]
        driver.switch_to.window(window_name=first_tab)

        Test.result_pass_no_quit(saving_cal_test)
    except NoSuchElementException:
        result = "예금계산기도 써보기 버튼을 찾지 못했습니다."
        Test.result_nt_no_quit(saving_cal_test, result)
    return True


def saving_buttion(driver: webdriver, saving_cal_test: Test) -> bool:
    try:
        print("지금 추천받기 버튼 Running...")
        driver.find_element(By.CSS_SELECTOR,
                            "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.bottom_1qFyD > a").click()
        tab = driver.window_handles[2]
        driver.switch_to.window(window_name=tab)
        saving_cal_test.result_total()

        if driver.current_url != "https://banksalad.com/savings/questions":
            result = "지금 추천받기 버튼 클릭시 잘못된 url로 이동합니다.\n" \
                     "기대결과값: https://banksalad.com/savings/questions\n" \
                     f"실제결과값: {driver.current_url}"
            saving_cal_test.result_fail_no_quit(driver, result)
            first_tab1 = driver.window_handles[0]
            driver.switch_to.window(window_name=first_tab1)
            return False

        saving_cal_test.result_pass(driver)
    except NoSuchElementException:
        result = "지금 추천받기 버튼을 찾지 못했습니다."
        Test.result_nt_no_quit(saving_cal_test, result)
    return True


def page_load(driver: webdriver, saving_cal_test: Test) -> bool:
    timeout = 10
    try:
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div:nth-child(1) > div > div > input[type=text]"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        result = "적금계산기 화면이 정상적으로 로드되지 않았습니다."
        saving_cal_test.result_fail_no_quit(driver, result)
        return False


def input(driver: webdriver, saving_cal_test: Test) -> bool:
    tc = saving_cal_test.get_tc()

    # 입력 값 초기화
    try:
        money = driver.find_element(By.CSS_SELECTOR,
                                    ".calculatorWrap_2RDVa > div > div:nth-child(1) > div > div > input[type=text]")
        while True:
            if money.get_attribute("value") != '0':
                money.send_keys(' \b')
            if money.get_attribute("value") == '0':
                break
        period = driver.find_element(By.CSS_SELECTOR,
                                     ".calculatorWrap_2RDVa > div > div:nth-child(2) > div > div > input[type=text]")
        while True:
            if period.get_attribute("value") != '0':
                period.send_keys(Keys.BACK_SPACE)
            if period.get_attribute("value") == '':
                break
        interest = driver.find_element(By.CSS_SELECTOR,
                                       ".calculatorWrap_2RDVa > div > div:nth-child(3) > div > div.inputForm_30zap > div > input[type=text]")
        while True:
            if interest.get_attribute("value") != '0':
                interest.send_keys(Keys.BACK_SPACE)
            if interest.get_attribute("value") == '':
                break

    except NoSuchElementException:
        result = "값을 초기화하기 위한 항목을 찾지 못했습니다."
        Test.result_nt_no_quit(saving_cal_test, result)
        return False

    # 값 입력
    try:
        money.send_keys(tc["납입금액"])
        period.send_keys(tc["가입기간"])
        interest.send_keys(tc["이자율"])

    except NoSuchElementException:
        result = "값을 입력하기 위한 항목을 찾지 못했습니다."
        Test.result_nt_no_quit(saving_cal_test, result)
        return False
    return True


def drop_select(driver: webdriver, saving_cal_test: Test) -> bool:
    tc = saving_cal_test.get_tc()
    # 단리/복리 버튼 선택
    try:
        select_button = tc["단/복리"]
        driver.find_element(By.CSS_SELECTOR,
                            ".calculatorWrap_2RDVa > div > div:nth-child(3) > div > div.dropDownContainer_YrgkD > div > label").click()
        driver.find_element(By.CSS_SELECTOR,
                            f".calculatorWrap_2RDVa > div > div:nth-child(3) > div > div.dropDownContainer_YrgkD > div > ul > li:nth-child({str(select_button)}) > button").click()
    except NoSuchElementException:
        result = "단리/복리 선택 버튼을 찾지 못했습니다."
        Test.result_nt_no_quit(saving_cal_test, result)
        return False
    return True


def result_confirm(driver: webdriver, saving_cal_test: Test) -> bool:
    # 가입기간 * 납입금액과 결과의 원금이 일치하는지 확인
    try:
        period = driver.find_element(By.CSS_SELECTOR,
                                     ".calculatorWrap_2RDVa > div > div:nth-child(2) > div > div > input[type=text]").get_attribute(
            "value")  # 가입기간
        money = driver.find_element(By.CSS_SELECTOR,
                                    ".calculatorWrap_2RDVa > div > div:nth-child(1) > div > div > input[type=text]").get_attribute(
            "value").replace(",", "")  # 월 납입금액
        result_money = driver.find_element(By.CSS_SELECTOR,
                                           ".calculatorWrap_2RDVa > div > div.resultContainer_1foXe > div:nth-child(1) > div").text.replace(
            ",", "").replace("원", "")  # 원금
        if int(result_money) != int(money) * int(period):
            result = "원금이 일치하지 않습니다.\n" \
                     f"기대결과 : {str(int(money) * int(period))}\n" \
                     f"실제결과 : {result_money}"
            saving_cal_test.result_fail_no_quit(driver, result)
            return False

    except NoSuchElementException:
        result = "원금 확인을 위한 항목을 찾지 못했습니다."
        Test.result_nt_no_quit(saving_cal_test, result)
        return False

    # 만기지급금액 일치여부 확인
    try:
        result_sum = driver.find_element(By.CSS_SELECTOR,
                                         ".calculatorWrap_2RDVa > div > div.option_blNaX.resultAmount_UmbNJ > div > div > input[type=text]").get_attribute(
            "value").replace(",", "")  # 만기지급금액
        interest = driver.find_element(By.CSS_SELECTOR,
                                       ".calculatorWrap_2RDVa > div > div:nth-child(3) > div > div.inputForm_30zap > div > input[type=text]").get_attribute(
            "value")  # 입력한 이자율
        select_button_text = driver.find_element(By.CSS_SELECTOR,
                                                 ".calculatorWrap_2RDVa > div > div:nth-child(3) > div > div.dropDownContainer_YrgkD > div > label").text  # 복리, 단리 확인

        monthlyInterestRate = ((float(interest) / 12 + 100) / 100)

        if select_button_text == '단리':
            simple = (((int(period) * int(money)) + (
                        int(period) * (int(period) + 1) / 2 * (float(monthlyInterestRate) - 1) * int(money))))
            if round(simple) != int(result_sum):
                result = "만기지급금액이 일치하지 않습니다.\n" \
                         f"기대결과 : {str(simple)}\n" \
                         f"실제결과 : {result_sum}"
                saving_cal_test.result_fail_no_quit(driver, result)
                return False

        if select_button_text == '복리':
            compound = (((int(money) * float(monthlyInterestRate) * (
                        math.pow((float(monthlyInterestRate)), int(period)) - 1) / (float(monthlyInterestRate) - 1))))
            if round(compound) != int(result_sum):
                result = "만기지급금액이 일치하지 않습니다.\n" \
                         f"기대결과 : {str(compound)}\n" \
                         f"실제결과 : {result_sum}"
                saving_cal_test.result_fail_no_quit(driver, result)
                return False

    except NoSuchElementException:
        result = "만기 지급금액 항목을 찾지 못했습니다."
        Test.result_nt_no_quit(saving_cal_test, result)
        return False

    # 이자(만기지급금액-원금) 일치여부 확인
    try:
        result_interest = driver.find_element(By.CSS_SELECTOR,
                                              "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.calculatorWrap_2RDVa > div > div.resultContainer_1foXe > div:nth-child(2) > div").text.replace(
            ",", "").replace("원", "")  # 만기 이자
        if (int(result_sum) - int(result_money)) != int(result_interest):
            result = "이자금액이 일치하지 않습니다.\n" \
                     f"기대결과 : {str(int(result_sum) - int(result_money))}\n" \
                     f"실제결과 : {str(int(result_interest))}"
            saving_cal_test.result_fail_no_quit(driver, result)
            return False
    except NoSuchElementException:
        result = "이자 항목을 찾지 못했습니다."
        Test.result_nt_no_quit(saving_cal_test, result)
        return False
    return True


def main():
    saving_cal_test = Test()
    saving_tc = doc.worksheet('적금계산기')
    saving_cal_test.set_total(len(saving_tc.col_values(1)) - 1)

    # 백그라운드 옵션
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("headless")

    print("------------------------테스트 시작------------------------")
    if not page_load(driver, saving_cal_test):
        driver.refresh()
    for i in range(1, saving_cal_test.get_total() + 1):

        saving_tc = tc_to_json(i)
        saving_cal_test.set_no(i)
        saving_cal_test.set_tc(saving_tc)
        print(f"{saving_tc['TC 명']} Running...")

        if not input(driver, saving_cal_test):
            continue
        if not drop_select(driver, saving_cal_test):
            continue
        if not result_confirm(driver, saving_cal_test):
            continue

        Test.result_pass_no_quit(saving_cal_test)

    deposit_cal_button(driver, saving_cal_test)
    saving_buttion(driver, saving_cal_test)
    saving_cal_test.set_end()
    result_table(saving_cal_test)


if __name__ == "__main__":
    main()
