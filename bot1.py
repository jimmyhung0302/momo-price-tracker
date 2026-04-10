import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import google.generativeai as genai

# ================= 設定區 (新專案) =================
# 1. 填入你的 Gemini API Key
API_KEY = "AIzaSyDbCq23U_1hQE5vF8IS4fp4lyurPyiourQ"

# 2. 新的目標商品 (DRAM)
TARGET_URL = "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=9573275&Area=search&mdiv=403&oid=1_1&cid=index&kw=kc3000"

# 3. Momo 價格選擇器 (通用)
SELECTOR = "li.special span" 

# 4. ⚠️ 資料庫檔案名稱 (改成 price_data1.json)
DB_FILE = "price_data1.json"

# 5. 模型名稱
MODEL_NAME = "gemini-2.5-flash" 
# ================================================

genai.configure(api_key=API_KEY)

def get_price():
    try:
        # 偽裝成瀏覽器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.momoshop.com.tw/'
        }
        
        response = requests.get(TARGET_URL, headers=headers)
        response.encoding = 'utf-8' 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 嘗試抓取特價
        price_element = soup.select_one(SELECTOR)
        # 如果沒抓到，嘗試抓一般價格
        if not price_element:
             price_element = soup.select_one(".price span")
             
        if not price_element:
            print(f"❌ 找不到價格")
            return None

        raw_price = price_element.text.strip()
        clean_price = ''.join(filter(str.isdigit, raw_price))
        
        if not clean_price: return None
        return int(clean_price)
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return None

def ask_gemini(history_data):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        recent_data = history_data[-10:]
        
        # ⚠️ 這裡改成 DRAM 的敘述
        prompt = f"""
        這是某個 ssd 記憶體的歷史價格：{json.dumps(recent_data)}
        請用繁體中文簡短分析：
        1. 價格趨勢。
        2. 給出購買建議。
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ AI 分析失敗: {e}")
        return "暫無分析"

def main():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []

    print("🕷️ 正在爬取 ssd 價格...")
    current_price = get_price()

    if current_price:
        today = datetime.date.today().strftime("%Y-%m-%d")
        print(f"💰 ssd 價格: ${current_price}")

        if history and history[-1]['date'] == today:
            history[-1]['price'] = current_price
        else:
            history.append({"date": today, "price": current_price})

        print(f"🧠 詢問 AI 中...")
        ai_advice = ask_gemini(history)
        history[-1]['ai_analysis'] = ai_advice

        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 完成！資料已寫入 {DB_FILE}")
    else:
        print("❌ 失敗")

if __name__ == "__main__":
    main()