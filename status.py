import requests
import time
import subprocess
import os
import psutil

def check_process_exists(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

if __name__ == "__main__":
    try:
        f = open('C:/screenlock/config.ini', 'r', encoding='utf-8')
        addr = f.readline().strip()  # 读取配置的门牌号
        f.close()
    except:
        addr = "获取失败"
        
    api_url = "https://47.109.57.252/api/screenlock/checkcurrent.php?addr={0}".format(addr)

    while True:
        try:
            response = requests.get(api_url, verify=False)
            if(response.status_code == 200):
                data = response.json()
                # format: {"set_time":unix_timestrap, "status", "lock"/"unlock"}
                set_time = float(data["set_time"])
                status = data["status"]
                if(float(time.time() - set_time) < 15): 
                    if(status == "unlock"):
                        try:
                            os.system("taskkill /f /im screenlock.exe")
                            subprocess.Popen("C:/Windows/explorer.exe")
                        except:
                            pass
                    else:
                        if not check_process_exists("screenlock.exe"):
                            subprocess.Popen("C:/screenlock/screenlock.exe")
                        time.sleep(15)
        except:
            pass
        time.sleep(8)
            