import matplotlib.pyplot as plt

# 数据
deepseek = [0.8500000000000001, 0.8899999999999999, 0.985, 0.8875, 0.95, 0.9, 1.0, 0.95, 0.9, 0.9, 1.0, 0.8, 0.9125, 0.9875, 0.8625]
llama3 = [0.8, 0.8, 0.8, 0.75, 0.75, 0.8, 0.8, 0.8, 0.8, 0.9, 0.8, 0.8, 0.8, 0.8, 0.8]
gemma2 = [0.8, 0.755, 0.8, 0.8, 0.7525, 0.775, 0.8, 0.8, 0.8, 0.9, 0.9, 0.8, 0.8, 0.875, 0.8]

# 全局设置字体
plt.rcParams['font.size'] = 20  # 设置字体大小
plt.rcParams['font.weight'] = 'bold'  # 设置字体加粗

# 将数据组合成一个列表
data = [deepseek, llama3, gemma2]

# 定义颜色（符合科研美感的颜色）
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 蓝色、橙色、绿色

# 创建箱线图
fig, ax = plt.subplots(figsize=(13, 8))  # 设置图形大小
boxplot = ax.boxplot(data, patch_artist=True, labels=['DeepSeek R1', 'LLaMA 3', 'Gemma 2'])

# 为每个箱线图设置颜色
for patch, color in zip(boxplot['boxes'], colors):
    patch.set_facecolor(color)

# 设置箱线图的线条颜色
for element in ['whiskers', 'caps', 'medians']:
    plt.setp(boxplot[element], color='black')

# 高亮显示中位线
# for median in boxplot['medians']:
#     median.set(color='red', linewidth=3)  # 设置中位线为红色并加粗

# 添加标题和标签
ax.set_title('Distribution of The Final Confidence Scores Across Three LLM Evaluators', fontsize=20, pad=20, weight='bold')
ax.set_ylabel('Confidence Score', fontsize=20, weight='bold')
ax.set_xlabel('Model', fontsize=20, weight='bold')

# 设置网格线（科研图表中常用）
ax.grid(True, linestyle='--', alpha=0.6)

# 保存为 PDF 文件
plt.savefig('boxplot.pdf', format='pdf', bbox_inches='tight')

# 显示图形
plt.tight_layout()
plt.show()

