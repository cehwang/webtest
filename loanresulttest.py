# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from gspreadAPI import GC, TESTCASE_LOAN_URL
from testresult import Test, result_table
doc = GC.open_by_url(TESTCASE_LOAN_URL)
tc = doc.worksheet('대출 Result TestCase')


def tc_to_json(i:int) -> dict:
    key = tc.row_values(1)
    col = len(key)
    value = tc.row_values(i + 1)

    return {
        key[x]: value[x] for x in range(col)
    }


def loan_select(driver: webdriver) -> bool:
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
        result = "대출 입력화면의 버튼을 찾지 못했습니다."
        Test.result_nt(driver, result)
        return False
    return True


def check_reset(driver: webdriver) -> bool:
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
        result = "대출 결과화면 초기화 시 버튼을 찾지 못했습니다."
        Test.result_nt(driver, result)
        return False
    return True


def check_fin(driver: webdriver, loanresult: Test) -> bool:
    tc = loanresult.get_tc()
    try:
        # 금융사 선택
        fin = tc["금융사"].split(", ")
        for x in range(0, len(fin)):
            driver.find_element(By.XPATH, f"//label[@class='label_fpNum' and contains(text(), '{fin[x]}')]").click()

    except NoSuchElementException:
        result = "금융사 선택 버튼을 찾지 못했습니다."
        Test.result_nt(driver, result)
        return False
    return True


def check_add_select(driver: webdriver, loanresult: Test) -> bool:
    tc = loanresult.get_tc()
    try:
        add_select = tc["추가선택"].split(", ")
        for x in range(0, len(add_select)):
            driver.find_element(By.XPATH, f"//label[@class='label_fpNum' and contains(text(), '{add_select[x]}')]").click()
    except NoSuchElementException:
        result = "추가사항 선택 버튼을 찾지 못했습니다."
        Test.result_nt(driver, result)
        return False
    return True


def check_rate_method(driver: webdriver, loanresult: Test) -> bool:
    tc = loanresult.get_tc()

    try:
        # 금리방식 선택
        rate = tc["금리방식"].split(", ")
        for x in range(0, len(rate)):
            driver.find_element(By.XPATH, f"//label[@class='label_fpNum' and contains(text(), '{rate[x]}')]").click()

    except NoSuchElementException:
        result = "금리방식 선택 버튼을 찾지 못했습니다."
        Test.result_nt(driver, result)
        return False
    return True


def check_repayment_method(driver: webdriver, loanresult: Test) -> bool:
    tc = loanresult.get_tc()
    try:
        # 상환방법 선택
        re_method = tc["상환방법"].split(", ")
        for x in range(0, len(re_method)):
            driver.find_element(By.XPATH, f"//label[@class='label_fpNum' and contains(text(), '{re_method[x]}')]").click()

    except NoSuchElementException:
        result = "상환방법 선택 버튼을 찾지 못했습니다."
        Test.result_nt(driver, result)
        return False
    return True


def check_primerate(driver: webdriver, loanresult: Test) -> bool:
    tc = loanresult.get_tc()
    try:
        # 우대금리 선택
        prime = tc["우대금리"].split(", ")
        for x in range(0, len(prime)):
            driver.find_element(By.XPATH, f"//label[@class='label_fpNum' and contains(text(), '{prime[x]}')]").click()

    except NoSuchElementException:
        result = "우대금리 선택 버튼을 찾지 못했습니다."
        Test.result_nt(driver, result)
        return False
    return True


# 결과 화면에 금리방식 노출 확인
def confirm_rate_method(driver: webdriver, loanresult: Test) -> bool:
    tc = loanresult.get_tc()
    i = driver.find_elements(By.CLASS_NAME, "resultItem_2jgVP")
    try:
        num = len(i)
        rate = tc["금리방식"].split(", ")
        if rate != "":
            if num > 1:
                for x in range(1, 3):
                    for y in range(1, len(rate)):
                        if str(rate) not in i[x].text:
                            result = "선택한 금리방식이 결과에 노출되지 않습니다."
                            loanresult.result_fail(driver, result)
                            return False
    except NoSuchElementException:
        result = "결과페이지에 노출되는 금리방식 항목을 찾지 못했습니다."
        Test.result_nt(driver, result)
        return False

    return True


