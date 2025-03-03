import pandas as pd
import ast
import random
from datasets import load_dataset

# --------------------- 第一部分：处理CSV并生成分类 ---------------------
def process_personality_data(csv_path):
    """处理性格特征数据并生成分类和阈值"""
    # 读取CSV文件
    df = pd.read_csv(csv_path, header=None, names=['user_id', 'personality_dict'])

    # 转换字典格式
    df['personality_dict'] = df['personality_dict'].apply(ast.literal_eval)
    personality_df = pd.json_normalize(df['personality_dict'])

    # 合并数据
    result_df = pd.concat([df['user_id'], personality_df], axis=1)

    # 定义分析维度
    dimensions = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']

    # 初始化存储结构
    classification = {dim: {'low': [], 'middle': [], 'high': []} for dim in dimensions}
    thresholds = {}

    # 计算分位数并分类
    for dim in dimensions:
        q33 = result_df[dim].quantile(0.33)
        q66 = result_df[dim].quantile(0.66)
        thresholds[dim] = {'33rd': q33, '66th': q66}

        classification[dim]['low'] = result_df[result_df[dim] <= q33]['interlocutor_id'].tolist()
        classification[dim]['middle'] = result_df[(result_df[dim] > q33) & (result_df[dim] <= q66)][
            'interlocutor_id'].tolist()
        classification[dim]['high'] = result_df[result_df[dim] > q66]['interlocutor_id'].tolist()

    return thresholds, classification


# --------------------- 第二部分：采样并统计对话数据 ---------------------
def sample_and_count(thresholds, classification):
    """从分类中采样并统计对话数量"""
    # 加载数据集
    dialogue_dataset = load_dataset(
        "nu-dialogue/real-persona-chat",
        name="dialogue",
        trust_remote_code=True
    )
    train_dialogue = dialogue_dataset['train']

    # 预先计算所有ID的对话数量
    all_ids = list({id for dim in classification.values()
                    for cat in dim.values() for id in cat})
    id_counts = {}
    for interlocutor_id in all_ids:
        filtered = train_dialogue.filter(
            lambda x: x['interlocutors'][0] == interlocutor_id
        )
        id_counts[interlocutor_id] = len(filtered)

    # 采样逻辑
    selected_ids = set()
    sampled_info = []

    # 遍历所有维度（5）和分类（3）
    for dim in classification:
        for category in ['low', 'middle', 'high']:
            candidates = classification[dim][category]

            # 过滤候选：未选中且对话数>=12
            available = [id for id in candidates
                         if id not in selected_ids
                         and id_counts.get(id, 0) >= 12]

            # 重试直到找到符合条件的候选
            while True:
                if not available:
                    raise ValueError(f"维度 {dim} 分类 {category} 没有符合条件的ID")

                random.shuffle(available)
                selected = available[0]

                # 确保对话数量符合要求
                if id_counts[selected] >= 12:
                    break
                else:
                    available.pop(0)  # 移除不合格的候选
                    continue

            # 记录选择信息
            selected_ids.add(selected)
            sampled_info.append({
                'id': selected,
                'dimension': dim,
                'category': category,
                'count': id_counts[selected],
                'thresholds': thresholds[dim]
            })

    return sampled_info


# --------------------- 输出结果到文件 ---------------------
def write_results(sampled_info, thresholds, total, output_path="Big5_HCD_statistics.txt"):
    with open(output_path, 'w', encoding='utf-8') as f:
        # 写入阈值信息
        f.write("维度分位数阈值:\n")
        for dim in thresholds:
            f.write(f"{dim}:\n")
            f.write(f"  33rd百分位数: {thresholds[dim]['33rd']:.4f}\n")
            f.write(f"  66th百分位数: {thresholds[dim]['66th']:.4f}\n")
            f.write("-" * 40 + "\n")

        # 写入采样结果
        f.write("\n采样结果详情:\n")
        for idx, info in enumerate(sampled_info, 1):
            f.write(f"{idx}. ID: {info['id']}\n")
            f.write(f"   所属维度: {info['dimension']}\n")
            f.write(f"   分类类别: {info['category']}\n")
            f.write(f"   对话数量: {info['count']}\n")
            f.write(f"   分位数阈值: 33rd={info['thresholds']['33rd']:.4f}, 66th={info['thresholds']['66th']:.4f}\n")
            f.write("-" * 60 + "\n")

        # 写入统计信息
        f.write(f"\n总计对话数量: {total}\n")
        f.write(f"平均每个ID: {total / len(sampled_info):.1f}\n")


# --------------------- 主程序执行 ---------------------
if __name__ == "__main__":
    # 配置参数
    CSV_PATH = "interlocutor_personality_traits.csv"  # 根据实际路径修改

    # 第一步：处理性格数据
    thresholds, classification = process_personality_data(CSV_PATH)

    # 第二步：采样并统计
    sampled_info = sample_and_count(thresholds, classification)

    # 计算总数
    total = sum(info['count'] for info in sampled_info)

    # 第三步：写入结果文件
    write_results(sampled_info, thresholds, total)

    # 控制台输出
    print("处理完成！结果已保存到results.txt")
    print(f"总计对话数量: {total}")
    print(f"采样ID列表: {[info['id'] for info in sampled_info]}")