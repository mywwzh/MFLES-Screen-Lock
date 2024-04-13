import requests
import time
import subprocess
import os
import psutil
from PIL import ImageGrab
from cv2 import VideoCapture, imwrite, Laplacian, CV_64F
from plyer import notification

executed_commands = []


def check_process_exists(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False


def upload_screenshot(addr):
    try:
        screenshot = ImageGrab.grab()
        screenshot.save("C:/screenlock/screenshot.png")
        data = {"addr": addr}
        files = {'file': open('C:/screenlock/screenshot.png', 'rb')}
        requests.post(
            '[your_url]/upload_screenshot.php', files=files, data=data)
        os.remove("C:/screenlock/screenshot.png")
    except Exception as err:
        try:
            data = {"addr": addr, "message": str(err)}
            requests.post("[your_url]/error_report.php", data=data)
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
        time.sleep(1)
        # 初始化最佳图像和最佳清晰度
        best_frame = None
        best_focus = 0
        # 捕获多帧图像并选择最清晰的一帧
        ret, frame = cap.read()
        for _ in range(10):
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
            requests.post("[your_url]/error_report.php", data=data)
        except:
            pass

    try:
        data = {"addr": addr}
        files = {'file': open('C:\\screenlock\\camera.png', 'rb')}
        requests.post(
            '[your_url]/upload_camera.php', files=files, data=data)
        os.remove("C:\\screenlock\\camera.png")
    except Exception as err:
        try:
            data = {"addr": addr, "message": str(err)}
            requests.post("[your_url]/error_report.php", data=data)
        except:
            pass


if __name__ == "__main__":
    try:
        f = open('C:/screenlock/config.ini', 'r', encoding='utf-8')
        addr = f.readline().strip()  # 读取配置的门牌号
        f.close()
    except:
        addr = "获取失败"
    if check_process_exists("screenlock.exe"):
        is_locked = "lock"
    else:
        is_locked = "unlock"
    api_url = "[your_url]/sync.php?addr={0}&is_locked={1}".format(
        addr, is_locked)

    while True:
        try:
            response = requests.get(api_url, verify=False)
            if response.status_code == 200:
                data = response.json()
                status = data["status"]
                status_set_time = float(data["status_set_time"])
                status_set_user = data["status_set_user"]
                command = data["command"]
                command_set_time = float(data["command_set_time"])
                show_screen_set_time = float(data["show_screen_set_time"])
                show_camera_set_time = float(data["show_camera_set_time"])

                current_time = time.time()

                if current_time - status_set_time < 5:
                    if status == "unlock" and status_set_time not in executed_commands:
                        try:
                            os.system("taskkill /f /im screenlock.exe")
                            subprocess.Popen("C:/Windows/explorer.exe")
                            executed_commands.append(status_set_time)
                            notification.notify(app_icon="C:/screenlock/mfles.ico", app_name="Screen Locker", title="远程解锁成功",
                                                message="管理员远程解锁了此设备。\n操作人：{0}".format(status_set_user), timeout=10)
                        except Exception as err:
                            try:
                                data = {"addr": addr, "message": str(err)}
                                requests.post(
                                    "[your_url]/error_report.php", data=data)
                            except:
                                pass
                    elif status_set_time not in executed_commands:
                        executed_commands.append(status_set_time)
                        if not check_process_exists("screenlock.exe"):
                            subprocess.Popen("C:/screenlock/screenlock.exe")

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
                    "[your_url]/error_report.php", data=data)
            except:
                pass
        time.sleep(2)
