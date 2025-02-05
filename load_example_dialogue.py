import os
import pandas as pd
import requests
from datasets import load_dataset
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

API_KEY = '50a857aec1164241a3411b5e38e99982'
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

dialogue_dataset = load_dataset(
    "nu-dialogue/real-persona-chat",
    name="dialogue",
    trust_remote_code=True
)
train_dialogue_dataset = dialogue_dataset['train']

# Filter the dataset where 'AH' is in the 'interlocutor' column
filtered_train_dialogue = train_dialogue_dataset.filter(lambda x: 'AH' in x['interlocutors'])

output_file = 'example_dialogues.csv'

lock = Lock()
dialogue_count = 0  # Initialize the dialogue count

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
    for text in filtered_train_dialogue[index]['utterances']['text']:
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

with ThreadPoolExecutor(max_workers=1) as executor:
    executor.map(process_dialogue, range(0, len(filtered_train_dialogue)))