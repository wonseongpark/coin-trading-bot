# sell_all_positions.py
import pyupbit
import os
from dotenv import load_dotenv
from time import sleep

# 환경 변수 로드
load_dotenv("dotenv.env")
ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)

def get_holdings():
    balances = upbit.get_balances()
    holdings = {}
    for b in balances:
        if b['currency'] == 'KRW':
            continue
        total = float(b['balance'])
        if total > 0:
            symbol = "KRW-" + b['currency']
            holdings[symbol] = total
    return holdings

def sell_all():
    holdings = get_holdings()
    if not holdings:
        print("보유 중인 코인이 없습니다.")
        return

    print("=== 보유 자산 일괄 매도 시작 ===")
    for ticker, amount in holdings.items():
        try:
            print(f"{ticker} | 수량: {amount:.6f}")
            res = upbit.sell_market_order(ticker, amount)
            print(f"→ 매도 요청 완료: {res}")
            sleep(1)  # 너무 빠른 요청 방지
        except Exception as e:
            print(f"[ERROR] {ticker} 매도 실패: {e}")

    print("=== 일괄 매도 완료 ===")

if __name__ == "__main__":
    sell_all()

