from market_trend_filter import get_btc_price_change, get_btc_dominance
import pyupbit


def get_altcoin_change():
    df = pyupbit.get_ohlcv("KRW-ETH", interval="minute60", count=2)
    if df is None or len(df) < 2:
        return 0.0
    return (df.iloc[-1]['close'] - df.iloc[-2]['close']) / df.iloc[-2]['close'] * 100


def select_active_strategies():
    change = get_btc_price_change()
    dominance = get_btc_dominance()
    alt_change = get_altcoin_change()

    # 강화된 판단 로직
    if change > 1.5 and dominance > 52.0:
        # BTC 강세, 도미넌스 높음: BTC 위주 전략 가동
        return ['A', 'B']
    elif abs(change) < 0.5 and alt_change > 1.0 and dominance < 52.0:
        # BTC 안정 + 알트 강세 + 낮은 도미넌스: 알트 전략 가동
        return ['C', 'D']
    elif change < -1.0 and alt_change < -1.5:
        # 시장 전반 약세: 보수 전략 혼합
        return ['C']
    else:
        # 혼조장세: 리스크 분산을 위한 혼합 전략
        return ['A', 'C']
