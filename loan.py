# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from gspreadAPI import GC, TESTCASE_LOAN_URL
from testresult import Test, result_table

doc = GC.open_by_url(TESTCASE_LOAN_URL)
tc = doc.worksheet("BEST 대출 TestCase")


def tc_to_json(i:int) -> dict:
    key = tc.row_values(1)
    col = len(key)
    value = tc.row_values(i + 1)

    return {
        key[x]: value[x] for x in range(col)
    }


def loan_select(driver: webdriver, loan_test: Test) -> bool:
    tc = loan_test.get_tc()
    # 대출 금액 버튼 선택
    try:
        loan = str(tc["대출금액"])
        driver.find_element(By.XPATH, f"//button[@class='tag_KCNXn' and contains(text(), '{loan}')]").click()
        sleep(1)
    except NoSuchElementException:
        result = "희망 대출 금액 선택 버튼을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False

    # 선택한 대출 금액이 입력항목에 정상 노출되는지 확인
    try:
        sleep(2)
        loan_result = driver.find_element(By.CSS_SELECTOR,".questions_3ScUv > li:nth-child(1) > .value_3k1fw").text.replace(",", "").replace("만원", "")
        loan_input = driver.find_element(By.CSS_SELECTOR, ".amount_3x6iq > .desktop_1HAhS > div > input").get_attribute('value')
        if loan_input != loan_result:
            result = "희망 대출 금액 버튼을 클릭했을 때, 입력 결과에 해당 금액이 정상적으로 노출되지 않습니다.\n"\
                f"입력 값: {str(loan_input)}, 결과 값: {str(loan_result)}"
            loan_test.result_fail(driver, result)
            return False
    except NoSuchElementException:
        result = "희망 대출 금액 버튼을 클릭했을 때, 입력 결과 항목을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False
    return True


def loan_credit(driver: webdriver, loan_test: Test) -> bool:
    tc = loan_test.get_tc()

    # 신용등급 선택
    try:
        credit = str(tc["신용등급"])
        driver.find_element(By.CSS_SELECTOR, "label > span").click()
        sleep(1)
        driver.find_element(By.XPATH, f"//span[@class='item_1x2gS' and contains(text(), '{credit}')]").click()
    except NoSuchElementException:
        result = "신용등급 선택창을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False

    # 신용등급 입력 결과 확인
    try:
        creditlevel = driver.find_element(By.CSS_SELECTOR, "label > span").text
        credit_result = driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(2) > .value_3k1fw").text
        if str(credit_result) != str(creditlevel):
            result = "신용등급 선택 시, 입력 결과에 선택 사항이 정상적으로 노출되지 않습니다.\n"\
                     f"입력: {str(creditlevel)}, 결과: {str(credit_result)}"
            loan_test.result_fail(driver, result)
            return False
    except NoSuchElementException:
        result = "신용등급 선택창과 입력 결과 항목을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False

    return True


def loan_job(driver: webdriver, loan_test: Test) -> bool:
    tc = loan_test.get_tc()
    # 직업 선택
    try:
        driver.find_element(By.CSS_SELECTOR, ":nth-child(6) > div > button").click()
    except NoSuchElementException:
        result = "직업 선택 버튼을 선택하지 못했습니다."
        loan_test.result_nt(driver, result)
        return False

    # 직업 선택 팝업이 5초 안에 노출되지 않으면 fail
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".list_2C8C4 > li:nth-child(1) > label"))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        result = "직업 선택 팝업이 정상적으로 노출되지 않았습니다."
        Test.result_fail(driver, result)
        return False

    try:
        job = tc["직업"]
        driver.find_element(By.XPATH, f"//label[contains(text(), '{job}')]").location_once_scrolled_into_view
        driver.find_element(By.XPATH, f"//label[contains(text(), '{job}')]").click()
        driver.find_element(By.CSS_SELECTOR, ".accept_3yeys").click()

    except NoSuchElementException:
        result = "직업 선택 버튼을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False

    # 선택한 직업이 입력항목에 정상 노출되는지 확인
    try:
        job_name = driver.find_element(By.CSS_SELECTOR, ":nth-child(6) > div > button").text
        job_result = driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(3) > .value_3k1fw").text
        if str(job_name) != str(job_result):
            result = "직업 선택 시, 입력 결과에 선택 사항이 정상적으로 노출되지 않습니다.\n"\
                f"선택: {str(job_name)}, 결과: {str(job_result)}"
            loan_test.result_fail(driver, result)
            return False
    except NoSuchElementException:
        result = "직업을 선택했을 때, 입력 결과 항목을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False

    return True


