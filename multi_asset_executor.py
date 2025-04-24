# multi_asset_executor.py (리팩토링: 중복 손실 알림 제거)
import time
import schedule
from threading import Thread
from datetime import datetime, timedelta
from strategy_a import run_strategy_a
from strategy_b import run_strategy_b
from strategy_c import run_strategy_c
from strategy_d import run_strategy_d
from risk_manager import check_risk_limit, check_daily_loss_limit, set_strategy_skip
from allocator import get_dynamic_allocation
from pnl_tracker import update_pnl, get_pnls, reset_daily_pnl
from upbit_api import get_balance, get_holdings, sell_all_positions
from notifier import notify
from market_trend_filter import should_trade_today
from strategy_selector import select_active_strategies

STRATEGY_FUNCS = {
    'A': run_strategy_a,
    'B': run_strategy_b,
    'C': run_strategy_c,
    'D': run_strategy_d
}

last_allocation = {k: 0.25 for k in STRATEGY_FUNCS}
strategy_skip = {k: {'until': datetime.min, 'last_notified': datetime.min} for k in STRATEGY_FUNCS}
set_strategy_skip(strategy_skip)

def rebalance():
    global last_allocation, capital
    pnls = get_pnls()
    last_allocation = get_dynamic_allocation(pnls)
    capital = get_balance()
    reset_daily_pnl()

    holdings = get_holdings()
    coin_summary = "\n".join([f" - {coin}: {amount:.4f}" for coin, amount in holdings.items()])
    
    msg = "[Rebalance Completed]\n"
    for key in last_allocation:
        msg += f" - {key}: {last_allocation[key]:.2%}\n"
    msg += f" - Total Capital (KRW): {capital:,.0f} KRW\n"
    msg += "\n[Current Holdings]\n" + (coin_summary if coin_summary else " - 없음")

    print(f"[{datetime.now()}] {msg}")
    notify(msg)

def run_strategy(strategy_key, alloc_amount):
    strategy_func = STRATEGY_FUNCS[strategy_key]
    now = datetime.now()

    # 쿨다운 상태면 전략 실행 중단 + 중복 알림 방지
    if now < strategy_skip[strategy_key]['until']:
        return

    # 손실 초과 여부 판단
    if check_risk_limit(strategy_key, alloc_amount):
        if strategy_skip[strategy_key]['until'] < now:  # 최초 중단 시점만 설정
            strategy_skip[strategy_key]['until'] = now + timedelta(minutes=5)
            strategy_skip[strategy_key]['last_notified'] = datetime.min  # 알림 초기화
        return

    # 전략 실행
    try:
        profit = strategy_func(alloc_amount)
        if profit:
            update_pnl(strategy_key, profit)
            notify(f"[{strategy_key}] 거래 발생\n수익: {profit:+,.0f} KRW")
    except Exception as e:
        notify(f"[{strategy_key}] ERROR: {e}")
        print(f"[ERROR] {strategy_key} 실행 중 오류: {e}")

def run():
    global capital
    print(f"[{datetime.now()}] Bot started.")
    notify("자동 전략 봇이 시작되었습니다.")
    rebalance()

    schedule.every().day.at("09:00").do(rebalance)

    while True:
        schedule.run_pending()

        if check_daily_loss_limit(capital):
            notify("일일 손실 한도 초과 - 전체 포지션 청산 후 종료")
            sell_all_positions()
            break

        if not should_trade_today():
            time.sleep(60)
            continue

        active = select_active_strategies()
        capital = get_balance()
        threads = [
            Thread(target=run_strategy, args=(k, capital * last_allocation.get(k, 0)))
            for k in active
        ]
        for t in threads: t.start()
        for t in threads: t.join()
        time.sleep(60)

if __name__ == "__main__":
    run()

