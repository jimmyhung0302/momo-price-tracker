import time

def count_partitions(n):
    if n < 0: return 0
    dp = [0] * (n + 1)
    dp[0] = 1 
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]
    return dp[n]

def main():
    print("========== Python 單核 CPU 壓力測試 (整數拆分) ==========")
    
    while True:
        try:
            user_input = input("\n請輸入測試規模 (輸入 q 退出): ")
            if user_input.lower() == 'q': break

            n = int(user_input)
            print(f"\n[測試開始] 正在運算 p({n})...")
            
            start_time = time.perf_counter()
            result = count_partitions(n)
            end_time = time.perf_counter()
            
            elapsed_time = end_time - start_time
            operations = (n * n) // 2
            score = int(operations / elapsed_time) if elapsed_time > 0 else 0

            
            if score > 12_000_000:
                status = "頂級單核效能 (高頻處理器/Apple M Pro系列)"
            elif score > 8_000_000:
                status = "優異效能 (主流桌面級 CPU)"
            elif score > 5_000_000:
                status = "中等效能 (筆電/舊款 CPU)"
            else:
                status = "低負載效能 (直譯器限制或低功耗模式)"
            # ---------------------

            print("-" * 40)
            result_str = str(result)
            if len(result_str) > 50:
                print(f"數字長度: {len(result_str)} 位數")
            
            print(f"耗費時間: {elapsed_time:.4f} 秒")
            print(f"效能跑分: {score:,} (ops/sec)")
            print(f"效能評價(以p=20000為基準): {status}") 
            print("-" * 40)
            
        except ValueError:
            print("錯誤：請輸入有效的整數。")
        except KeyboardInterrupt:
            print("\n測試中斷。")
            break

if __name__ == "__main__":
    main()
