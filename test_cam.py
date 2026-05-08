import cv2

print("🔍 開始測試攝影機連線...")

working_index = None
working_mode = None
cap = None

# 測試鏡頭編號 0, 1, 2
for i in range(3):
    # 測試 1：預設模式
    print(f"嘗試開啟鏡頭編號 {i} (預設模式)...")
    cap = cv2.VideoCapture(i)
    if cap.isOpened() and cap.read()[0]:
        print(f"✅ 成功！找到可用鏡頭，編號是 {i}，請在原程式使用 cv2.VideoCapture({i})")
        working_index = i
        working_mode = "預設"
        break
    if cap: cap.release()
        
    # 測試 2：DSHOW 模式
    print(f"嘗試開啟鏡頭編號 {i} (DSHOW 模式)...")
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cap.isOpened() and cap.read()[0]:
        print(f"✅ 成功！找到可用鏡頭，編號是 {i} (DSHOW)，請在原程式使用 cv2.VideoCapture({i}, cv2.CAP_DSHOW)")
        working_index = i
        working_mode = "DSHOW"
        break
    if cap: cap.release()

if working_index is None:
    print("\n❌ 慘了，找不到任何可用的攝影機畫面！")
    print("請檢查：")
    print("1. 實體線路有沒有插好？")
    print("2. Windows「隱私權與安全性 > 相機」有沒有允許傳統型應用程式存取？")
    print("3. 是否有其他軟體（如 Zoom, Line 等）正在佔用鏡頭？")
else:
    print(f"\n🎥 正在顯示畫面 (模式: {working_mode} / 編號: {working_index})")
    print("請確認畫面是否正常，在畫面上按下 'q' 關閉測試。")
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera Test', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()