import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import google.generativeai as genai
import re


API_KEY = "AIzaSyDbCq23U_1hQE5vF8IS4fp4lyurPyiourQ"


TARGET_URL = "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=12627127&osm=Ad07&utm_source=googleshop&utm_medium=traffic-pla-3C&gad_source=1&gad_campaignid=22679348820&gbraid=0AAAAADlbkmNQBiC82wiUNXAS1zkcMPUQ7&gclid=Cj0KCQiA_8TJBhDNARIsAPX5qxTy-Jo_TC9SGV9r3_vmd3khcEBYPN-HyzPEaguM6Q9wmYwKyRkil-gaAnSiEALw_wcB"


SELECTOR = "li.special span" 


DB_FILE = "price_data.json"

MODEL_NAME = "gemini-2.5-flash"


genai.configure(api_key=API_KEY)

def get_price():
    """ 爬取 Momo 網頁並抓出價格 """
    try:
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.momoshop.com.tw/'
        }
        
        response = requests.get(TARGET_URL, headers=headers)
        response.encoding = 'utf-8' 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        price_element = soup.select_one(SELECTOR)
        
        
        if not price_element:
             price_element = soup.select_one(".price span")
             
        if not price_element:
            print(f"❌ 找不到價格，可能 Momo 改版或被擋了")
            return None

        
        raw_price = price_element.text.strip()
        
        clean_price = ''.join(filter(str.isdigit, raw_price))
        
        if not clean_price:
            print(f"❌ 抓到了元素但裡面沒數字: {raw_price}")
            return None
            
        return int(clean_price)
    except Exception as e:
        print(f"❌ 爬蟲發生錯誤: {e}")
        return None

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
        return "暫無法取得 AI 分析 (請檢查 API Key 或模型名稱)"

def main():
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []

    print("🕷️ 正在爬取 Momo 價格...")
    current_price = get_price()

    if current_price:
        today = datetime.date.today().strftime("%Y-%m-%d")
        print(f"💰 抓到價格: ${current_price}")

        
        if history and history[-1]['date'] == today:
            history[-1]['price'] = current_price
            print("📅 更新今日價格記錄")
        else:
            history.append({"date": today, "price": current_price})
            print("📝 新增一筆記錄")

        # 呼叫 Gemini
        print(f"🧠 正在詢問 AI ({MODEL_NAME})...")
        ai_advice = ask_gemini(history)
        print("\n🤖 AI 建議:", ai_advice)
        
        history[-1]['ai_analysis'] = ai_advice

        
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        print("\n✅ 完成！資料已存入 SSD。")
    else:
        print("❌ 任務失敗")

if __name__ == "__main__":
    main()