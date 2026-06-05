import time
import statistics

def count_partitions(n):
    """計算整數拆分的動態規劃函數"""
    if n < 0: return 0
    dp = [0] * (n + 1)
    dp[0] = 1 
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]
    return dp[n]

def run_single_search(run_index):
    """執行一次完整的動態縮圈效能尋找"""
    start_n = 1000
    end_n = 10000
    step = 1000
    
    global_best_n = 0
    global_max_score = 0
    
    # 這裡為了畫面整潔，單次尋找過程中我們只印出精簡資訊
    print(f"\n▶ 正在執行第 {run_index} 次完整尋找 ", end="", flush=True)

    while step >= 1:
        local_best_n = 0
        local_max_score = 0
        
        for n in range(start_n, end_n + 1, step):
            start_time = time.perf_counter()
            count_partitions(n)
            end_time = time.perf_counter()
            
            elapsed_time = end_time - start_time
            operations = (n * n) // 2
            score = int(operations / elapsed_time) if elapsed_time > 0 else 0
            
            if score > local_max_score:
                local_max_score = score
                local_best_n = n

        if local_max_score > global_max_score:
            global_max_score = local_max_score
            global_best_n = local_best_n

        if step == 1:
            break
            
        start_n = max(1000, local_best_n - step) 
        end_n = local_best_n + step              
        
        step = step // 10 
        if step == 0: step = 1
        
        # 印出進度點
        print(".", end="", flush=True)
        
    print(f" 完成! 最佳 n = {global_best_n}, 跑分 = {global_max_score:,}")
    return global_best_n, global_max_score

def main():
    print("========== Python 單核 CPU 效能穩定度統計系統 ==========")
    
    # 讓使用者輸入測試次數
    while True:
        try:
            num_tests = int(input("請輸入要執行幾次完整測試 (建議 5 到 10 次): "))
            if num_tests < 1:
                print("次數必須大於 0，請重新輸入。")
                continue
            break
        except ValueError:
            print("格式錯誤，請輸入整數。")

    best_n_list = []
    max_score_list = []

    # 執行多次測試
    start_total_time = time.time()
    for i in range(1, num_tests + 1):
        best_n, max_score = run_single_search(i)
        best_n_list.append(best_n)
        max_score_list.append(max_score)
    end_total_time = time.time()

    # ---------------- 統計數據計算 ----------------
    print("\n" + "="*50)
    print("📊 統計結果分析報告")
    print(f"總耗時: {end_total_time - start_total_time:.2f} 秒")
    print("-" * 50)
    
    print("【最佳甜蜜點 (n) 的統計】")
    print(f"所有結果: {best_n_list}")
    print(f"平均值 (Mean):   {statistics.mean(best_n_list):.2f}")
    
    print(f"中位數 (Median): {statistics.median(best_n_list)}")
    
    # 計算標準差需要至少 2 筆資料
    if num_tests >= 2:
        print(f"標準差 (Stdev):  {statistics.stdev(best_n_list):.2f} (越小代表越穩定)")
    else:
        print("標準差 (Stdev):  資料不足，需至少測試 2 次")

    print("\n【極限跑分 (ops/sec) 的統計】")
    print(f"平均值 (Mean):   {int(statistics.mean(max_score_list)):,}")
    mean_score = int(statistics.mean(max_score_list))

# 直接拿純數字跟 20000 比較
    if mean_score > 25000000:
       print("頂級單核效能")
    elif mean_score >20000000:
        print(f"中階單核效能")
    elif mean_score > 15000000:
        print(f"低階單核效能")
    else:
        print(f"低負載運轉")
    
    print(f"中位數 (Median): {int(statistics.median(max_score_list)):,}")
    
    if num_tests >= 2:
        print(f"標準差 (Stdev):  {int(statistics.stdev(max_score_list)):,} (越小代表跑分越無波動)")
    print("="*50)

if __name__ == "__main__":
    main()