def loan_income(driver: webdriver, loan_test: Test) -> bool:
    tc = loan_test.get_tc()

    # 연소득 선택
    try:
        income = str(tc["연소득"])
        driver.find_element(By.XPATH, f"//button[@class='tag_G72-i' and contains(text(), '{income}')]").click()

    except NoSuchElementException:
        result = "연소득 선택 항목을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False

    # 선택한 연소득이 입력항목에 정상 노출되는지 확인
    try:
        input_income = int(driver.find_element(By.CSS_SELECTOR, ".amount_1_jHL > .desktop_1HAhS > div > input").get_attribute('value'))
        income_result = driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(4) > .value_3k1fw").text.replace(",", "")
        income_result = income_result.replace("만원", "")
        if input_income != int(income_result):
            result = "연소득 선택 시, 입력 결과에 선택 사항이 정상적으로 노출되지 않습니다.\n"\
                f"입력값: {str(input_income)}, 결과값: {str(income_result)}"
            loan_test.result_fail(driver, result)
            return False
    except NoSuchElementException:
        result = "연소득을 선택했을 때, 입력 결과를 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False
    return True


# 결과 리스트 로드 timeout 시 fail처리
def load_loan(driver: webdriver, loan_test: Test) -> bool:
    wait = 0
    for x in range(1, 4):
        while True:
            if wait > 20:
                result = "결과 리스트 로드 timeout"
                loan_test.result_fail(driver, result)
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
def confirm_detail(driver: webdriver, loan_test: Test) -> bool:

    num = len(driver.find_elements(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol:nth-child(2) > li"))
    wait = 0
    if num > 2:
        num = 2
    for x in range(0, num):
        while True:
            if wait > 20:
                result = "결과 리스트 로드 timeout"
                loan_test.result_fail(driver, result)
                return False
            lst_loan = driver.find_elements(By.CSS_SELECTOR, ".resultItem_2jgVP")

            if len(lst_loan) > 0:
                break

            sleep(1)
            wait += 1

        loan_name1 = driver.find_elements(By.CSS_SELECTOR, ".headerText_SOgCc > h1")[x].text.replace("고정금리", "").replace("변동금리", "")
        loan_detail = driver.find_element(By.CSS_SELECTOR, f".resultWrap_1ZJb- > ol > li:nth-child({str(x + 1)}) > div > div.body_cYC3y > div > div.linkButtons_3eD-d > a.linkDetail_2YWx8.linkButton_3mX1p")
        lst_loan[x].location_once_scrolled_into_view
        sleep(1)
        loan_detail.click()

        # 상품 상세페이지 10초동안 로드되지 않은 경우 fail처리
        timeout = 10
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".head_25kNF > h1"))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            result = "상품 상세 페이지가 정상적으로 로드되지 않았습니다."
            loan_test.result_fail(driver, result)
            return False

        try:
            loan_name2 = driver.find_element(By.CSS_SELECTOR, ".head_25kNF > h1").text

            if loan_name1 != loan_name2:
                result = "잘못된 상세페이지로 이동\n"\
                    f"기대결과값: {loan_name1}의 상세페이지, 실제결과값: {loan_name2}의 상세페이지"
                loan_test.result_fail(driver, result)
                return False

            # 결과리스트가 10초동안 로드되지 않은 경우 fail 처리
            wait = 0
            if wait > 10:
                result = "결과 리스트 로드 timeout"
                loan_test.result_fail(driver, result)
                return False

            if len(driver.find_elements(By.CLASS_NAME, "resultItem_2jgVP")) > 0:
                break

            driver.find_element(By.LINK_TEXT, "결과 리스트로").click()
            sleep(2)
            if driver.current_url != "https://banksalad.com/credit-loans/profits":
                result = "결과 리스트로 버튼 클릭시 잘못된 url로 이동\n"\
                    "기대결과값: https://banksalad.com/credit-loans/profits\n"\
                    f"실제결과값: {driver.current_url}"
                loan_test.result_fail(driver, result)
                return False

        except NoSuchElementException:
            result = "상품 상세보기 페이지 내 결과 리스트로 버튼 또는 상품 요소를 찾지못함"
            loan_test.result_nt(driver, result)
            return False
    return True


