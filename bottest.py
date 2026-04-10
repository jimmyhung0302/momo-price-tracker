import requests
from bs4 import BeautifulSoup
import re

TARGET_URL = "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=12627127"

def get_price():
    """ 爬取 Momo 網頁並抓出價格 """
    try:
       
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.momoshop.com.tw/',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        response = requests.get(TARGET_URL, headers=headers, timeout=10)
        response.encoding = 'utf-8' 
        
        if response.status_code != 200:
            print(f" 請求失敗，狀態碼: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        selectors = [
            "li.special span",      
            ".price_area .price",  
            "#countPrice",          
            "meta[property='product:price:amount']" 
        ]
        
        price = None
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
               
                raw_val = element.get('content') if element.name == 'meta' else element.text
                clean_price = ''.join(filter(str.isdigit, raw_val))
                if clean_price:
                    price = int(clean_price)
                    break
        
        if price:
            return price
        else:
            print("找不到價格元素，請檢查 URL 是否有效或 Momo 是否改版")
            return None

    except Exception as e:
        print(f"發生錯誤: {e}")
        return None

if __name__ == "__main__":
    current_price = get_price()
    if current_price:
        print(f"今日單價: {current_price}")
#hihi
