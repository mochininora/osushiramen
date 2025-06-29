import requests
import time
import threading
from datetime import datetime, timedelta, timezone
import os
import front
import tkinter as tk
import platform
import subprocess
from plyer import notification
from shared import shared_data, data_lock, flag


bucket_id = 'aw-watcher-window_mochininora'
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

def monitor_usage():
    flag=0
    try:
        while True:
            with data_lock:
                latest = shared_data.get("latest_result")
            if latest:
                print(f"📦 最新の送信データ: {latest}")
                print(f"📦 最新の送信データ: {latest['cell1']}")
                minutes1=latest['cell1']
                minutes=float(minutes1)

            usage = get_usage_minutes()
            now_time = datetime.now(jst).strftime("%H:%M:%S")
            if usage is not None:
                print(f"[{now_time}] Microsoft Edge の今日の使用時間: {usage} 分")
            else:
                print(f"[{now_time}] 使用時間の取得に失敗しました")
            if latest:
                if usage>=int(minutes) and flag==0:
                    send_notification(usage, "あ")
                    flag=1
            time.sleep(5)
    except Exception as e:
        print(f"❌ モニタースレッドで例外が発生: {e}")



def main():
    print("📡 使用時間モニタリングを開始します。終了するにはウィンドウを閉じてください。")

    root = tk.Tk()
    app = front.PythonGUIApp(root)

    # GUIのあとに動くバックグラウンド処理（GUIを一切触らない）
    threading.Thread(target=monitor_usage, daemon=True).start()

    print("Python GUIアプリケーションを起動しています...")
    print("3つのセルに入力して、送信ボタンを押してください。")

    root.mainloop()

if __name__ == "__main__":
    main()
