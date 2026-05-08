import cv2
import collections
import time
import os
import threading
import requests
from ultralytics import YOLO
from dotenv import load_dotenv # 新增這行：載入 dotenv 套件
from moviepy import VideoFileClip
# 新增這行：讀取 .env 檔案裡面的機密資訊
load_dotenv() 

# --- 設定區 ---
FPS = 30
PRE_SECONDS = 5
POST_SECONDS = 5
BUFFER_SIZE = FPS * PRE_SECONDS
SAVE_DIR = "./pet_records"
os.makedirs(SAVE_DIR, exist_ok=True)

# --- 🚀 TG 機器人設定區 (安全版) ---
# 使用 os.getenv() 來抓取 .env 裡面的值
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
EVENT_COOLDOWN = 60  
DETECT_COOLDOWN = 1.5 

# ... 下面的程式碼完全不用動 ...

print("正在載入 AI 大腦 (YOLOv8)...")
model = YOLO("yolov8n.pt") 
print("AI 準備就緒！")

frame_buffer = collections.deque(maxlen=BUFFER_SIZE)
is_event_triggered = False 
last_detect_time = 0
last_event_time = 0  

def send_telegram_photo(msg, image_path):
    """傳送照片與文字到 TG (加上防卡死機制)"""
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
    try:
        with open(image_path, 'rb') as img:
            files = {'photo': img}
            data = {'chat_id': TG_CHAT_ID, 'caption': msg}
            # 加上 timeout=15，最多等 15 秒，避免網路斷線導致程式當機
            response = requests.post(url, data=data, files=files, timeout=15)
            if response.status_code == 200:
                print("TG 照片發送成功！")
            else:
                print(f"TG 照片發送失敗: {response.text}")
    except Exception as e:
        print(f"TG 系統發生錯誤: {e}")


def send_telegram_video(video_path):
    """傳送錄製好的影片到 TG (加上防卡死機制)"""
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendVideo"
    try:
        with open(video_path, 'rb') as vid:
            files = {'video': vid}
            
            # 這裡新增 'supports_streaming': 'true'
            data = {
            'chat_id': TG_CHAT_ID, 
            'supports_streaming': 'true' # 這行很重要
            }
            
            # 影片檔案比較大，給它 60 秒的時間上傳
            response = requests.post(url, data=data, files=files, timeout=60)
            if response.status_code == 200:
                print("TG 影片發送成功！")
            else:
                print(f"TG 影片發送失敗: {response.text}")
    except Exception as e:
        print(f"TG 系統發生錯誤: {e}")

def save_event(pre_frames, trigger_frame, post_frames, target_name):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    print(f"正在儲存 {target_name} 錄影: {timestamp}...")
    
    # 1. 存截圖並發送 TG (即時通知)
    img_path = f"{SAVE_DIR}/shot_{target_name}_{timestamp}.jpg"
    cv2.imwrite(img_path, trigger_frame)
    
    tg_msg = f"Juice要上廁所，監視器捕捉到 {target_name}！\n時間：{timestamp}\n(影片正在背景處理中...)"
    send_telegram_photo(tg_msg, img_path)
    
    # 2. 存原始影片 (改回不會報錯的 mp4v！)
    height, width, _ = trigger_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    vid_path = f"{SAVE_DIR}/video_{target_name}_{timestamp}.mp4"
    out = cv2.VideoWriter(vid_path, fourcc, FPS, (width, height))
    
    for frame in pre_frames: out.write(frame)
    out.write(trigger_frame)
    for frame in post_frames: out.write(frame)
    out.release()
    print(f"[{target_name}] 原始影片儲存完成！準備轉換為 TG 支援的 H.264 格式...")
    
    # 3. 使用 MoviePy 進行無痛轉檔
    tg_vid_path = f"{SAVE_DIR}/TG_video_{target_name}_{timestamp}.mp4"
    try:
        # 讀取剛剛錄好的原始影片
        clip = VideoFileClip(vid_path)
        # 轉存為 libx264 (Telegram 唯一指定格式)，logger=None 讓畫面不要洗版
        clip.write_videofile(tg_vid_path, codec="libx264", logger=None)
        clip.close()
        
        print("轉檔完成！準備上傳 TG...")
        
        # 4. 上傳「轉檔後」的影片給 TG
        send_telegram_video(tg_vid_path)
        
        # (選擇性) 如果你想節省硬碟空間，可以把這行打開，它會自動刪除不能預覽的舊影片
        # os.remove(vid_path) 
        
    except Exception as e:
        print(f"影片轉檔或上傳失敗: {e}")
        
    print("處理完畢！等待冷卻中...")

def ai_worker_thread(frame_to_check, current_time):
    global is_event_triggered, last_event_time
    
    # 冷卻時間檢查
    if current_time - last_event_time < EVENT_COOLDOWN:
        return 

    results = model(frame_to_check, verbose=False)
    detected_target = None
    
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])           
            class_name = model.names[cls_id]   
            confidence = float(box.conf[0])    
            
            if class_name in ['cat', 'dog'] and confidence > 0.60:
                detected_target = class_name
                break 
        if detected_target:
            break
            
    if detected_target:
        print(f"\n[AI] 偵測到目標：{detected_target}！觸發錄影與 TG 通知！")
        is_event_triggered = True
        last_event_time = current_time 

def main():
    global is_event_triggered, last_detect_time
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    
    post_frames = []
    post_frame_count = 0
    trigger_frame = None
    pre_frames_snapshot = []

    print("系統啟動：AI 寵物辨識 + Telegram 雲端推播！")

    while True:
        ret, frame = cap.read()
        if not ret: break

        if not is_event_triggered:
            frame_buffer.append(frame)
            current_time = time.time()
            if current_time - last_detect_time > DETECT_COOLDOWN:
                threading.Thread(target=ai_worker_thread, args=(frame.copy(), current_time)).start()
                last_detect_time = current_time

        else:
            if post_frame_count == 0:
                trigger_frame = frame.copy()
                pre_frames_snapshot = list(frame_buffer)
            
            post_frames.append(frame)
            post_frame_count += 1
            
            if post_frame_count >= (FPS * POST_SECONDS):
                threading.Thread(
                    target=save_event, 
                    args=(pre_frames_snapshot, trigger_frame, post_frames, "Pet")
                ).start()
                
                is_event_triggered = False
                post_frames = []
                post_frame_count = 0
                frame_buffer.clear() 

        cv2.imshow("Smart Pet Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()