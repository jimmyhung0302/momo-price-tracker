from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 👈 1. 載入 CORS 套件
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import traceback

app = FastAPI()

# 👇 2. 加上這整段 CORS 設定，允許 GitHub Pages 來拿資料
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源 (包含你的 GitHub Pages)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 記得要用環境變數讀密碼喔！
DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except Exception as e:
        # 完整印出錯誤追蹤，而不僅僅是錯誤訊息
        print(f"詳細錯誤發生：{traceback.format_exc()}")
        return None

@app.get("/")
def read_root():
    return {"message": "歡迎來到 DRAM/SSD 追蹤 API"}

# 建立讀取價格的 API 端點
@app.get("/api/prices")
def get_prices():
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="無法連線到資料庫")
    
    try:
        # 使用 RealDictCursor 讓撈出來的資料直接變成 Python 字典格式 (JSON)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT record_date, model_name, capacity, price, ai_analysis FROM ssd_prices ORDER BY record_date DESC")
        prices = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"status": "success", "data": prices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))