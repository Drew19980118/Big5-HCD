import requests
import json
import csv
import numpy as np

# File paths for the two CSVs
human_human_csv = '../sampled_HHDs/N_Low_EA_example_dialogues.csv'
human_computer_csv = '../role_model_HCDs_construction/N_Low_EA_role_model_synthetized_HCD.csv'
deepseek_output_file = 'deepseek_evaluation_results/N_Low_EA.txt'
llama3_output_file = 'llama3_evaluation_results/N_Low_EA.txt'
gemma2_output_file = 'gemma2_evaluation_results/N_Low_EA.txt'

api_url = "http://127.0.0.1:11434/api/generate"
headers = {"Content-Type": "application/json"}

additional_knowledge = """
Differences Between Human Human Dialogue (HHD) and Human Computer Dialogue (HCD):

Communication Styles:

HCD: Interactions between humans and machines are characterized by brief, frequent exchanges that prioritize efficiency. Humans expect clear, straightforward responses without unnecessary elaboration.
Example: Human: "What time is my next meeting?" System: "Your meeting starts at 2:00 PM in Conference Room B."

HHD: Interactions between humans are more nuanced and context-rich, often incorporating additional details, shared thoughts, or collaborative reasoning.
Example: Person A: "The weather app says it’ll stay clear, but the sky looks a bit hazy. Do you think we should leave earlier for the hike?" Person B: "Good point—maybe we can avoid the afternoon crowd too. Let’s aim for 8 AM instead!"

Relational and Personality Expression:

HCD: Interactions between humans and machines are transactional and lack emotional depth or personal connection, as machines are incapable of genuine empathy or emotional understanding.
Example: Human: "I’m overwhelmed with work deadlines." System: "Would you like me to schedule a reminder for your tasks?"

HHD: Human interactions are infused with emotional expression, humor, and openness, fostering trust and mutual understanding. These exchanges often include empathy, support, and shared problem-solving.
Example: Person A: "I’ve been swamped with deadlines all week—it’s exhausting." Person B: "That sounds rough. Want to grab coffee later? We can brainstorm ways to tackle it together."
"""

personality_traits = """
Openness: 4.833333492279053
EA is quite open to new experiences and ideas. His/her imagination and curiosity drive him/her to explore new concepts and embrace unconventional perspectives. This score indicates a balanced appreciation for both novel and traditional elements, suggesting EA is adaptable and willing to consider different viewpoints.
Conscientiousness: 3.8333332538604736
EA has a moderate level of conscientiousness, reflecting a tendency to be responsible and organized, but also allowing for some flexibility and spontaneity. He/she likely plans ahead and strives for efficiency in his/her endeavors, but isn’t overly rigid in his/her approach.
Extraversion: 3.8333332538604736
EA enjoys social interactions and draws energy from engaging with others, but is also comfortable spending time alone. He/she has a balanced approach to socializing, enjoying the company of friends and family without needing constant interaction to feel fulfilled.
Agreeableness: 4.166666507720947
EA tends to be cooperative, compassionate, and friendly. He/she is likely to be considerate of others' feelings and strives to maintain harmony in his/her relationships. This score indicates a strong preference for positive social interactions and a willingness to put others' needs alongside or occasionally ahead of his/her own.
Neuroticism: 3.3333332538604736
EA experiences a moderate level of emotional reactivity. He/she may sometimes feel anxious or stressed, but generally manages to cope well with life's challenges. This score suggests that while EA might occasionally experience emotional ups and downs, he/she has a fairly stable and resilient disposition.
"""

def read_csv(file_path):
    dialogues = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            dialogues.append(row[1])  # Assuming Dialogue is in the second column
    return dialogues

