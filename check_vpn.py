import urllib.request
import json

def check_vpn_status():
    print("正在查詢目前的網路狀態，請稍候...\n")
    try:
        # 呼叫免費的 IP 查詢 API
        url = "https://ipinfo.io/json"
        
        # 發送請求並讀取回應
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

        print("=== 🌐 你的網路身份 ===")
        print(f"📍 目前的 IP 地址 : {data.get('ip')}")
        print(f"🏢 網路供應商 (ISP): {data.get('org')}")
        print(f"🌍 所在城市 / 國家 : {data.get('city')}, {data.get('country')}")
        
        print("\n=== 💡 如何判斷？ ===")
        print("👉 如果上面的「國家」或「ISP」顯示的是你【真正的所在地】和【原本的電信公司】（例如台灣、中華電信），代表 VPN 其實沒在運作（或是俗稱的漏 IP 了）。")
        print("👉 如果顯示的是你【設定的 VPN 節點】（例如日本、美國的某家機房），就代表 VPN 有成功把你的流量帶出去！")

    except Exception as e:
        print(f"❌ 查詢失敗，請檢查是不是完全斷網了。錯誤細節：{e}")

if __name__ == "__main__":
    check_vpn_status()