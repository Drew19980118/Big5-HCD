import pandas as pd
import requests
import csv

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

# Load the dataset
df = pd.read_parquet('sampled_turn_6_dialogues.parquet')
df = df.iloc[:]
conversations = df['conversation']

def format_conversation(conversation):
    formatted = []
    for utterance in conversation:
        if utterance['role'] == 'user':
            formatted.append(f"User: {utterance['content']}")
        elif utterance['role'] == 'assistant':
            formatted.append(f"Assistant: {utterance['content']}")
    return '\n'.join(formatted)


# Initialize the output CSV file with headers
output_file = 'converted_dialogues.csv'
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Index", "Dialogue"])

index = 1
completed = 1

for conversation in conversations:
    formatted_conversation = format_conversation(conversation)
    prompt = f"""
    Rewrite the human-computer dialogue I provided below to shorten all Assistant responses exceeding 20 words (summary the responses). Follow these rules:

User Utterances: Keep completely unchanged

Assistant Utterances: Only summary responses with >20 words and most importantly Strict 20 word limit 

Format: Maintain original dialogue structure

Style: Keep responses natural and conversational

The Human-Computer dialogue is:
{formatted_conversation}

Directly output the converted dialogue without any other information.
    """
    # Call the LLM API
    result = llm_response(prompt)

    if result is not None:
        # Append the result to the CSV file
        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([completed, result])
            # Print progress information
            print(f"completed {completed} dialogues...")
            completed += 1

    # Increment the index regardless of success or failure
    index += 1