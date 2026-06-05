from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# ⚠️ 請將這串替換成你剛剛在 DBeaver 成功連線的完整 External Database URL
DATABASE_URL = "DATABASE_URL"
def get_db_connection():
    try:
        # 建立與 Render PostgreSQL 的連線
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"資料庫連線失敗: {e}")
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
        cursor.execute("SELECT * FROM ssd_prices ORDER BY record_date DESC;")
        prices = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"status": "success", "data": prices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))