import pyupbit
import requests
from config import BTC_CHANGE_THRESHOLD, BTC_DOMINANCE_THRESHOLD

def get_btc_price_change():
    df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60", count=2)
    if df is None or len(df) < 2:
        return 0
    return (df.iloc[-1]["close"] - df.iloc[-2]["close"]) / df.iloc[-2]["close"] * 100

def get_btc_dominance():
    try:
        response = requests.get("https://api.coinpaprika.com/v1/global")
        dominance = response.json().get("market_cap_percentage", {}).get("btc", 0)
        return dominance
    except:
        return 0

def should_trade_today():
    change = get_btc_price_change()
    dominance = get_btc_dominance()

    return abs(change) <= BTC_CHANGE_THRESHOLD and dominance < BTC_DOMINANCE_THRESHOLD
