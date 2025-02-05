import re

# 打开评估结果文件
with open('assessment_results.txt', 'r') as file:
    content = file.read()

# 初始化一个字典来存储每个维度的分数
trait_scores = {
    "openness": [],
    "conscientiousness": [],
    "extraversion": [],
    "agreeableness": [],
    "neuroticism": []
}

# 正则表达式匹配每个维度的分数
pattern = re.compile(
    r'(Openness|Conscientiousness|Extraversion|Agreeableness|Neuroticism):\s*([\d.]+)',
    re.IGNORECASE
)

# 查找所有匹配的分数
matches = pattern.findall(content)

# 将分数存储到对应的维度列表中
for trait, score in matches:
    trait_lower = trait.lower()  # 统一转换为小写
    trait_scores[trait_lower].append(float(score))

# 计算每个维度的平均分数
average_scores = {}
for trait, scores in trait_scores.items():
    if len(scores) > 0:  # 检查分数列表是否为空
        average_scores[trait] = sum(scores) / len(scores)
    else:
        print(f"Warning: No scores found for {trait}. Skipping average calculation.")
        average_scores[trait] = None  # 如果没有分数，设置为 None

# 将平均分数写入新的文件
with open('average_results.txt', 'w') as output_file:
    for trait, avg_score in average_scores.items():
        if avg_score is not None:
            output_file.write(f"{trait.capitalize()}: {avg_score:.2f}\n")
        else:
            output_file.write(f"{trait.capitalize()}: No data available\n")

print("Average scores calculated and saved to average_results.txt")