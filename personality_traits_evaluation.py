import requests
import pandas as pd

# 定义五个维度的描述
dimensions = [
    {
        "dimension_name": "openness",
        "description": "This dimension captures cognitive curiosity and appreciation for novelty. \n"
                       "High scorers tend to be imaginative, creative, and open to unconventional ideas, while low scorers prefer routine, practicality, and traditional values."
    },
    {
        "dimension_name": "conscientiousness",
        "description": "This dimension reflects self-discipline and goal-directed behavior. \n"
                       "High scorers are organized, reliable, and detail-oriented; low scorers may be spontaneous, flexible, or less focused on long-term planning."
    },
    {
        "dimension_name": "extraversion",
        "description": "This dimension measures engagement with the external world. \n"
                       "High scorers seek social interaction, assertiveness, and stimulation (e.g., enthusiasm, talkativeness), while low scorers (introverts) prefer solitude or quieter environments"
    },
    {
        "dimension_name": "agreeableness",
        "description": "This dimension relates to interpersonal tendencies and compassion. \n"
                       "High scorers prioritize harmony, trust, and empathy, whereas low scorers may be more competitive, skeptical, or direct in communication."
    },
    {
        "dimension_name": "neuroticism",
        "description": "This dimension assesses emotional reactivity and resilience. \n"
                       "High scorers experience frequent negative emotions (e.g., anxiety, sadness) and stress sensitivity; low scorers remain calm and emotionally steady under pressure."
    },
]

additional_knowledge = """
Differences Between Human-Human (HHD) and Human-Computer Dialogues (HCD):

Communication Styles:

HCD: Humans interact with machines using shorter, more frequent exchanges, emphasizing efficiency and expecting direct, concise responses.
Example: "It’s 72°F and sunny."
HHD: Human conversations are richer in context and often include additional details or shared thoughts.
Example: "It’s 72°F and sunny, but should we bring an umbrella later?"
Relational and Empathetic Engagement:

HCD: Interactions with machines are transactional, lacking emotional depth or personal connection, as machines are not capable of genuine empathy.
Example: When stressed, a machine might respond neutrally, e.g., "I'm here to help."
HHD: Human interactions include empathy and emotional resonance, often showing understanding and support.
Example: A friend might reply empathetically, e.g., "I understand how you feel. Let’s figure this out together."
Personality Expression:

HCD: Humans often use formal and polite language when interacting with machines, reflecting a transactional and task-oriented tone.
Example: "Could you please help me?"
HHD: Conversations with humans allow for more casual, expressive, and dynamic tones, including emotional cues such as emojis.
Example: "Hey, can you give me a hand? 😊"
"""

# 配置
API_KEY = '50a857aec1164241a3411b5e38e99982'

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}


def llm_response(prompt):
    # 请求的 payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 1,
        "top_p": 0.95,
        "max_tokens": 400
    }

    ENDPOINT = "https://genai-jp.openai.azure.com/openai/deployments/ln-gpt40/chat/completions?api-version=2024-02-15-preview"

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # 对于不成功的状态码抛出 HTTPError
        result = response.json()

        # 检查响应结构的有效性
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            print("Unexpected response format:", result)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except KeyError as e:
        print(f"Key error while parsing response: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None


# 读取 CSV 文件
df = pd.read_csv('interview_dialogues.csv')

# 打开一个文件来存储结果
with open('assessment_results.txt', 'w') as result_file:
    # 遍历每个对话
    total_dialogues = len(df)  # 总对话数
    print(f"Total dialogues to process: {total_dialogues}")

    for index, row in df.iterrows():
        dialogue = row['Dialogue']
        print(f"\nProcessing Dialogue {index + 1} of {total_dialogues}...")  # 显示当前处理的对话序号

        result_file.write(f"Dialogue {index + 1}:\n")

        # 对每个维度进行评估
        for dimension in dimensions:
            print(f"  Assessing {dimension['dimension_name']}...")  # 显示当前评估的维度

            prompt = f"""
            You are an expert in Psychometrics, especially Big Five. I am conducting the Big Five test on someone. I am gauging
            his/her position on the {dimension['dimension_name']} dimension through a dialogue. For clarity, here’s some background
            this particular dimension:
            ===
            {dimension['description']}
            ===
            I’ve invited a participant, AH, and I have a dialogue between AH and Computer (Human Computer Dialogue) in English. I
            will input the dialogue.

            ##Dialogue:
            {dialogue}

            Besides, I will provide you the additional knowledge regarding the difference between Human Human Dialogue (HHD) and Human Computer Dialogue (HCD):
            ##Additional Knowledge:
            {additional_knowledge}

            Please help me assess AH’s score within the {dimension['dimension_name']} dimension of Big Five (your assessment should consider the additional knowledge).
            You should provide the score of AH in terms of {dimension['dimension_name']}, which is a number between 0 and
            7. 0 denotes 'not {dimension['dimension_name']} at all', 3.5 denotes 'neutral', and 7 denotes
            'strongly {dimension['dimension_name']}'. Other numbers in this range represent different degrees of '{dimension['dimension_name']}'. Note, you must present your answer. Please directly output the score without any other information.
            """
            # 调用 LLM API
            result = llm_response(prompt)
            if result:
                result_file.write(f"{dimension['dimension_name'].capitalize()}: {result}\n")
            else:
                result_file.write(f"{dimension['dimension_name'].capitalize()}: Assessment failed\n")

        result_file.write("\n")  # 每个对话之间留空行

print("\nAssessment completed and results saved to assessment_results.txt")