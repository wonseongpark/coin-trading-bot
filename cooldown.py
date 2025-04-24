# cooldown.py - 종목별 쿨다운 관리
import os
import json
import time
from config import COOLDOWN_SECONDS

CD_DIR = "cooldowns"
os.makedirs(CD_DIR, exist_ok=True)

# 파일 경로 생성
def _cd_file(ticker):
    return os.path.join(CD_DIR, f"{ticker}.json")

# 쿨다운 확인
def is_in_cooldown(ticker):
    path = _cd_file(ticker)
    if not os.path.exists(path):
        return False
    with open(path, "r") as f:
        data = json.load(f)
    last_time = data.get("last", 0)
    return (time.time() - last_time) < COOLDOWN_SECONDS

# 쿨다운 갱신
def update_cooldown(ticker):
    path = _cd_file(ticker)
    with open(path, "w") as f:
        json.dump({"last": time.time()}, f)
