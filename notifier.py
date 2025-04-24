import os
import requests
from dotenv import load_dotenv
from time import sleep

load_dotenv("dotenv.env")

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def notify(message, retries=3):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}

    for attempt in range(retries):
        try:
            resp = requests.post(url, data=data, timeout=5)
            if resp.status_code == 200:
                return
            else:
                print(f"[NOTIFY] 실패 (status {resp.status_code}): {resp.text}")
        except Exception as e:
            print(f"[NOTIFY] 오류 발생 (시도 {attempt+1}/{retries}): {e}")
        sleep(2)
