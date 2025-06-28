import time 
import platform
import subprocess
from plyer import notification



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
send_notification(1, "テスト")
