import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# 테스터가 구글스프레드시트 발급받은 API key json 파일 명
JSON_FILE_NAME = "ferrous-ranger-280410-a01265739651.json"

CREDENTIAL = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE_NAME, SCOPE)
GC = gspread.authorize(CREDENTIAL)

TESTCASE_CARD_URL = "https://docs.google.com/spreadsheets/d/1tAaE06aP_Bk5UuVsI-wKvoZTOywf-GYz2WY8NseYuTw/"
TESTCASE_CMA_URL = "https://docs.google.com/spreadsheets/d/1tAaE06aP_Bk5UuVsI-wKvoZTOywf-GYz2WY8NseYuTw/"
TESTCASE_LOAN_URL = "https://docs.google.com/spreadsheets/d/1tAaE06aP_Bk5UuVsI-wKvoZTOywf-GYz2WY8NseYuTw/edit#gid=445109408"
TESTCASE_CAL_URL = "https://docs.google.com/spreadsheets/d/1tAaE06aP_Bk5UuVsI-wKvoZTOywf-GYz2WY8NseYuTw/edit#gid=445109408"
