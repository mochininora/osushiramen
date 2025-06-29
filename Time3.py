import requests
import time
from datetime import datetime, timedelta, timezone
import os

bucket_id = 'aw-watcher-window_LAPTOP-5A2GDQCB'
TARGET_APP_NAME = 'msedge.exe'
jst = timezone(timedelta(hours=9))

def get_usage_minutes():
    start_of_today = datetime.now(jst).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)
    now = datetime.now(timezone.utc)

    try:
        res = requests.get(
            f"http://localhost:5600/api/0/buckets/{bucket_id}/events",
            params={"start": start_of_today.isoformat(), "end": now.isoformat()}
        )
        res.raise_for_status()
        events = res.json()
    except Exception as e:
        print(f"❌ イベント取得に失敗: {e}")
        return None

    total_seconds = sum(
        event.get("duration", 0)
        for event in events
        if event.get("data", {}).get("app", "") == TARGET_APP_NAME
    )
    return round(total_seconds / 60)

print("📡 使用時間モニタリングを開始します。終了するには Ctrl + C を押してください。")

try:
    while True:
        usage = get_usage_minutes()
        os.system("cls" if os.name == "nt" else "clear")
        now_time = datetime.now(jst).strftime("%H:%M:%S")
        if usage is not None:
            print(f"[{now_time}] Microsoft Edge の今日の使用時間: {usage} 分")
        else:
            print(f"[{now_time}] 使用時間の取得に失敗しました")
        time.sleep(5)
except KeyboardInterrupt:
    print("\n⏹️ モニタリングを終了しました。")
