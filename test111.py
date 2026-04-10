import matplotlib.pyplot as plt
import numpy as np

# 設定支援中文的字體 (Mac 環境)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 時間與簡化後的數據 (萬瓩)
times = ['12:30 (日間)', '19:30 (夜間)']
solar = [849.3, 0]
fossil = [1508.4 + 673.8, 1794.2 + 759.9] # 燃氣+燃煤總和

x = np.arange(len(times))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))

# 繪製長條圖
rects1 = ax.bar(x - width/2, solar, width, label='太陽能', color='#32CD32')
rects2 = ax.bar(x + width/2, fossil, width, label='傳統石化能源 (燃煤+燃氣)', color='#FF6347')

# 加上標籤與標題
ax.set_ylabel('發電量 (萬瓩)', fontsize=12)
ax.set_title('日夜間發電結構對比：太陽能缺口與火力支援', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(times, fontsize=12)
ax.legend(fontsize=11)

# 在柱狀圖上方標示數值
ax.bar_label(rects1, padding=3, fmt='%.1f')
ax.bar_label(rects2, padding=3, fmt='%.1f')

# 加上輔助線與排版優化
ax.yaxis.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# 儲存圖片或顯示
plt.savefig('energy_comparison1.png', dpi=300)
plt.show()