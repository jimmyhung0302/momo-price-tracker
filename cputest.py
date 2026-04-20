import time
import multiprocessing
import math

def cpu_bound_task(iterations):
    """核心壓力測試任務"""
    result = 0
    for i in range(iterations):
        result += math.sqrt(i)
    return result

def calibrate_m2(target_seconds=60):
    """
    先進行短時間測試，推算跑滿指定秒數需要的運算量。
    這樣可以確保不管是在插電還是電池模式，都能精準跑到 1 分鐘。
    """
    print(f"⏳ 正在對晶片進行快速校準，計算 {target_seconds} 秒所需的運算量...")
    start_time = time.time()
    test_iterations = 20_000_000  # 用 2000 萬次來測速
    
    cpu_bound_task(test_iterations)
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    # 計算每秒可以執行幾次
    iterations_per_second = test_iterations / time_taken
    
    # 計算目標秒數的總運算量 (加上 5% 緩衝，確保「至少」跑滿 1 分鐘)
    required_workload = int(iterations_per_second * target_seconds * 1.05)
    
    print(f"⚡️ 校準完成！單核每秒約可執行 {iterations_per_second:,.0f} 次")
    print(f"🎯 已將每個核心的運算量鎖定為: {required_workload:,} 次\n")
    
    return required_workload

def run_benchmark(cores_to_use, workload_per_core):
    total_workload = workload_per_core * cores_to_use
    
    print(f"🚀 開始 M2 晶片 {cores_to_use} 核心 1 分鐘耐力測試...")
    print(f"👉 總運算量將高達: {total_workload:,} 次")
    print("🔥 測試進行中，請稍候 (你可以打開 macOS 的「活動監視器」查看 CPU 負載)...\n")
    
    start_time = time.time()

    with multiprocessing.Pool(processes=cores_to_use) as pool:
        pool.map(cpu_bound_task, [workload_per_core] * cores_to_use)

    end_time = time.time()
    time_taken = end_time - start_time
    
    operations_per_second = total_workload / time_taken
    score = int(operations_per_second / 20000)

    print(f"ㄋ測試完成！")
    print(f"⏱️ 總耗時: {time_taken:.2f} 秒")
    print(f"🏆 M2 長時效能綜合跑分: {score:,} 分")

if __name__ == '__main__':
    # M2 晶片通常有 8 個核心 (4個效能核心 + 4個節能核心)
    total_cores = multiprocessing.cpu_count()
    print(f"🖥️ 系統偵測到 {total_cores} 個邏輯核心。")

    try:
        user_input = input(f"請輸入你要測試的核心數 (1 - {total_cores}): ")
        cores = int(user_input)
        
        if cores < 1:
            cores = 1
        elif cores > total_cores:
            cores = total_cores
            
    except ValueError:
        cores = total_cores

    # 1. 自動測速並決定 1 分鐘所需的運算量
    target_time = 60 # 設定目標時間為 60 秒
    workload = calibrate_m2(target_seconds=target_time)

    # 2. 正式開始耐力跑分
    run_benchmark(cores, workload)