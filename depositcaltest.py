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
deposit_tc = doc.worksheet('예금계산기')
driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://banksalad.com/deposits/calculator')


def tc_to_json(i:int) -> dict:
    key = deposit_tc.row_values(1)
    col = len(key)
    value = deposit_tc.row_values(i + 1)

    return {
        key[x]: value[x] for x in range(col)
    }


def page_load(driver: webdriver, deposit_cal_test: Test) -> bool:

    timeout = 10
    try:
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(1) > div > div > input[type=text]"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        result = "예금계산기 화면이 정상적으로 로드되지 않았습니다."
        deposit_cal_test.result_fail_no_quit(driver, result)
        return False


def input(driver: webdriver, deposit_cal_test: Test) -> bool:
    tc = deposit_cal_test.get_tc()

    # 입력 값 초기화
    try:
        money = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(1) > div > div > input[type=text]")
        while True:
            if money.get_attribute("value") != '0':
                money.send_keys(' \b')
            if money.get_attribute("value") == '0':
                break
        period = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(2) > div > div > input[type=text]")
        while True:
            if period.get_attribute("value") != '0':
                period.send_keys(Keys.BACK_SPACE)
            if period.get_attribute("value") == '':
                break
        interest = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.inputForm_LqSYE > div > input[type=text]")
        while True:
            if interest.get_attribute("value") != '0':
                interest.send_keys(Keys.BACK_SPACE)
            if interest.get_attribute("value") == '':
                break

    except NoSuchElementException:
        result = "값을 초기화하기 위한 항목을 찾지 못했습니다."
        Test.result_nt_no_quit(deposit_cal_test, result)
        return False

    # 값 입력
    try:
        money.send_keys(tc["예치금"])
        period.send_keys(tc["가입기간"])
        interest.send_keys(tc["이자율"])

    except NoSuchElementException:
        result = "값을 입력하기 위한 항목을 찾지 못했습니다."
        Test.result_nt_no_quit(deposit_cal_test, result)
        return False
    return True


def drop_select(driver: webdriver, deposit_cal_test: Test) -> bool:
    global sum_nt
    tc = deposit_cal_test.get_tc()
    # 단리/복리 버튼 클릭
    try:
        select_button = tc["단/복리"]
        driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.dropDownContainer_3NNNi > div > label").click()
        driver.find_element(By.CSS_SELECTOR, f".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.dropDownContainer_3NNNi > div > ul > li:nth-child({str(select_button)}) > button").click()

    except NoSuchElementException:
        result = "단리/복리 클릭 버튼을 찾지 못했습니다."
        Test.result_nt_no_quit(deposit_cal_test, result)
        return False
    return True


def result_confirm(driver: webdriver, deposit_cal_test: Test) -> bool:
    # 원금 및 만기지급금액 일치 여부 확인
    try:
        result_interest = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div.resultContainer_1uMhk > div:nth-child(2) > div").text.replace(",", "").replace("원", "")  # 하단 이자 값
        interest = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.inputForm_LqSYE > div > input[type=text]").get_attribute("value")  # 이자 입력 값
        money = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(1) > div > div > input[type=text]").get_attribute("value").replace(",", "")  # 예치금 입력 값
        result_money = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div.resultContainer_1uMhk > div:nth-child(1) > div").text.replace(",", "").replace("원", "")  # 원금 값

        # 예치금액 입력값과 하단 원금 일치여부 확인
        if result_money != money:
            result = f"원금이 일치하지 않습니다 \n" \
                  f"기대결과 : {result_money} \n" \
                  f"실제결과 : {money}"
            deposit_cal_test.result_fail(driver, result)
            return False

    except NoSuchElementException:
        result = "원금 확인을 위한 항목을 찾지 못했습니다."
        Test.result_nt_no_quit(deposit_cal_test, result)
        return False

    try:
        select_button_text = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.dropDownContainer_3NNNi > div > label").text  # 복리, 단리 클릭
        period = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(2) > div > div > input[type=text]").get_attribute("value")  # 기간 입력 값
        expired_payment_amount = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div.option_VmIHA.resultAmount_3pRs4 > div > div > input[type=text]").get_attribute("value").replace(",", "")  # 만기 지급금액 값

        monthlyInterestRate = float(interest) / 12 / 100

        # 만기금액 결과 일치여부 확인
        if select_button_text == '단리':
            simple = (int(money) * (1 + int(period) * float(monthlyInterestRate)))
            if round(simple) != int(expired_payment_amount):
                result = f"만기지급금액이 일치하지 않습니다.\n" \
                        f"기대결과 : {str(simple)}\n" \
                        f"실제결과 :{ expired_payment_amount}"
                deposit_cal_test.result_fail_no_quit(driver, result)
                return False

        if select_button_text == '복리':
            compound = (int(money) * (1 + (math.pow((1 + float(monthlyInterestRate)), int(period)) - 1)))
            if round(compound) != int(expired_payment_amount):
                result = f"만기지급금액이 일치하지 않습니다.\n" \
                    f"기대결과 : {str(compound)}\n" \
                    f"실제결과 : {expired_payment_amount}"
                deposit_cal_test.result_fail_no_quit(driver, result)
                return False

    except NoSuchElementException:
        print("NT - 만기지급금액 결과 확인을 위한 항목을 찾지 못했습니다.")
        return False

    try:
        # 이자 금액 확인
        if (int(expired_payment_amount) - int(result_money)) != int(result_interest):
            result = f"이자금액이 일치하지 않습니다.\n" \
                f"기대결과 : {str(result_interest)}\n" \
                f"실제결과 : {str(int(expired_payment_amount) - int(result_money))}"
            deposit_cal_test.result_fail_no_quit(driver, result)
            return False

    except NoSuchElementException:
        result = "만기지급금액 결과 확인을 위한 항목을 찾지 못했습니다."
        deposit_cal_test.result_fail_no_quit(driver, result)
        return False
    return True