# 결과 화면에 상환방법 노출 확인
def confirm_repayment_method(driver: webdriver, loanresult: Test) -> bool:
    tc = loanresult.get_tc()
    i = driver.find_elements(By.CLASS_NAME, "resultItem_2jgVP")
    num = len(i)

    try:
        re_method = tc['상환방법'].split(", ")
        if num > 1:
            if re_method != "":
                for x in range(1, 3):
                    for y in range(1, len(re_method)):
                        if str(re_method) not in i[x].text:
                            result = "선택한 상환방법이 결과에 노출되지 않습니다."
                            loanresult.result_fail(driver, result)
                            return False
    except NoSuchElementException:
        result = "결과페이지에 노출되는 상환방법 항목을 찾지 못했습니다."
        Test.result_nt(driver, result)
        return False
    return True


# 결과 화면에 중도상환수수료 노출 확인
def confirm_prepayment(driver: webdriver, loanresult: Test) -> bool:
    tc = loanresult.get_tc()
    i = driver.find_elements(By.CLASS_NAME, "resultItem_2jgVP")
    num = len(i)
    add_select = tc["추가선택"].split(", ")
    try:
        if num > 1:
            if add_select != "":
                for x in range(1, 3):
                    for y in range(1, len(add_select)):
                        if str(add_select) not in i[x].text:
                            result = "선택한 중도상환수수료가 결과에 노출되지 않습니다."
                            loanresult.result_fail(driver, result)
                            return False
    except NoSuchElementException:
        result = "결과페이지에 노출되는 추가선택(이벤트/당일대출/중도상환수수료) 항목을 찾지 못했습니다."
        Test.result_nt(driver, result)
        return False
    return True


def main():

    loanresult = Test()
    tc = doc.worksheet('대출 Result TestCase')
    loanresult.set_total(len(tc.col_values(1)) - 1)

    # 백그라운드 옵션
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("headless")

    print("------------------------테스트 시작------------------------")

    for i in range(1, loanresult.get_total() + 1):

        tc = tc_to_json(i)
        loanresult.set_no(i)
        loanresult.set_tc(tc)
        print(f"{tc['TC 명']} Running...")

        driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        driver.get('https://banksalad.com/credit-loans/questions')

        if not loan_select(driver):
            driver.quit()
            continue

        sleep(1)

        loan_result = driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(1) > .value_3k1fw").text.replace(",", "")
        loan_result = loan_result.replace("만원", "")
        loan_expect = driver.find_element(By.CSS_SELECTOR, "div.preview_Qee0B > div.foot_2aDGD > section > span.resultValue_rynW5 > span").text.replace(",", "").replace("예상 대출한도 ", "").replace("만원", "")

        try:
            driver.find_element(By.LINK_TEXT, "결과보기").click()
            sleep(1)

        except NoSuchElementException:
            result = "\'결과보기\' 버튼을 찾지 못했습니다."
            loanresult.result_nt(driver, result)
            continue

        # 희망 대출금액이 예상 한도보다 낮은 경우 노출되는 alert 처리
        if int(loan_result) > int(loan_expect):

            try:
                alert_switch = driver.switch_to.alert
                alert_switch.accept()
                sleep(1)

            except NoSuchElementException:
                result = "\'alert\' 항목을 찾지 못했습니다."
                loanresult.result_nt(driver, result)
                continue

            if not check_reset(driver):
                driver.quit()
                continue

        else:
            # 희망 대출금액이 예상한도보다 높은 경우 동작
            if not check_reset(driver):
                driver.quit()
                continue

        check_fin(driver, loanresult)
        check_add_select(driver, loanresult)
        check_rate_method(driver, loanresult)
        check_repayment_method(driver, loanresult)
        check_primerate(driver, loanresult)

        sleep(2)
        loan_div = driver.find_elements(By.CLASS_NAME, "resultItem_2jgVP")

        if len(loan_div) == 0:
            result = "상품이 노출되지 않습니다."
            loanresult.result_nt(driver, result)
            continue

        loan_div[0].location_once_scrolled_into_view

        if not confirm_rate_method(driver, loanresult):
            driver.quit()
            continue

        if not confirm_repayment_method(driver, loanresult):
            driver.quit()
            continue

        if not confirm_prepayment(driver, loanresult):
            driver.quit()
            continue

        sleep(1)
        loanresult.result_pass(driver)
    loanresult.set_end()
    result_table(loanresult)


if __name__ == "__main__":
    main()
