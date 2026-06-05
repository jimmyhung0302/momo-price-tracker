from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允許前端跨域請求 (很重要！這樣 Vercel 上的網頁才能讀取這個 API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⚠️ 請替換成你真實的 External Database URL
DATABASE_URL = "DATABASE_URL"
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"資料庫連線失敗: {e}")
        return None

# 測試用首頁
@app.get("/")
def read_root():
    return {"message": "歡迎來到 Momo 記憶體/SSD 追蹤 API"}

# 建立讀取價格歷史的 API 端點
@app.get("/api/prices")
def get_prices():
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="無法連線到資料庫")
    
    try:
        # 使用 RealDictCursor 讓資料直接變成字典格式 (JSON)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # 依照日期排序，最新的在前面
        cursor.execute("SELECT * FROM ssd_prices ORDER BY record_date DESC;")
        prices = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"status": "success", "data": prices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))