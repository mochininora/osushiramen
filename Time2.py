import requests
from datetime import datetime, timedelta, timezone

# バケットID（固定でOK）
bucket_id = 'aw-watcher-window_LAPTOP-5A2GDQCB'

# Edgeの実際のアプリ名に合わせて修正！
TARGET_APP_NAME = 'msedge.exe'

# 日本時間で今日の0時を取得し、UTCに変換
jst = timezone(timedelta(hours=9))
start_of_today = datetime.now(jst).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)
now = datetime.now(timezone.utc)

# イベント取得
try:
    res = requests.get(
        f"http://localhost:5600/api/0/buckets/{bucket_id}/events",
        params={"start": start_of_today.isoformat(), "end": now.isoformat()}
    )
    res.raise_for_status()
    events = res.json()
except Exception as e:
    print(f"❌ イベント取得に失敗: {e}")
    exit()

# 使用時間の合計（秒）
total_seconds = 0

# 判定条件に合致するイベントだけ合計
for event in events:
    app = event.get("data", {}).get("app", "")
    duration = event.get("duration", 0)
    if app == TARGET_APP_NAME:
        total_seconds += duration

# 分に変換して出力
total_minutes = round(total_seconds / 60)
print(f"🕒 Microsoft Edge（msedge.exe）の今日の使用時間: {total_minutes} 分")