def deepseek_evaluate_dialogue(human_human_dialogue, human_computer_dialogue):
    payload = {
        "model": "deepseek-r1:8b",
        "prompt": f"""
Now, I will give you a Human Human Dialogue. The content is as follows:  
## Human Human Dialogue:  
{human_human_dialogue}

And I will also provide you with EA's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
## Personality traits score & Personality traits description:  
{personality_traits}

Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where EA simulates the role of a Human (converting EA's utterances in the original Human Human Dialogue), and CP simulates the role of a Computer (converting CP's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.  
## Human Computer Dialogue:
{human_computer_dialogue}

The conversion of this Human Human Dialogue into Human Computer Dialogue is based on the following Additional Knowledge:  
## Additional Knowledge   
{additional_knowledge}

You will analyze two aspects of the Human Computer Dialogue converted from Human Human Dialogue:

Task 1. Analyze whether this Human Computer Dialogue strictly follows the Additional Knowledge to transform the original Human Human Dialogue, you may need to refer EA's Personality Traits Score & Personality Traits Description.

Task 2. Check whether the content and meaning of all utterances (from both Human Role and Computer Role) are preserved without alteration from the original Human Human Dialogue.

Your output must only have two kinds:
1. If you believe both of the tasks are complete. The final output is 'Task Completed'.
2. If you think any task is incomplete, provide a single confidence score (0.0-1.0, 0.01 increments) reflecting the overall performance across both tasks.
The final output is: 'Score: [confidence score]'.

**Important!!!** Your final output must not include any other text or information.
""",
        "stream": False
    }
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        response_data = response.json()['response']
        think_end = response_data.find("</think>")
        if think_end != -1:
            response_data = response_data[think_end + len("</think>"):].strip()
        if response_data.startswith('Score:'):
            return float(response_data.split(': ')[1])
        else:
            return 1.0

def llama3_gemma2_evaluate_dialogue(human_human_dialogue, human_computer_dialogue):
    payload = {
        "model": "llama3.1:8b",
        "prompt": f"""
Now, I will give you a Human Human Dialogue. The content is as follows:  
## Human Human Dialogue:  
{human_human_dialogue}

And I will also provide you with EA's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
## Personality traits score & Personality traits description:  
{personality_traits}

Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where EA simulates the role of a Human (converting EA's utterances in the original Human Human Dialogue), and CP simulates the role of a Computer (converting CP's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.  
## Human Computer Dialogue:
{human_computer_dialogue}

The conversion of this Human Human Dialogue into Human Computer Dialogue is based on the following Additional Knowledge:  
## Additional Knowledge   
{additional_knowledge}

You will analyze two aspects of the Human Computer Dialogue converted from Human Human Dialogue:

Task 1. Analyze whether this Human Computer Dialogue strictly follows the Additional Knowledge to transform the original Human Human Dialogue, you may need to refer EA's Personality Traits Score & Personality Traits Description.

Task 2. Check whether the content and meaning of all utterances (from both Human Role and Computer Role) are preserved without alteration from the original Human Human Dialogue.

Your output must only have two kinds:
1. If you believe both of the tasks are complete. The final output is 'Task Completed'.
2. If you think any task is incomplete, provide a single confidence score (0.0-1.0, 0.01 increments) reflecting the overall performance across both tasks.
The final output is: 'Score: [confidence score]'.

**Important!!!** Your final output must not include any other text or information.
""",
        "stream": False
    }
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        response_data = response.json().get("response", "")
        if response_data.startswith('Score:'):
            return float(response_data.split(': ')[1])
        else:
            return 1.0

# Read dialogues from CSVs
human_human_dialogues = read_csv(human_human_csv)
human_computer_dialogues = read_csv(human_computer_csv)

# Store median scores for each dialogue pair
deepseek_median_scores = []
llama3_median_scores = []
gemma2_median_scores = []

