import requests
import pandas as pd

# Configuration
API_KEY = '50a857aec1164241a3411b5e38e99982'
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

# Function to call LLM API
def llm_response(prompt):
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

# Load the CSV file
csv_file = 'adapted_dialogues_processed.csv'
# df = pd.read_csv(csv_file)
df = pd.read_csv(csv_file, skiprows=range(1001, 1045))

# Ensure the CSV has a 'Dialogue' column
if 'Dialogue' not in df.columns:
    raise ValueError("The CSV file must contain a 'Dialogue' column.")

# Create a new column 'Keyword' to store the results
df['Keyword'] = None

# Process each row and immediately update the CSV
for index, row in df.iterrows():
    dialogue = row['Dialogue']
    if pd.isna(dialogue) or dialogue.strip() == "":
        continue  # Skip empty dialogues

    # Create the prompt
    prompt = f"""
    I will now provide you with a Human-Computer Dialogue. Please help me summarize the user's intention in this dialogue into a few keywords. Your response should only contain the keywords without any other information.

    ##Dialogue:
    {dialogue}
    """

    # Call the LLM API
    result = llm_response(prompt)
    if result:
        # Update the current row's 'Keyword' column
        df.at[index, 'Keyword'] = result

        # Save the updated row to the CSV file immediately
        df.to_csv(csv_file, index=False)
        print(f"Processed and saved row {index + 1}.")
    else:
        print(f"Failed to process dialogue at index {index}.")

print("Processing complete. All results have been saved to the CSV file.")