import requests
import ast
import csv

# Configuration
API_KEY = '50a857aec1164241a3411b5e38e99982'
ENDPOINT = "https://genai-jp.openai.azure.com/openai/deployments/ln-gpt40/chat/completions?api-version=2024-02-15-preview"

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

def generate_personality_description(row):
    try:
        data = ast.literal_eval(row[1])
        interlocutor_id = data['interlocutor_id']

        # 创建prompt模板
        prompt = f"""You are an outstanding psychologist. You will be given a interlocutor's Big Five personality traits with scores on a 7-point scale. For each trait, please provide a concise description of the interlocutor’s personality, explaining what kind of person they are based on the score. The traits include 'Openness,' 'Conscientiousness,' 'Extraversion,' 'Agreeableness,' and 'Neuroticism.'
        ## Interlocutor's code name:
        {interlocutor_id}
        ## Interlocutor's Big Five personality traits scores:
        'Openness': {data['Openness']},
        'Conscientiousness': {data['Conscientiousness']},
        'Extraversion': {data['Extraversion']},
        'Agreeableness': {data['Agreeableness']},
        'Neuroticism': {data['Neuroticism']}

        For each trait:
        Explain what the score represents in terms of the interlocutor's behavior, tendencies, and characteristics.
        Use clear, concise, and empathetic language to paint a vivid picture of the person from a third-person perspective.
        Only provide the answer. Do not include any other information or introductory text in your response."""

        return llm_response(prompt)
    except Exception as e:
        print(f"Error processing row {row[0]}: {str(e)}")
        return None

def main():
    # 读取CSV文件
    with open('sampled_interlocutors.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)

        # 创建结果文件
        with open('personality_descriptions.csv', 'w', newline='', encoding='utf-8') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerow(['Interlocutor ID', 'Description'])

            for row in csv_reader:
                if len(row) < 2:  # 跳过空行或格式错误的行
                    continue

                description = generate_personality_description(row)
                if description:
                    data = ast.literal_eval(row[1])
                    csv_writer.writerow([data['interlocutor_id'], description])
                    print(f"Processed {data['interlocutor_id']} successfully")

if __name__ == "__main__":
    main()