# Open file for writing results
with open(deepseek_output_file, 'w') as file:
    # Iterate over each pair of dialogues
    for index, (hh_dialogue, hc_dialogue) in enumerate(zip(human_human_dialogues, human_computer_dialogues), start=1):
        scores = []

        print(f"\nDeepSeek - Processing Dialogue Pair {index}")
        file.write(f"\nProcessing Dialogue Pair {index}\n")

        # Perform 50 evaluations
        for i in range(50):
            score = deepseek_evaluate_dialogue(hh_dialogue, hc_dialogue)
            if score is not None:
                scores.append(score)
                print(f"DeepSeek - Evaluation {i + 1}: Score = {score}")
                file.write(f"  Evaluation {i + 1}: Score = {score}\n")

        # Calculate median for the 50 scores
        if scores:
            median_score = np.median(scores)
            deepseek_median_scores.append(median_score)
            print(f"DeepSeek - Median Score for Dialogue Pair {index}: {median_score}")
            file.write(f"  Median Score for Dialogue Pair {index}: {median_score}\n")

    # Calculate the final median of medians
    if deepseek_median_scores:
        final_score = np.median(deepseek_median_scores)
        print(f"\nDeepSeek - Final Score (Median of Medians): {final_score}")
        file.write(f"\nFinal Score (Median of Medians): {final_score}\n")
    else:
        print("DeepSeek - No valid scores obtained.")
        file.write("No valid scores obtained.\n")

# Open file for writing results
with open(llama3_output_file, 'w') as file:
    # Iterate over each pair of dialogues
    for index, (hh_dialogue, hc_dialogue) in enumerate(zip(human_human_dialogues, human_computer_dialogues), start=1):
        scores = []

        print(f"\nLlama 3 - Processing Dialogue Pair {index}")
        file.write(f"\nProcessing Dialogue Pair {index}\n")

        # Perform 50 evaluations
        for i in range(50):
            score = llama3_gemma2_evaluate_dialogue(hh_dialogue, hc_dialogue)
            if score is not None:
                scores.append(score)
                print(f"Llama 3 - Evaluation {i + 1}: Score = {score}")
                file.write(f"  Evaluation {i + 1}: Score = {score}\n")

        # Calculate median for the 50 scores
        if scores:
            median_score = np.median(scores)
            llama3_median_scores.append(median_score)
            print(f"Llama 3 - Median Score for Dialogue Pair {index}: {median_score}")
            file.write(f"  Median Score for Dialogue Pair {index}: {median_score}\n")

    # Calculate the final median of medians
    if llama3_median_scores:
        final_score = np.median(llama3_median_scores)
        print(f"\nLlama 3 - Final Score (Median of Medians): {final_score}")
        file.write(f"\nFinal Score (Median of Medians): {final_score}\n")
    else:
        print("Llama 3 - No valid scores obtained.")
        file.write("No valid scores obtained.\n")

# Open file for writing results
with open(gemma2_output_file, 'w') as file:
    # Iterate over each pair of dialogues
    for index, (hh_dialogue, hc_dialogue) in enumerate(zip(human_human_dialogues, human_computer_dialogues), start=1):
        scores = []

        print(f"\nGemma 2 - Processing Dialogue Pair {index}")
        file.write(f"\nProcessing Dialogue Pair {index}\n")

        # Perform 50 evaluations
        for i in range(50):
            score = llama3_gemma2_evaluate_dialogue(hh_dialogue, hc_dialogue)
            if score is not None:
                scores.append(score)
                print(f"Gemma 2 - Evaluation {i + 1}: Score = {score}")
                file.write(f"  Evaluation {i + 1}: Score = {score}\n")

        # Calculate median for the 50 scores
        if scores:
            median_score = np.median(scores)
            gemma2_median_scores.append(median_score)
            print(f"Gemma 2 - Median Score for Dialogue Pair {index}: {median_score}")
            file.write(f"  Median Score for Dialogue Pair {index}: {median_score}\n")

    # Calculate the final median of medians
    if gemma2_median_scores:
        final_score = np.median(gemma2_median_scores)
        print(f"\nGemma 2 - Final Score (Median of Medians): {final_score}")
        file.write(f"\nFinal Score (Median of Medians): {final_score}\n")
    else:
        print("Gemma 2 - No valid scores obtained.")
        file.write("No valid scores obtained.\n")