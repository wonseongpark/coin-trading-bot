import os
from dotenv import load_dotenv

# Load .env 파일
load_dotenv("dotenv.env")

# API 키
ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 공통 설정
TARGET_INTERVAL = "minute15"
MIN_ORDER_KRW = 5500
TEST_MODE = True  # 실전 돌입 시 False로 변경

# 전략 A 설정
RSI_BUY_LEVELS = [40, 35, 30]   # 분할 진입용 RSI 임계값 (레벨 0, 1, 2)
STRATEGY_A_PROFIT_TARGETS = [0.03, 0.05]   # 분할 익절 목표 (3%, 5%)
STRATEGY_A_STOP_LOSS = -0.02              # 손절 -2%

# 전략 B 설정 (고점 돌파)
STRATEGY_B_PROFIT_TARGETS = [0.03, 0.06]
STRATEGY_B_STOP_LOSS = -0.025

# 전략 C 설정 (볼린저 밴드 + RSI)
STRATEGY_C_PROFIT_TARGETS = [0.025, 0.05]
STRATEGY_C_STOP_LOSS = -0.015

# 전략 D (VWAP 돌파 전략)
STRATEGY_D_PROFIT_TARGETS = [0.03, 0.05]   # 익절 라인: +3%, +5%
STRATEGY_D_STOP_LOSS = -0.02              # 손절 라인: -2%

# 트레일링 스탑 설정 (전략 A/B/C 공통)
TRAILING_STOP_GAP = 0.015  # 최고가 대비 하락폭 1.5% 이상 시 익절 처리

# 쿨다운 설정 (초 단위)
COOLDOWN_SECONDS = 60 * 5  # 1시간

# 시장 흐름 판단용 (strategy_selector & market_trend_filter 에서 사용됨)
BTC_CHANGE_THRESHOLD = 1.0           # 1시간 ±1% 이내면 안정
BTC_DOMINANCE_THRESHOLD = 52.0       # 52% 이하이면 알트 순환 기대