# 금리 낮은 순 선택
def confirm_filter1(driver: webdriver, loan_test: Test) -> bool:
    n = len(driver.find_elements(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol:nth-child(2) > li"))
    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div > ul > li:nth-child(1) > button").click()

        for i in range(1, n):
            sleep(2)
            result_list = driver.find_element(By.CSS_SELECTOR, f".resultWrap_1ZJb- > ol > li:nth-child({str(i)}) > div > div.body_cYC3y > div > div.info_19W26 > dl  dd.interestInfo_r017q > ul > li:nth-child(1) > div > strong").text.replace("평균 ", "").replace("%", "")
            result_list2 = driver.find_element(By.CSS_SELECTOR, f".resultWrap_1ZJb- > ol > li:nth-child({str(i + 1)}) > div > div.body_cYC3y > div > div.info_19W26 > dl  dd.interestInfo_r017q > ul > li:nth-child(1) > div > strong").text.replace("평균 ", "").replace("%", "")
            if float(result_list) > float(result_list2):
                result = "금리 낮은 순 필터가 정상적으로 동작하지 않습니다."
                loan_test.result_fail(driver, result)
                return False

    except NoSuchElementException:
        result = "금리 낮은 순 필터 관련 항목을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False
    return True


# 한도 높은 순 선택
def confirm_filter2(driver: webdriver, loan_test: Test) -> bool:
    n = len(driver.find_elements(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol:nth-child(2) > li"))
    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div > ul > li:nth-child(2) > button").click()

        for i in range(1, n):
            sleep(2)
            result_list = driver.find_element(By.CSS_SELECTOR, f".resultWrap_1ZJb- > ol > li:nth-child({str(i)}) > div > div.body_cYC3y > div > div.info_19W26 > dl > dd.interestInfo_r017q > ul > li.calculatedInterestWrap_1QJa1 > span.calculatedInterest_2MmE7").text.replace("예상한도 ", "").replace(",", "").replace("만원", "")
            result_list2 = driver.find_element(By.CSS_SELECTOR, f".resultWrap_1ZJb- > ol > li:nth-child({str(i + 1)}) > div > div.body_cYC3y > div > div.info_19W26 > dl > dd.interestInfo_r017q > ul > li.calculatedInterestWrap_1QJa1 > span.calculatedInterest_2MmE7").text.replace("예상한도 ", "").replace(",", "").replace("만원", "")
            if int(result_list) < int(result_list2):
                result = "한도 높은 순 필터가 정상적으로 동작하지 않습니다."
                loan_test.result_fail(driver, result)
                return False

    except NoSuchElementException:
        result = "한도 높은 순 필터 관련 항목을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False
    return True


# 최장 기간 순 선택
def confirm_filter3(driver: webdriver, loan_test: Test) -> bool:
    n = len(driver.find_elements(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol:nth-child(2) > li"))
    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div > ul > li:nth-child(3) > button").click()

        for i in range(1, n):
            sleep(2)
            result_list = driver.find_element(By.CSS_SELECTOR, f".resultWrap_1ZJb- > ol > li:nth-child({str(i)}) > div > div.body_cYC3y > div > div.info_19W26 > dl > dd:nth-child(4) > ul > li > span").text
            result_list2 = driver.find_element(By.CSS_SELECTOR, f".resultWrap_1ZJb- > ol > li:nth-child({str(i + 1)}) > div > div.body_cYC3y > div > div.info_19W26 > dl > dd:nth-child(4) > ul > li > span").text
            split1 = result_list.split('~', 2)
            split2 = split1[1].split('개월', 2)
            split3 = result_list2.split('~', 2)
            split4 = split3[1].split('개월', 2)
            if int(split2[0]) < int(split4[0]):
                result = "한도 높은 순 필터가 정상적으로 동작하지 않습니다."
                loan_test.result_fail(driver, result)
                return False

    except NoSuchElementException:
        result = "최장기간 순 필터 관련 항목을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False
    return True


def result_credit(driver: webdriver, loan_test: Test) -> bool:
    # 선택한 신용등급과 결과페이지 상단 신용등급 일치 여부 확인
    try:
        result_creditlevel = driver.find_element(By.CSS_SELECTOR,".desktop_1HAhS > ul > li:nth-child(1) > div > ""label").text
        creditlevel = driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(2) > .value_3k1fw").text
        if creditlevel != result_creditlevel:
            result = "신용등급이 결과 페이지 상단과 일치하지 않습니다.\n"\
                f"기대결과값: {str(creditlevel)}, 실제결과값: {str(result_creditlevel)}"
            loan_test.result_fail(driver, result)
            return False
    except NoSuchElementException:
        result = "결과페이지 상단 신용등급을 찾지 못했습니다."
        loan_test.result_nt(driver, result)
        return False
    return True


def main():
    loan_test = Test()
    tc = doc.worksheet('대출 Result TestCase')
    loan_test.set_total(len(tc.col_values(1)) - 1)

    # 백그라운드 옵션
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("headless")

    print("------------------------테스트 시작------------------------")
    for i in range(1, loan_test.get_total() + 1):

        tc = tc_to_json(i)
        loan_test.set_no(i)
        loan_test.set_tc(tc)
        print(f"{tc['TC 명']} Running...")

        driver = webdriver.Chrome('C:/Users/cehwang/PycharmProjects/Selenium/chromedriver.exe')
        driver.get('https://banksalad.com/credit-loans/questions')

        if not loan_select(driver, loan_test):
            driver.quit()
            continue

        get_loan_result = driver.find_element(By.CSS_SELECTOR,".questions_3ScUv > li:nth-child(1) > .value_3k1fw").text.replace(",", "").replace("만원", "")

        if not loan_credit(driver, loan_test):
            driver.quit()
            continue

        if not loan_job(driver, loan_test):
            driver.quit()
            continue

        if not loan_income(driver, loan_test):
            driver.quit()
            continue

        sleep(1)

        # 희망 대출 금액, 예상 대출 한도
        loan_expect = driver.find_element(By.CSS_SELECTOR, "div.preview_Qee0B > div.foot_2aDGD > section > span.resultValue_rynW5 > span").text.replace(",", "").replace("예상 대출한도 ", "").replace("만원", "")
        creditlevel = driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(2) > .value_3k1fw").text
        try:
            driver.find_element(By.LINK_TEXT, "결과보기").click()
            sleep(1)

        except NoSuchElementException:
            result = "\'결과보기\' 버튼을 찾지 못했습니다."
            loan_test.result_nt(driver, result)
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
                    result = "희망 대출금액이 결과 페이지 상단 금액과 일치하지 않습니다.\n"\
                        f"alert 워딩에 {str(alert_text)} 결과 페이지 상단 금액 {str(loan_text)}이 포함되지 않습니다."
                    loan_test.result_fail(driver, result)
                    continue

            except NoSuchElementException:
                result = "\'결과페이지 상단 금액\' 항목을 찾지 못했습니다."
                loan_test.result_nt(driver, result)
                continue

        else:
            # 희망 대출금액이 예상한도보다 높은 경우 동작
            sleep(1)
            # 선택한 희망 대출금액이 상단 금액과 일치하는지 확인
            try:
                loan_text = driver.find_element(By.CSS_SELECTOR, "#amount").get_attribute('value')
                if get_loan_result != loan_text:
                    result = "희망 대출금액이 결과 페이지 상단 금액과 일치하지 않습니다.\n" \
                             f"기대결과값: {str(get_loan_result)}, 실제결과값: {str(loan_text)}"
                    loan_test.result_fail(driver, result)
                    continue

            except NoSuchElementException:
                result = "결과 페이지 상단 금액을 찾지 못했습니다."
                loan_test.result_nt(driver, result)
                continue

        # 예상한도가 결과페이지 첫번째 상품에 노출되는 금액과 동일한지 확인
        try:
            sleep(2)
            loan_expect_result_list = driver.find_element(By.CSS_SELECTOR, ".calculatedInterest_2MmE7").text.replace(",", "").replace("예상한도 ", "").replace("만원", "")  # 결과 페이지의 첫번째 상품 한도

            if int(loan_expect) != int(loan_expect_result_list):
                result = "희망 대출금액이 결과 페이지 상단 금액과 일치하지 않습니다.\n" \
                         f"기대결과값: {str(loan_expect)}, 실제결과값: {str(loan_expect_result_list)}"
                loan_test.result_fail(driver, result)
                continue

        except NoSuchElementException:
            result = "결과페이지 첫 번째 상품의 예상한도를 찾지 못했습니다."
            loan_test.result_nt(driver, result)
            continue

        # 선택한 신용등급과 결과페이지 상단 신용등급 일치 여부 확인
        try:
            result_creditlevel = driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(1) > div > ""label").text
            if creditlevel != result_creditlevel:
                result = "신용등급이 결과 페이지 상단과 일치하지 않습니다.\n" \
                            f"기대결과값: {str(creditlevel)}, 실제결과값: {str(result_creditlevel)}"
                loan_test.result_fail(driver, result)
                continue

        except NoSuchElementException:
            result = "결과페이지 상단 신용등급을 찾지 못했습니다."
            loan_test.result_nt(driver, result)
            continue

        if not load_loan(driver, loan_test):
            driver.quit()
            continue

        if not confirm_detail(driver, loan_test):
            driver.quit()
            continue

        if not confirm_filter1(driver, loan_test):
            driver.quit()
            continue

        if not confirm_filter2(driver, loan_test):
            driver.quit()
            continue

        if not confirm_filter3(driver, loan_test):
            driver.quit()
            continue

        loan_test.result_pass(driver)
    loan_test.set_end()
    result_table(loan_test)


if __name__ == "__main__":
    main()
