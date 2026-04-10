def count_partitions(n):
   
    if n < 0:
        return 0
    
    
    dp = [0] * (n + 1)
    dp[0] = 1 
    
    
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]
            
    return dp[n]

def main():
    print("--- 整數拆分計數器 ---")
    try:
        user_input = input("請輸入一個正整數 (輸入 q 退出): ")
        
        if user_input.lower() == 'q':
            return

        n = int(user_input)
        
        if n < 0:
            print("請輸入大於或等於 0 的數字。")
        else:
            result = count_partitions(n)
            print(f"數字 {n} 的拆分方案總共有: {result} 種")
            
    except ValueError:
        print("錯誤：請輸入有效的整數數字。")

if __name__ == "__main__":
    main()