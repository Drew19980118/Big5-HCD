import pandas as pd
import json
from datasets import load_dataset
import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import os

API_KEY = '50a857aec1164241a3411b5e38e99982'

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

def llm_response(prompt):
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": 1,
        "top_p": 0.95,
        "max_tokens": 400
    }

    ENDPOINT = "https://genai-jp.openai.azure.com/openai/deployments/ln-gpt40/chat/completions?api-version=2024-02-15-preview"

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    return response.json()['choices'][0]['message']['content']

def process_dialogue(index):
    global dialogue_count  # Access the global counter
    utterances = []
    for text in first_twelve_dialogues[index]['utterances']['text']:
        refined_prompt = f"Please translate the following sentence from Japanese into English '{text}'. If the sentence contains any sensitive contents, you are required to ignore them. Most Importantly! You are only allowed to output the translated sentence without any other information!!!"
        response = llm_response(refined_prompt)
        utterances.append(response)

    dialogue_str = ''
    for i, utterance in enumerate(utterances):
        if i % 2 == 0:
            dialogue_str += f'{filtered_train_dialogue[index]["interlocutors"][0]}: {utterance} '
        else:
            dialogue_str += f'{filtered_train_dialogue[index]["interlocutors"][1]}: {utterance} '
    dialogue_str = dialogue_str.strip()

    # Save the dialogue_str to the CSV
    with lock:
        # Increment and print the counter
        dialogue_count += 1
        print(f"completed {dialogue_count} dialogues...")
        df = pd.DataFrame([[dialogue_count, dialogue_str]], columns=["Index", "Dialogue"])
        if not os.path.exists(output_file):
            df.to_csv(output_file, mode='w', header=True, index=False)
        else:
            df.to_csv(output_file, mode='a', header=False, index=False)

# 读取 CSV 文件
interlocutors_df = pd.read_csv('sampled_interlocutors.csv', header=None)

# 替换单引号为双引号并解析 JSON 字符串
interlocutors_df[1] = interlocutors_df[1].apply(lambda x: json.loads(x.replace("'", '"')))

# 加载对话数据集
dialogue_dataset = load_dataset(
    "nu-dialogue/real-persona-chat",
    name="dialogue",
    trust_remote_code=True
)
train_dialogue_dataset = dialogue_dataset['train']

# 从第三个数据开始遍历
for i, row in enumerate(interlocutors_df.iloc[5:].iterrows()):
    _, row_data = row  # iterrows() 返回 (index, row)
    interlocutor_data = row_data[1]  # 提取 JSON 数据

    # 检查 'Interlocutor.id' 是否存在
    interlocutor_id = interlocutor_data.get('interlocutor_id', None)

    # 检查 'Category' 是否存在（假设这是另一个字段）
    category = interlocutor_data.get('Category', None)

    # 过滤对话数据集以获取当前 interlocutor 的对话
    filtered_train_dialogue = train_dialogue_dataset.filter(lambda x: x['interlocutors'][0] == interlocutor_id)

    #获取前十二个对话
    # first_twelve_dialogues = filtered_train_dialogue.select(range(min(12, len(filtered_train_dialogue))))

    first_twelve_dialogues = filtered_train_dialogue.select(range(28, 32))

    # 保存到 CSV 文件
    output_file = f'sampled_HHDs/{category}_{interlocutor_id}_example_dialogues.csv'

    lock = Lock()
    dialogue_count = 0  # Initialize the dialogue count

    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(process_dialogue, range(0, len(first_twelve_dialogues)))