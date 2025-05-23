import requests
import json
import csv
import re
import os

# Configuration
API_KEY = 'Your API Key'

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

    ENDPOINT = "Your Endpoint"

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


global_score_lists = []


def evaluate_dialogue(dialogue, additional_knowledge, human_human_dialogue, evaluators, api_url, first_speaker,
                      secondary_speaker, try_number=1):
    while True:
        feedback_list = []
        new_feedback_list = []
        score_list = []
        feedback_counter = 1

        for evaluator in evaluators:
            payload = {
                "model": evaluator,
                "prompt": f"""
            Now, I will give you a Human Human Dialogue. The content is as follows:  
            ## Human Human Dialogue:  
            {human_human_dialogue}

            And I will also provide you with {first_speaker}'s Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
            ## Personality traits score & Personality traits description:  
            {personality_traits}

            Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where {first_speaker} simulates the role of a Human (converting {first_speaker}'s utterances in the original Human Human Dialogue), and {secondary_speaker} simulates the role of a Computer (converting {secondary_speaker}'s utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.  
            ## Human Computer Dialogue:
            {human_computer_dialogue}

            The conversion of this Human Human Dialogue into Human Computer Dialogue is based on the following Additional Knowledge:  
            ## Additional Knowledge   
            {additional_knowledge}

            You will analyze two aspects of the Human Computer Dialogue converted from Human Human Dialogue:

            Task 1. Analyze whether this Human Computer Dialogue strictly follows the Additional Knowledge to transform the original Human Human Dialogue, you may need to refer {first_speaker}'s Personality Traits Score & Personality Traits Description.

            Task 2. Check whether the content and meaning of all utterances (from both Human Role and Computer Role) are preserved without alteration from the original Human Human Dialogue.

            Your output must only have two kinds:
            1. If you believe both of the tasks are complete. The final output is 'Task Completed'.
            2. If you think any task is incomplete, provide a single confidence score (0.0-1.0, 0.01 increments) reflecting the overall performance across both tasks, along with your feedback listing the specific deficiencies.
            The final output is: 'Feedback: [your detailed feedback], Score: [confidence score]'.

            **Important!!!** Your final output must not include any other text or information.
            """,
                "stream": False
            }

            headers = {"Content-Type": "application/json"}
            response = requests.post(api_url, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                if evaluator == 'deepseek-r1:8b':
                    response_data = response.json()['response']
                    think_end = response_data.find("</think>")
                    if think_end != -1:
                        response_data = response_data[think_end + len("</think>"):].strip()
                else:
                    response_data = response.json().get("response", "")
                if response_data.startswith("Feedback"):
                    feedback_score = response_data.split("Score:", 1)
                    if len(feedback_score) == 2:
                        feedback_part = feedback_score[0].strip()
                        score_part = feedback_score[1].strip()
                        feedback_list.append(feedback_part)
                        score_match = re.search(r'-?\d+\.?\d*', score_part)
                        if score_match:
                            score_part_cleaned = score_match.group(0)
                            score_list.append(float(score_part_cleaned))
                else:
                    score_list.append(1.0)
            else:
                print(f"Failed to fetch {evaluator} data. Status code: {response.status_code}")
                print("Response:", response.text)

        # average +1 std aggregation
        if score_list[0] >= 0.9183333333333333 and score_list[1] >= 0.8 and score_list[2] >= 0.8105:
            print(f'evaluation end. The confidence scores are {score_list}')
            return (dialogue,
                    try_number,
                    count_speaker_occurrences(human_human_dialogue, first_speaker),
                    count_speaker_occurrences(human_human_dialogue, secondary_speaker),
                    count_speaker_occurrences(dialogue, first_speaker),
                    count_speaker_occurrences(dialogue, secondary_speaker))

        else:
            for feedback in feedback_list:
                if feedback.startswith("Feedback"):
                    cleaned_response = feedback[len("Feedback:"):].strip()
                    formatted_feedback = f"Feedback {feedback_counter}:\n{cleaned_response}"
                    new_feedback_list.append(formatted_feedback)
                    feedback_counter += 1

            output_feedback = "\n\n".join(new_feedback_list)

            regenerate_prompt = f"""
            Now, I will give you a Human Human Dialogue. The content is as follows:
            ## Human Human Dialogue:
            {human_human_dialogue}
            Here, {first_speaker} and {secondary_speaker} are their respective designations. Now I will provide you with {first_speaker}'s Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
            ## Personality traits score & Personality traits description:  
            {personality_traits}
            Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where {first_speaker} simulates the role of a Human (converting {first_speaker}'s utterances in the original Human Human Dialogue), and {secondary_speaker} simulates the role of a Computer (converting {secondary_speaker}'s utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
            ## Human Computer Dialogue:
            {dialogue}
            The conversion of this Human Human Dialogue into Human Computer Dialogue is based on the following Additional Knowledge:
            ## Additional Knowledge
            {additional_knowledge}
            Now, I have received several different evaluators’ feedback regarding the issues with this transformed Human Computer Dialogue:
            {output_feedback}

            Your task is to revise this Human Computer Dialogue based on the feedback (you may need to refer to the original Human Human Dialogue, Personality traits score & Personality Traits Description and Additional Knowledge) and output a completely new Human Computer Dialogue. The output format should remain consistent with the original Human Computer Dialogue.

            **Important!!!** The newly generated Human Computer Dialogue must consider the content of each feedback simultaneously. Your response should only include the newly generated Human Computer Dialogue and no additional titles or information.
            """
            print(f'regenerate {try_number} times. The confidence scores are {score_list}.')
            try_number += 1
            dialogue = llm_response(regenerate_prompt)

            while True:
                if dialogue is None:
                    dialogue = llm_response(regenerate_prompt)
                    continue

                hhd_first_speaker_count = count_speaker_occurrences(human_human_dialogue, first_speaker)
                hhd_secondary_speaker_count = count_speaker_occurrences(human_human_dialogue, secondary_speaker)
                hcd_first_speaker_count = count_speaker_occurrences(dialogue, first_speaker)
                hcd_secondary_speaker_count = count_speaker_occurrences(dialogue, secondary_speaker)

                if hcd_first_speaker_count != hhd_first_speaker_count or hcd_secondary_speaker_count != hhd_secondary_speaker_count:
                    dialogue = None
                    continue
                break


def read_dialogues_from_csv(file_path):
    dialogues = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            if 3 <= i <= 12:
                dialogues.append(row['Dialogue'])
    return dialogues


def count_speaker_occurrences(dialogue, speaker):
    return dialogue.count(f"{speaker}:")


# Example usage
if __name__ == "__main__":

    csv_file_path = '../sampled_HHDs/A_High_CC_example_dialogues.csv'

    output_csv_path = 'data/average_-1_std_aggregation_output_adapted_dialogues/A_High_CC_HCD.csv'

    human_human_dialogues = read_dialogues_from_csv(csv_file_path)

    file_exists = os.path.exists(output_csv_path) and os.path.getsize(output_csv_path) > 0

    # 打开CSV文件准备写入
    with open(output_csv_path, mode='a', newline='', encoding='utf-8') as output_file:
        fieldnames = ['Index', 'Dialogue', 'Try_Number', 'hhd_fs_count', 'hhd_ss_count', 'hcd_fs_count', 'hcd_ss_count']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        # Initialize an index counter
        index = 1

        for human_human_dialogue in human_human_dialogues:

            # Regex to capture everything before the first colon
            match_first_speaker = re.match(r'(\w+):', human_human_dialogue)

            if match_first_speaker:
                first_speaker = match_first_speaker.group(1)
                print("First speaker's identifier:", first_speaker)
            else:
                print("No match found.")

            # Regex to capture the speaker after the first 'BJ:'
            match_second_speaker = re.search(r'(?<=\s)(\w+):', human_human_dialogue)

            if match_second_speaker:
                secondary_speaker = match_second_speaker.group(1)
                print("Secondary speaker's identifier:", secondary_speaker)
            else:
                print("No secondary speaker found.")

            personality_traits = """
            Openness: 6.25
            CC is highly open to new experiences and values creativity and innovation. He/she enjoys exploring new ideas, learning new things, and is often curious about the world. This openness makes him/her adaptable and imaginative.
            Conscientiousness: 3.0
            CC has a moderate level of conscientiousness. He/she may not be particularly focused on organization or detailed planning, but can still complete tasks and meet responsibilities. His/her approach may be more flexible and spontaneous rather than strictly disciplined.
            Extraversion: 3.3333332538604736
            CC has a balanced level of extraversion. He/she enjoys social interactions and can be outgoing and energetic in social situations, but also values and needs some time alone to recharge. This balance allows him/her to be adaptable in both social and solitary settings.
            Agreeableness: 5.333333492279053
            CC is quite agreeable, displaying warmth, kindness, and a cooperative nature. He/she is likely to be empathetic and considerate towards others, valuing harmonious relationships and often putting others' needs before his/her own.
            Neuroticism: 3.0833332538604736
            CC has a relatively average level of neuroticism. He/she may experience occasional stress or emotional fluctuations, but generally manages to maintain a balanced emotional state. This level allows him/her to be resilient in most situations without being overly affected by negative emotions.
            """

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

            dialogue_transformation_prompt = f"""
            Now I will provide you with a Human Human Dialogue as follows:  
            ## Human Human Dialogue:  
            {human_human_dialogue}
            Here, {first_speaker} and {secondary_speaker} are their respective designations. Now I will provide you with {first_speaker}'s Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
            ## Personality traits score & Personality traits description:  
            {personality_traits}
            Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
            ## Additional Knowledge:  
            {additional_knowledge}
            Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with {first_speaker} playing the role of the Human and {secondary_speaker} playing the role of the Computer. Specifically, you need to transform {first_speaker}'s utterances based on {first_speaker}'s Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform {secondary_speaker}'s utterances into a Computer style, also without altering the content and meaning.  

            **Important!!!** Your final output format must strictly follow the format of the provided Human-Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
            """

            human_computer_dialogue = llm_response(dialogue_transformation_prompt)

            while True:
                if human_computer_dialogue is None:
                    human_computer_dialogue = llm_response(dialogue_transformation_prompt)
                    continue

                hhd_first_speaker_count = count_speaker_occurrences(human_human_dialogue, first_speaker)
                hhd_secondary_speaker_count = count_speaker_occurrences(human_human_dialogue, secondary_speaker)
                hcd_first_speaker_count = count_speaker_occurrences(human_computer_dialogue, first_speaker)
                hcd_secondary_speaker_count = count_speaker_occurrences(human_computer_dialogue, secondary_speaker)

                if hcd_first_speaker_count != hhd_first_speaker_count or hcd_secondary_speaker_count != hhd_secondary_speaker_count:
                    human_computer_dialogue = None
                    continue

                break

            # Evaluators and API URL
            evaluators = ["deepseek-r1:8b", "llama3.1:8b", "gemma2:9b"]
            api_url = "http://127.0.0.1:11434/api/generate"

            # Get final Human-Computer Dialogue
            final_dialogue, try_number, hhd_fs_count, hhd_ss_count, hcd_fs_count, hcd_ss_count = evaluate_dialogue(
                human_computer_dialogue, additional_knowledge, human_human_dialogue, evaluators,
                api_url, first_speaker, secondary_speaker)

            # Write the row with the index
            writer.writerow(
                {'Index': index, 'Dialogue': final_dialogue, 'Try_Number': try_number, 'hhd_fs_count': hhd_fs_count,
                 'hhd_ss_count': hhd_ss_count, 'hcd_fs_count': hcd_fs_count, 'hcd_ss_count': hcd_ss_count})

            # Flush the buffer to ensure data is written to the file immediately
            output_file.flush()

            # Increment the index
            index += 1