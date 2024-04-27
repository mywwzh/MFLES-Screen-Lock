import psutil
import subprocess
import os
import time
import requests as r
import win32file

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

if __name__ == "__main__":
    try:
        response = r.get(
            "https://msl.mywwzh.top/select_admin_key.php", verify=False, headers=headers)
        if (response.status_code == 200):
            admin_key = response.text
        else:
            admin_key = "CFDA0330819B58D7A08D23DB182FA8EE0508D7CD56687E69FFFBF06B40618DFDDD306422A843F2090458F6C33556B191900034F7ED2A92BE76D0BA32724A49F4"
    except:
        admin_key = "CFDA0330819B58D7A08D23DB182FA8EE0508D7CD56687E69FFFBF06B40618DFDDD306422A843F2090458F6C33556B191900034F7ED2A92BE76D0BA32724A49F4"
    
    while True:
        try:
            drives = win32file.GetLogicalDrives()
            for drive in range(26):
                if drives & (1 << drive):
                    usb_path = '{}:\\'.format(chr(drive+65))
                    key_path = os.path.join(usb_path, '.msl_key', 'key.key')
                    if os.path.exists(key_path):
                        with open(key_path, 'r') as f:
                            file_content = f.readline().strip()
                        if file_content == admin_key:
                            continue
        except:
            pass
        try:
            if (not os.path.exists('C:/screenlock/sync.exe')) or (not os.path.exists("C:/screenlock/screenlock.exe")):
                os.system("shutdown -r -t 10")
            if not check_process_exists('sync.exe'):
                subprocess.Popen('C:/screenlock/sync.exe')
            if not os.path.exists("C:/screenlock/background.jpg"):
                download_background_image()
        except:
            continue
        time.sleep(3)
