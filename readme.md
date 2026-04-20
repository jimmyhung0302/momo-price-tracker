記憶體與 SSD 價格追蹤與 AI 分析系統 (程式設計 II 期中專題)
專題介紹
近日記憶體與 SSD 價格波動劇烈，本專題旨在開發一款自動化爬蟲軟體，專門追蹤電商平台上的 DDR5 與 Gen 4 SSD 價格。透過結合 Gemini API，系統能對收集到的數據進行即時分析與未來價格趨勢預測，並透過視覺化網頁呈現最終結果。

使用技術
後端與爬蟲： Python, BeautifulSoup, JSON 數據處理

AI 分析： Google Gemini API (google.generativeai)

自動化工作流： Docker, n8n (設定定時排程執行)

前端展示： HTML, CSS, JavaScript, GitHub Pages

系統亮點與克服挑戰
成功突破 Momo 購物網的反爬蟲機制與動態 Selector 限制。

整合 n8n 自動化工具，實現完全無需人工介入的定時價格抓取。

解決 macOS 下 Docker 的網路限制與 Safari 安全性阻擋問題。

如何執行 (安裝與使用方式)
複製此專案：git clone [你的 GitHub 網址]

建立並啟動 Conda 虛擬環境

安裝必要套件：pip install -r requirements.txt

執行爬蟲程式：python bot.py

啟動本地端伺服器檢視網頁：python -m http.server

AI 協作聲明
本專案開發過程全程採用 AI (Gemini) 輔助，涵蓋架構規劃、程式碼生成、環境除錯、突破反爬蟲限制以及 Docker/n8n 部署設定。詳細對話紀錄與截圖請參閱期中簡報。

相關連結
專題展示網站： [(https://jimmyhung0302.github.io/momo-price-tracker/)]

期中簡報檔： [請替換成你的簡報 PDF 或 Google Slides 連結]

執行展示影片 (YouTube)： https://youtu.be/mGx7TMgrF4k
