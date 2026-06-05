import numpy as np
import matplotlib.pyplot as plt

# 1. 建立 theta 的範圍，從 0 到 2*pi，取 1000 個點讓曲線平滑
theta = np.linspace(0, 2 * np.pi, 1000)

# 2. 定義第 3 題的極坐標方程式 r = 2 + 3*sin(theta)
r = 2 + 3 * np.sin(theta)

# 3. 建立畫布與極坐標軸 (polar projection)
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))

# 4. 繪製曲線
ax.plot(theta, r, color='b', linewidth=2, label='r = 2 + 3sin(θ)')

# 5. 設定標題與圖例
ax.set_title('Q3: Graph of Polar Equation', fontsize=14, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

# 6. 顯示格線並呈現圖形
ax.grid(True)
plt.show()