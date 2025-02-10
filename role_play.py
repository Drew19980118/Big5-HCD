import requests
import pandas as pd
import csv
import os

# Configuration
API_KEY = '50a857aec1164241a3411b5e38e99982'

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

def llm_response(prompt):
    # Payload for the request
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
        response.raise_for_status()  # Raise an HTTPError for unsuccessful status codes
        result = response.json()

        # Check response structure validity
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

persona_description = """
1. I am a student. 
2. I am from Saitama Prefecture. 
3. I don't eat breakfast every day. 
4. I go for a walk every day. 
5. I often go to the convenience store. 
6. I type fast. 
7. I have a poor memory. 
8. I have a clear goal for my future. 
9. I can find something fun every day. 
10. I am very particular about the things I like.
"""

personality_traits = """
'Openness': 5.25
AH are a curious and imaginative individual who values creativity and new experiences. AH are likely to enjoy exploring different cultures, ideas, and unconventional ways of thinking. This trait makes AH open-minded and receptive to change, often leading AH to seek out diverse perspectives and innovative solutions in your personal and professional life.

'Conscientiousness': 3.1666667461395264
AH are moderately organized and reliable, though AH may sometimes struggle with maintaining consistent levels of discipline and planning. While AH are capable of setting goals and working towards them, AH might occasionally procrastinate or find it challenging to stay focused. In AH's relationships and work, AH's balance spontaneity with responsibility, often adapting to the needs of the moment.

'Extraversion': 3.3333332538604736
AH have a balanced level of extraversion, enjoying social interactions and activities while also valuing AH's alone time. AH can be outgoing and energetic in social settings, but AH also appreciate periods of solitude to recharge. This trait allows AH to be adaptable in various social environments, maintaining meaningful connections without feeling overwhelmed.

'Agreeableness': 4.166666507720947
AH are generally kind, empathetic, and cooperative, often striving to maintain harmony in AH's relationships. AH value getting along with others and are usually willing to compromise to avoid conflicts. This trait helps AH build strong, supportive relationships, though AH might sometimes prioritize others' needs over AH's own.

'Neuroticism': 4.416666507720947
AH are somewhat prone to experiencing stress and emotional fluctuations, often feeling worried or anxious about potential problems. While this can sometimes lead to moments of self-doubt or moodiness, it also means AH are highly aware of AH's emotions and can be very empathetic towards others. AH's sensitivity allows AH to navigate and respond to emotional situations thoughtfully.
"""

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

# 读取 O_HIgh_AH_example_dialogues.csv 的第二列（含表头）
example_dialogues_df = pd.read_csv('test_interlocutor_dialogues/O_HIgh_AH_example_dialogues.csv')
header = example_dialogues_df.columns[1]
data_rows = example_dialogues_df.iloc[:, 1].astype(str).dropna().tolist()
sample_dialogues_list = [header] + data_rows

index = 1
completed = 1

# Main script for LLM-to-LLM interaction
if __name__ == "__main__":

    # Initialize the output CSV file with headers
    output_file = 'adapted_dialogues.csv'

    file_exists = os.path.exists(output_file)

    # Initialize the output CSV file if it does not exist
    if not file_exists:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Dialogue"])

    df = pd.read_csv('converted_dialogues.csv')

for dialogue in df['Dialogue'].iloc[:].dropna():
    # 根据 completed 计算当前组数（每100个切换一组）
    group_number = (completed - 1) // 100  # 例如 completed=150 → group_number=1

    # group_number = 9
    # 计算数据行起始索引（每组3个对话）
    start_index = group_number * 3
    end_index = start_index + 3

    # 提取当前组的3个对话（自动处理索引越界）
    current_data = sample_dialogues_list[start_index:end_index]

    current_data[0] = 'The first sample dialogue: ' + current_data[0]
    current_data[1] = 'The second sample dialogue: ' + current_data[1]
    current_data[2] = 'The third sample dialogue: ' + current_data[2]

    sample_dialogues = "\n".join(current_data)

    prompt = f"""
        You are an exceptional role player. I need you to temporarily forget your original AI role and embody a specific real person, named AH. I will provide you with the following details:

Persona Description: (A profile of AH’s persona)
Personality Traits Description: (The Big Five personality traits of AH with specific scores on a 7-point scale and detailed descriptions for each trait)
Sample Dialogues: (Real dialogues between AH and another real person)

Additionally, I will provide:
Target Dialogue: A real Human-Computer Dialogue (not a dialogue between AH and the computer).
Additional Knowledge: Insights on the specific differences between Human-Human Dialogues (HHD) and Human-Computer Dialogues (HCD).

Your task:
Based on the Persona Description, Personality Traits Description, and Sample Dialogues, fully embody AH (focusing on how AH interacts with real people). Then, rewrite the User's utterances in the Target Dialogue to align with AH’s persona, style, and traits (adjusting only the style without altering the meaning). The Assistant's utterances in the Target Dialogue must remain unchanged.

IMPORTANT NOTES: Incorporate the Additional Knowledge to ensure the rewritten dialogue accurately reflects the characteristics of AH’s persona while maintaining the semantic coherence of the entire dialogue. Please ensure your output is a rewritten version of the Target Dialogue with the same format as the original Target Dialogue. Do not provide any extra information outside of the rewritten dialogue.

Provided Information:
Persona Description: {persona_description}
Personality Traits Description: {personality_traits}
Sample Dialogues: {sample_dialogues}
Target Dialogue: {dialogue}
Additional Knowledge: {additional_knowledge}
        """

    assistant_context = []
    # User LLM generates a response
    response = llm_response(prompt)
    if response is not None:
        # Append the result to the CSV file
        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([completed, response])
            # Print progress information
            print(f"completed {completed} dialogues...")
            completed += 1

    # Increment the index regardless of success or failure
    index += 1
