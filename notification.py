import requests
import time 
import platform
import subprocess
from plyer import notification
from datetime import datetime, timedelta, timezone

#(追加)使用時間を取得する関数
def get_used_minutes_from_activitywatch():
    bucket_id = 'aw-watcher-window_LAPTOP-5A2GDQCB'
    #bucket_id = 'aw-watcher-window_tokudasuiseinoMacBook-Air.local' #Macの場合
    TARGET_APP_NAME = 'msedge.exe'
    #TARGET_APP_NAME = 'Safari' #MacのSafari

    jst = timezone(timedelta(hours=9))
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
        return 0

    total_seconds = 0
    for event in events:
        app = event.get("data", {}).get("app", "")
        if app == TARGET_APP_NAME:
            total_seconds += event.get("duration", 0)

    return round(total_seconds / 60)


def send_notification(used_hours, next_task):
    system = platform.system()
    if system == "Darwin":  # macOSの場合
        script = f'display notification "{used_hours}時間使用しています。\n{next_task}に取り組みましょう" with title "タイマー"'
        subprocess.run(["osascript", "-e", script])
    else:
        # Windowsやその他のOSは元のplyerの通知を使う
        notification.notify(
            title="タイマー",
            message=f"{used_hours}時間使用しています。\n{next_task}に取り組みましょう",
            timeout=10
        )

# 呼び出し例
used_minutes = get_used_minutes_from_activitywatch()
used_hours = used_minutes / 60
next_task = "休憩する"  # UIなどから受け取る想定

send_notification(used_hours, next_task)


