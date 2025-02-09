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


additional_knowledge = """
    Differences Between Human Human Dialogue (HHD) and Human Computer Dialogue (HCD):
    Communication Styles:
    HCD: Interactions between humans and machines are characterized by brief, frequent exchanges that prioritize efficiency. Users expect clear, straightforward responses without unnecessary elaboration.
    Example: "It’s 72°F and sunny."
    HHD: Conversations between humans are more nuanced and context-rich, often incorporating additional details, shared thoughts, or collaborative reasoning.
    Example: "It’s 72°F and sunny, but should we bring an umbrella later?"
    Relational and Personality Expression:
    HCD: Interactions between humans and machines are transactional and lack emotional depth or personal connection, as machines are incapable of genuine empathy or emotional understanding.
    Example: When a user expresses stress, a machine might respond neutrally, e.g., "I'm here to help."
    HHD: Human interactions are infused with emotional expression, humor, and openness, fostering trust and mutual understanding. These exchanges often include empathy, support, and shared problem-solving.
    Example: A friend might respond empathetically, e.g., "I understand how you feel. Let’s figure this out together."
    """

dialogue = """AH: Hello!
Computer: Hello.
AH: Do you eat breakfast?
Computer: Yes.
AH: Could you tell me what kind of menu it is?
Computer: Plain white rice with natto.
AH: Is natto rice easy to make and delicious?
Computer: Yes, sometimes with raw eggs.
AH: Raw eggs, natto, and rice seem to be a great match!
Computer: Correct. Can you eat natto?
AH: Yes, I eat it every night.
Computer: Good.
AH: It seems to be good for health.
Computer: Yes. Doctors recommend it.
AH: Even doctors recommend it?
Computer: Yes, as reported in the news.
AH: I didn't think it was that good.
Computer: It also affects lifespan.
AH: Fermented foods are said to be good for your health.
Computer: Correct.
AH: The person who ate it first must be amazing.
Computer: True.
AH: If there are rotten items, I will throw them away.
Computer: Understandable.
AH: The person who made that sauce invented something great.
Computer: Agreed. Natto with a raw egg is good.
AH: I also love that sauce.
Computer: Understood.
AH: It's nice to know others think the same.
Computer: Let's talk again.
"""

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

        result = llm_response(prompt)

        print(f"{dimension['dimension_name'].capitalize()}: {result}\n")