import pyupbit
import os
from dotenv import load_dotenv

load_dotenv("dotenv.env")

ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)

# 전체 원화 잔고 조회
def get_balance():
    try:
        balances = upbit.get_balances()
        for b in balances:
            if b['currency'] == 'KRW':
                return float(b['balance'])
    except Exception as e:
        print(f"[ERROR] 잔고 조회 실패: {e}")
    return 0.0

# 전체 포지션 정리 (모든 코인 시장가 매도)
def sell_all_positions():
    try:
        balances = upbit.get_balances()
        sell_results = []
        for b in balances:
            currency = b['currency']
            if currency == "KRW":
                continue
            balance = float(b['balance'])
            if balance > 0:
                ticker = f"KRW-{currency}"
                resp = upbit.sell_market_order(ticker, balance)
                sell_results.append((ticker, resp))
        for ticker, result in sell_results:
            print(f"[SELL] {ticker}: {result}")
        print("[SELL] 전체 포지션 정리 완료")
    except Exception as e:
        print(f"[ERROR] 포지션 정리 실패: {e}")

def get_holdings():
    """KRW를 제외한 보유 중인 코인 목록 반환"""
    holdings = {}
    try:
        balances = upbit.get_balances()
        for b in balances:
            currency = b['currency']
            if currency != "KRW":
                amount = float(b['balance'])
                if amount > 0:
                    holdings[f"KRW-{currency}"] = amount
    except Exception as e:
        print(f"[ERROR] 보유 코인 조회 실패: {e}")
    return holdings