def saving_cal_button(driver: webdriver, deposit_cal_test: Test) -> bool:
    # 적금계산기도 써보기 버튼 클릭
    try:
        print("적금 계산기도 써보기 페이지 클릭 Running...")
        deposit_cal_test.result_total()
        driver.find_element(By.CSS_SELECTOR, "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.bottom_3nZP1 > div > a").click()
        saving_cal_tab = driver.window_handles[1]
        driver.switch_to.window(window_name=saving_cal_tab)

        if driver.current_url != "https://banksalad.com/savings/calculator":
            result = f"적금 계산기도 써보기 버튼 클릭시 잘못된 url로 이동합니다.\n" \
                "기대결과값: https://banksalad.com/savings/calculator\n" \
                f"실제결과값: {driver.current_url}"
            deposit_cal_test.result_fail(driver, result)
            first_tab = driver.window_handles[0]
            driver.switch_to.window(window_name=first_tab)
            return False

        first_tab = driver.window_handles[0]
        driver.switch_to.window(window_name=first_tab)
        Test.result_pass_no_quit(deposit_cal_test)

    except NoSuchElementException:
        result = "적금계산기도 써보기 버튼을 찾지 못했습니다."
        Test.result_nt_no_quit(deposit_cal_test, result)
    return True


def deposit_button(driver: webdriver, deposit_cal_test: Test) -> bool:
    # 지금 추천받기 버튼 클릭
    try:
        print("지금 추천받기 클릭 Running...")
        deposit_cal_test.result_total()
        driver.find_element(By.CSS_SELECTOR, "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.bottom_3nZP1 > a").click()
        deposit_tab = driver.window_handles[2]
        driver.switch_to.window(window_name=deposit_tab)

        if driver.current_url != "https://banksalad.com/deposits/questions":
            result = f"지금 추천받기 버튼 클릭시 잘못된 url로 이동합니다.\n" \
                "기대결과값: https://banksalad.com/deposits/questions\n" \
                f"실제결과값: {driver.current_url}"
            deposit_cal_test.result_fail(driver, result)
            first_tab = driver.window_handles[0]
            driver.switch_to.window(window_name=first_tab)
            return False

        deposit_cal_test.result_pass(driver)

    except NoSuchElementException:
        result = "지금 추천받기 버튼을 찾지 못했습니다."
        Test.result_nt_no_quit(deposit_cal_test, result)
    return True


def main():
    deposit_cal_test = Test()
    deposit_tc = doc.worksheet('예금계산기')
    deposit_cal_test.set_total(len(deposit_tc.col_values(1)) - 1)

    # 백그라운드 옵션
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("headless")

    print("------------------------테스트 시작------------------------")

    if not page_load(driver, deposit_cal_test):
        driver.refresh()
    for i in range(1, deposit_cal_test.get_total() + 1):

        deposit_tc = tc_to_json(i)
        deposit_cal_test.set_no(i)
        deposit_cal_test.set_tc(deposit_tc)
        print(f"{deposit_tc['TC 명']} Running...")

        if not input(driver, deposit_cal_test):
            continue
        if not drop_select(driver, deposit_cal_test):
            continue
        if not result_confirm(driver, deposit_cal_test):
            continue

        Test.result_pass_no_quit(deposit_cal_test)

    saving_cal_button(driver, deposit_cal_test)
    deposit_button(driver, deposit_cal_test)
    deposit_cal_test.set_end()
    result_table(deposit_cal_test)


if __name__ == "__main__":
    main()
