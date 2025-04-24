import os
import csv
from datetime import datetime

# 로그 디렉토리 경로
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 일반 로그 기록 (콘솔 + 파일)
def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{now}] {msg}"
    print(full_msg)
    
    with open(os.path.join(LOG_DIR, "trade.log"), "a") as f:
        f.write(full_msg + "\n")

# 매매 결과 저장 (전략별 수익률 기록용)
def log_trade_result(ticker, strategy, entry_price, exit_price, profit_rate, entry_time):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    PERF_FILE = os.path.join(LOG_DIR, "performance.csv")

    row = [
        now,                     # 청산 시각
        ticker,                  # 종목
        strategy,                # 전략명
        round(entry_price, 4),   # 진입가
        round(exit_price, 4),    # 청산가
        f"{profit_rate:.4f}",    # 수익률
        entry_time               # 진입 시각
    ]

    new_file = not os.path.exists(PERF_FILE)

    with open(PERF_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["청산시각", "종목", "전략", "진입가", "청산가", "수익률", "진입시각"])
        writer.writerow(row)
