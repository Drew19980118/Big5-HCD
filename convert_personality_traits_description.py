import requests

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
        "max_tokens": 2000
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

prompt = f"""You are an outstanding psychologist. You will be given a user's Big Five personality traits with scores on a 7-point scale. For each trait, please provide a concise description of the user’s personality, explaining what kind of person they are based on the score. The traits include 'Openness,' 'Conscientiousness,' 'Extraversion,' 'Agreeableness,' and 'Neuroticism.'
Example input:
'Openness': 5.333333492279053,
'Conscientiousness': 6.333333492279053,
'Extraversion': 6.25,
'Agreeableness': 6.25,
'Neuroticism': 1.0833333730697632

For each trait:
Explain what the score represents in terms of the user's behavior, tendencies, and characteristics.
Provide insights into how this trait might influence their relationships, work habits, decision-making, or other aspects of their life.
Use clear, concise, and empathetic language to paint a vivid picture of the person.
Only provide the answer. Do not include any other information or introductory text in your response.
"""
# Call the LLM API
result = llm_response(prompt)

print(result)