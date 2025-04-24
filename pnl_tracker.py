import os
import json
from datetime import datetime
from collections import defaultdict

# 동적 전략별 PnL 저장소
pnl_data = defaultdict(float)
daily_loss_tracker = defaultdict(list)

# 전략별 수익 업데이트
def update_pnl(strategy_name, profit):
    pnl_data[strategy_name] += profit
    daily_loss_tracker[strategy_name].append(profit)

# 전략별 전체 누적 수익률 반환
def get_pnls():
    return dict(pnl_data)

# 특정 전략의 누적 수익률 반환
def get_pnl(strategy_name):
    return pnl_data[strategy_name]

# 전체 손실 합산 (일일 손실)
def get_daily_loss_sum():
    return sum(sum(losses) for losses in daily_loss_tracker.values())

# 일일 손익 초기화 (리밸런싱용)
def reset_daily_pnl():
    daily_loss_tracker.clear()
