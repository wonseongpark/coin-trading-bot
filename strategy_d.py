import pyupbit
import os
from dotenv import load_dotenv
from config import *
from position import *
from notifier import notify
from logger import log, log_trade_result
from strategy_info import STRATEGY_DESCRIPTIONS

load_dotenv("dotenv.env")
ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

TICKER = "KRW-XRP"
STRATEGY = "D"

def get_vwap(df):
    return (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()

def entry_signal(df):
    vwap_series = get_vwap(df)
    vwap = vwap_series.iloc[-1]
    prev_vwap = vwap_series.iloc[-2]
    close = df["close"].iloc[-1]
    prev_close = df["close"].iloc[-2]

    if close > vwap and prev_close < prev_vwap:
        return True, 0
    return False, -1

def should_exit(pos, current_price):
    if pos["trailing_max"] - current_price >= pos["trailing_stop_gap"]:
        return "트레일링 익절"
    if any(current_price >= tp for tp in pos["take_profit_levels"]):
        return "목표가 익절"
    if current_price <= pos["stop_loss"]:
        return "손절"
    return None

def run_strategy_d(allocated_krw):
    upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)
    df = pyupbit.get_ohlcv(TICKER, interval=TARGET_INTERVAL, count=100)
    if df is None or len(df) < 2:
        log(f"[{STRATEGY}] 데이터 부족")
        return None

    current_price = df["close"].iloc[-1]
    pos = load_position(TICKER, STRATEGY)

    if not pos["has_position"]:
        should_enter, level = entry_signal(df)
        if should_enter:
            size = allocated_krw / current_price
            try:
                res = upbit.buy_market_order(TICKER, allocated_krw)
                if "uuid" in res:
                    record_entry(
                        TICKER, current_price, STRATEGY, level, size,
                        stop_loss=current_price * (1 + STRATEGY_D_STOP_LOSS),
                        take_profit_levels=[current_price * (1 + x) for x in STRATEGY_D_PROFIT_TARGETS],
                        trailing_gap=current_price * TRAILING_STOP_GAP
                    )
                    notify(
                        f"{STRATEGY_DESCRIPTIONS[STRATEGY]}\n"
                        f"✅ 매수 진입 - {TICKER}\n"
                        f"가격: {current_price:.0f}원\n레벨: {level}"
                    )
                    log(f"[{STRATEGY}] 매수 진입: {current_price} @ level {level}")
            except Exception as e:
                log(f"[{STRATEGY}] 매수 오류: {e}")
        return None

    profit_rate = (current_price - pos["avg_buy_price"]) / pos["avg_buy_price"]
    update_trailing_max(TICKER, current_price, STRATEGY)
    reason = should_exit(pos, current_price)

    if reason:
        try:
            balance = upbit.get_balance(TICKER)
            if balance > 0:
                res = upbit.sell_market_order(TICKER, balance)
                if "uuid" in res:
                    profit = profit_rate * pos["position_size"] * pos["avg_buy_price"]
                    log_trade_result(TICKER, STRATEGY, pos["avg_buy_price"], current_price, profit_rate, pos["entry_time"])
                    notify(
                        f"[{STRATEGY}] {reason} 청산 - {TICKER}\n"
                        f"진입가: {pos['avg_buy_price']:.0f}\n청산가: {current_price:.0f}\n"
                        f"수익률: {profit_rate:.2%}\n수익: {profit:,.0f}원"
                    )
                    log(f"[{STRATEGY}] {reason} 청산 완료: 수익률 {profit_rate:.2%}")
                    reset_position(TICKER, STRATEGY)
                    return profit
        except Exception as e:
            log(f"[{STRATEGY}] 매도 오류: {e}")
            return None

    return None
