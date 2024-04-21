import psutil
import subprocess
import os
import time
import requests as r

headers = {
    'User-Agent': 'MFLES Screen Lock v1.2.0'
}


def check_process_exists(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False


def download_background_image():
    retries = 0
    while retries < 3:
        try:
            response = r.get(
                "https://msl.mywwzh.top/background.jpg", headers=headers)
            with open("C:/screenlock/background.jpg", "wb") as f:
                f.write(response.content)
                f.close()
            break
        except:
            retries += 1
            continue


while True:
    try:
        if (not os.path.exists('C:/screenlock/sync.exe')) or (not os.path.exists("C:/screenlock/screenlock.exe")):
            os.system("shutdown -r -t 10")
        if not check_process_exists('sync.exe'):
            subprocess.Popen('C:/screenlock/sync.exe')
        if not os.path.exists("C:/screenlock/background.jpg"):
            download_background_image()
        if check_process_exists('taskmgr.exe'):
            os.system('taskkill /f /im taskmgr.exe')
    except:
        continue
    time.sleep(3)
