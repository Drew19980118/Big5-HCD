import requests
import json
import csv
import numpy as np

# File paths for the two CSVs
human_human_csv = '../sampled_HHDs/C_High_BE_example_dialogues.csv'
human_computer_csv = '../role_model_HCDs/C_High_BE_role_model_synthetized_HCD.csv'
deepseek_output_file = 'deepseek_evaluation_results/C_High_BE.txt'
llama3_output_file = 'llama3_evaluation_results/C_High_BE.txt'
gemma2_output_file = 'gemma2_evaluation_results/C_High_BE.txt'

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
Openness: 4.5
BE is moderately open to new experiences. He/She enjoys trying new things and exploring different ideas, but also appreciates some level of routine and familiarity. He/She is curious and imaginative, often seeking intellectual or artistic pursuits, yet maintains a balanced approach without being overly adventurous or unconventional.
Conscientiousness: 5.17
BE is quite conscientious, indicating a strong sense of responsibility and reliability. He/She is well-organized, diligent, and typically ensures that tasks are completed with care and efficiency. BE is goal-oriented and can be depended upon to follow through on commitments, although he/she allows for some flexibility when necessary.
Extraversion: 4.83
BE is fairly extroverted, enjoying social interactions and feeling energized by being around others. He/She is outgoing, talkative, and often seeks out social settings. BE can comfortably engage with new people and tends to have a positive and enthusiastic demeanor in group settings.
Agreeableness: 4.83
BE is generally agreeable, showing a high level of empathy and cooperation in his/her interactions. He/She is considerate, kind, and tends to prioritize harmonious relationships. BE values getting along with others and is likely to be seen as warm and compassionate, often seeking to resolve conflicts amicably.
Neuroticism: 4.25
BE has a moderate level of neuroticism, indicating that he/she experiences emotions fairly intensely but can usually manage them effectively. He/She might sometimes feel anxious, stressed, or moody, but overall, he/she has a reasonable level of emotional stability. BE is self-aware and can recognize and address his/her emotional responses when needed.
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

And I will also provide you with BE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
## Personality traits score & Personality traits description:  
{personality_traits}

Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where BE simulates the role of a Human (converting BE's utterances in the original Human Human Dialogue), and AQ simulates the role of a Computer (converting AQ's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.  
## Human Computer Dialogue:
{human_computer_dialogue}

The conversion of this Human Human Dialogue into Human Computer Dialogue is based on the following Additional Knowledge:  
## Additional Knowledge   
{additional_knowledge}

You will analyze two aspects of the Human Computer Dialogue converted from Human Human Dialogue:

Task 1. Analyze whether this Human Computer Dialogue strictly follows the Additional Knowledge to transform the original Human Human Dialogue, you may need to refer BE's Personality Traits Score & Personality Traits Description.

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

And I will also provide you with BE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
## Personality traits score & Personality traits description:  
{personality_traits}

Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where BE simulates the role of a Human (converting BE's utterances in the original Human Human Dialogue), and AQ simulates the role of a Computer (converting AQ's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.  
## Human Computer Dialogue:
{human_computer_dialogue}

The conversion of this Human Human Dialogue into Human Computer Dialogue is based on the following Additional Knowledge:  
## Additional Knowledge   
{additional_knowledge}

You will analyze two aspects of the Human Computer Dialogue converted from Human Human Dialogue:

Task 1. Analyze whether this Human Computer Dialogue strictly follows the Additional Knowledge to transform the original Human Human Dialogue, you may need to refer BE's Personality Traits Score & Personality Traits Description.

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