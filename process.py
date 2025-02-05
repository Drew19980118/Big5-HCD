import pandas as pd

# 读取CSV文件
df = pd.read_csv('adapted_dialogues_processed.csv')

# 删除Keyword列为null的行
df = df.dropna(subset=['Keyword'])

# 重新设置Index列
df['Index'] = range(1, len(df) + 1)

# 保存处理后的数据到新的CSV文件
df.to_csv('adapted_dialogues_processed_cleaned.csv', index=False)

print("处理完成，结果已保存到 'adapted_dialogues_processed_cleaned.csv'")