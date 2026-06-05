import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import google.generativeai as genai
import psycopg2

# ==========================================
# 1. 參數設定區 (請填入你的金鑰與密碼)
# ==========================================
API_KEY = "API_KEY"
# ⚠️ 請替換成你真實的 Render 密碼
DATABASE_URL = "DATABASE_URL"
TARGET_URL = "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=9573275"
SELECTOR = "li.special span" 
DB_FILE = "price_data.json"
MODEL_NAME = "gemini-2.5-flash"

genai.configure(api_key=API_KEY)

# ==========================================
# 2. 爬蟲功能：抓取價格與商品名稱
# ==========================================
def get_product_info():
    """ 爬取 Momo 網頁並抓出價格與商品名稱 """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.momoshop.com.tw/'
        }
        
        response = requests.get(TARGET_URL, headers=headers)
        response.encoding = 'utf-8' 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 抓取價格
        price_element = soup.select_one(SELECTOR)
        if not price_element:
             price_element = soup.select_one(".price span")
             
        if not price_element:
            print("❌ 找不到價格，可能 Momo 改版或被擋了")
            return None

        raw_price = price_element.text.strip()
        clean_price = ''.join(filter(str.isdigit, raw_price))
        
        if not clean_price:
            print(f"❌ 抓到了元素但裡面沒數字: {raw_price}")
            return None
            
        final_price = int(clean_price)
        
        # 抓取商品名稱 (為了符合資料庫 Schema)
        title_tag = soup.find('h1', {'id': 'osmGoodsName'})
        model_name = title_tag.text.strip() if title_tag else "Momo SSD (未抓取到名稱)"
        
        # 簡易判斷容量
        capacity = "1TB" 
        if "2TB" in model_name: capacity = "2TB"
        elif "500GB" in model_name: capacity = "500GB"

        return {
            "price": final_price,
            "model_name": model_name,
            "capacity": capacity
        }
        
    except Exception as e:
        print(f"❌ 爬蟲發生錯誤: {e}")
        return None

# ==========================================
# 3. AI 分析功能
# ==========================================
def ask_gemini(history_data):
    """ 把歷史數據丟給 Gemini 分析 """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        recent_data = history_data[-10:]
        prompt = f"""
        這是某個 SSD 硬碟的歷史價格：{json.dumps(recent_data)}
        請用繁體中文簡短分析：
        1. 價格趨勢。
        2. 是否為歷史低點？建議現在下單嗎？
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Gemini 分析失敗: {e}")
        return "暫無法取得 AI 分析"

# ==========================================
# 4. 雲端資料庫上傳功能 (新增)
# ==========================================
def upload_data_to_db(product_info):
    print("☁️ 準備將今日價格同步至 Render 雲端資料庫...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        today_date = datetime.date.today().isoformat()
        
        insert_query = """
            INSERT INTO ssd_prices (model_name, capacity, price, record_date) 
            VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            product_info["model_name"], 
            product_info["capacity"], 
            product_info["price"], 
            today_date
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ 成功同步至雲端資料庫！")
        
    except Exception as e:
        print(f"❌ 雲端資料庫寫入失敗: {e}")

# ==========================================
# 5. 主程式流程
# ==========================================
def main():
    # 讀取本地端 JSON 歷史紀錄
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []

    print("🕷️ 正在爬取 Momo 價格...")
    product_info = get_product_info()

    if product_info:
        current_price = product_info["price"]
        today = datetime.date.today().strftime("%Y-%m-%d")
        print(f"💰 抓到價格: ${current_price} ({product_info['model_name']})")
        
        # 1. 更新本地 JSON 歷史紀錄
        if history and history[-1]['date'] == today:
            history[-1]['price'] = current_price
            print("📅 更新今日價格記錄")
        else:
            history.append({"date": today, "price": current_price})
            print("📝 新增一筆記錄")

        # 2. 呼叫 Gemini 分析
        print(f"🧠 正在詢問 AI ({MODEL_NAME})...")
        ai_advice = ask_gemini(history)
        print("\n🤖 AI 建議:\n", ai_advice)
        history[-1]['ai_analysis'] = ai_advice
        
        # 3. 儲存 JSON
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
            
        # 4. 同步至雲端 PostgreSQL (呼叫我們新增的功能)
        upload_data_to_db(product_info)
        
        print("\n🎉 任務完美結束！資料已存入 JSON 與雲端資料庫。")
    else:
        print("❌ 任務失敗")

if __name__ == "__main__":
    main()






        