import pandas as pd

# 读取 CSV 文件
file_path = 'adapted_dialogues.csv'
df = pd.read_csv(file_path)

# 定义处理函数
def process_dialogue(dialogue):
    # 检查是否存在 'User:'
    if 'User:' in dialogue:
        user_index = dialogue.find('User:')  # 找到第一个 'User:' 的位置

        # 检查 'User:' 前是否存在 'Assistant:'
        assistant_index = dialogue.find('Assistant:')  # 找到第一个 'Assistant:' 的位置
        if assistant_index != -1 and assistant_index < user_index:
            # 如果 'Assistant:' 存在且在 'User:' 前，保留 'Assistant:' 及其后内容
            return dialogue[assistant_index:]
        else:
            # 如果 'Assistant:' 不存在或不在 'User:' 前，保留 'User:' 及其后内容
            return dialogue[user_index:]
    # 如果不包含 'User:'，返回原始数据
    return dialogue

# 对 Dialogue 列应用处理函数
df['Dialogue'] = df['Dialogue'].astype(str).apply(process_dialogue)

# 保存到新文件
output_file = 'adapted_dialogues_processed.csv'
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"处理完成，结果已保存到 {output_file}")