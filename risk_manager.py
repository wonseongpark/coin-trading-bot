from pnl_tracker import get_pnl, get_daily_loss_sum
from datetime import datetime, timedelta
from notifier import notify

MAX_STRATEGY_LOSS_RATIO = -0.02
MAX_DAILY_LOSS_RATIO = -0.05

# 외부에서 공유받는 전략 상태
strategy_skip = {}

def set_strategy_skip(external_skip_dict):
    global strategy_skip
    strategy_skip = external_skip_dict

def check_risk_limit(strategy_name, allocated_capital):
    now = datetime.now()
    pnl = get_pnl(strategy_name)

    if allocated_capital == 0:
        print(f"[RISK] {strategy_name} 전략은 자본 할당이 0원입니다 — 스킵합니다.")
        return True

    if pnl / allocated_capital < MAX_STRATEGY_LOSS_RATIO:
        cooldown_info = strategy_skip.get(strategy_name, {
            'until': datetime.min,
            'last_notified': datetime.min
        })

        strategy_skip[strategy_name]['until'] = now + timedelta(minutes=5)

        if (now - cooldown_info['last_notified']).total_seconds() > 240:
            notify(f"[{strategy_name}] 전략 손실 초과 - 5분간 중단")
            strategy_skip[strategy_name]['last_notified'] = now

        print(f"[RISK] {strategy_name} 전략 손실 {pnl:.2f}원이 자본 대비 -2% 초과")
        return True

    return False

def check_daily_loss_limit(total_capital=None):
    if total_capital is None:
        return False

    daily_loss = get_daily_loss_sum()
    if daily_loss / total_capital < MAX_DAILY_LOSS_RATIO:
        print(f"[RISK] 전체 전략 하루 손실 {daily_loss:.2f}원이 -5% 초과")
        return True
    return False

