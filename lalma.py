import time

def count_partitions(n):
    """
    計算整數 n 的拆分總數 (不考慮順序)
    時間複雜度: O(n^2)
    """
    if n < 0:
        return 0
    
    dp = [0] * (n + 1)
    dp[0] = 1 
    
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]
            
    return dp[n]

def main():
    print("========== Python 單核 CPU 壓力測試 (整數拆分) ==========")
    print("提示：測試規模越大，對 CPU 單核心的負載越高。")
    print("入門測試建議輸入 10000，進階測試可挑戰 30000 以上。")
    print("=========================================================")
    
    while True:
        try:
            user_input = input("\n請輸入測試規模 (正整數，輸入 q 退出): ")
            
            if user_input.lower() == 'q':
                print("測試結束。")
                break

            n = int(user_input)
            
            if n < 0:
                print("請輸入大於或等於 0 的數字。")
                continue
                
            print(f"\n[測試開始] 正在運算 p({n})，CPU 單核滿載中，請稍候...")
            
            # 使用 perf_counter 取得最高精度的時間
            start_time = time.perf_counter()
            
            result = count_partitions(n)
            
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            
            # 計算效能指標：
            # 演算法的雙層迴圈總共執行了約 (n * n) / 2 次加法與陣列存取
            operations = (n * n) // 2
            
            # 避免除以零的錯誤（當 n 極小的時候）
            if elapsed_time > 0:
                # 跑分定義：每秒可以執行多少次內層迴圈運算
                score = int(operations / elapsed_time)
            else:
                score = 0

            print("-" * 40)
            # 為了避免終端機被超長數字洗頻，若位數太多則只顯示前後段
            result_str = str(result)
            if len(result_str) > 50:
                print(f"運算結果: {result_str[:20]} ... {result_str[-10:]}")
                print(f"數字長度: {len(result_str)} 位數")
            else:
                print(f"運算結果: {result}")
            
            print(f"耗費時間: {elapsed_time:.4f} 秒")
            print(f"效能跑分: {score:,} (每秒迴圈運算次數)")
            print("-" * 40)
            
        except ValueError:
            print("錯誤：請輸入有效的整數數字。")
        except KeyboardInterrupt:
            # 允許使用者用 Ctrl+C 強制中斷過久的測試
            print("\n測試已手動中斷。")

if __name__ == "__main__":
    main()
