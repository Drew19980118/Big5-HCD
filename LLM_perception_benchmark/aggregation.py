import os
import statistics

def extract_final_scores(folder_path):
    """
    从指定文件夹中的所有txt文件中提取Final Score (Median of Medians)的值
    """
    final_scores = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # 获取最后一行并提取数值
            last_line = lines[-1]
            final_score = float(last_line.split(': ')[1].strip())
            final_scores.append(final_score)

    return final_scores

def calculate_average(scores):
    """
    计算列表中数值的平均值
    """
    if len(scores) == 0:
        return 0  # 避免除以0
    return sum(scores) / len(scores)

def calculate_std_dev(scores):
    """
    计算列表中数值的标准差
    """
    if len(scores) < 2:
        return 0  # 标准差至少需要两个数据点
    return statistics.stdev(scores)

# 定义文件夹路径
folders = [
    "deepseek_evaluation_results",
    "llama3_evaluation_results",
    "gemma2_evaluation_results"
]

# 提取每个文件夹的Final Score并计算平均值和标准差
results = {}
for folder in folders:
    scores = extract_final_scores(folder)
    average = calculate_average(scores)
    std_dev = calculate_std_dev(scores)
    results[folder] = {
        "scores": scores,
        "average": average,
        "std_dev": std_dev
    }

# 将结果写入txt文件
with open("llm_evaluators_benchmarks.txt", "w") as output_file:
    for folder, data in results.items():
        output_file.write(f"Evaluator: {folder}\n")
        output_file.write(f"Final Scores: {data['scores']}\n")
        output_file.write(f"Average: {data['average']}\n")
        output_file.write(f"Standard Deviation: {data['std_dev']}\n")
        output_file.write("-" * 30 + "\n")