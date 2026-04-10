import pyautogui
import time
import os

def auto_screenshot(interval_seconds, save_folder="screenshots"):
    """
    定時自動截圖程式
    :param interval_seconds: 每次截圖的間隔時間（秒）
    :param save_folder: 截圖存放的資料夾名稱
    """
    # 檢查並建立存放截圖的資料夾
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print(f"已建立資料夾：{save_folder}")

    print(f"開始自動截圖！每 {interval_seconds} 秒截取一次。")
    print("【溫馨提示】在終端機按下 Ctrl + C 即可停止程式。")

    try:
        while True:
            # 取得當前時間，格式化為 年月日_時分秒，用來當作檔名
            current_time = time.strftime("%Y%m%d_%H%M%S")
            file_name = os.path.join(save_folder, f"screenshot_{current_time}.png")
            
            # 執行截圖
            img = pyautogui.screenshot()
            
            
            img.save(file_name)
            print(f"[{time.strftime('%H:%M:%S')}] 成功儲存：{file_name}")
            
            
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        
        print("\n收到停止指令，自動截圖已結束！")


if __name__ == "__main__":
    auto_screenshot(interval_seconds=60)

    f"我好想吃宵夜"