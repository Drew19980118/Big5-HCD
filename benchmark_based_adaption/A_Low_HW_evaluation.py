import requests
import json
import csv
import re

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


global_score_lists = []


def evaluate_dialogue(dialogue, additional_knowledge, human_human_dialogue, evaluators, api_url, first_speaker, secondary_speaker, try_number=1):
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
            Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where {first_speaker} simulates the role of a Human (converting {first_speaker}'s utterances in the original Human Human Dialogue), and {secondary_speaker} simulates the role of a Computer (converting {secondary_speaker}'s utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.  
            ## Human Computer Dialogue:
            {human_computer_dialogue}

            The conversion of this Human Human Dialogue into Human Computer Dialogue is based on the following Additional Knowledge:  
            ## Additional Knowledge   
            {additional_knowledge}

            You will analyze two aspects of the Human Computer Dialogue converted from Human Human Dialogue:

            Task 1. Analyze whether this Human Computer Dialogue strictly follows the Additional Knowledge to transform the original Human Human Dialogue.

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
                        score_list.append(float(score_part))
                else:
                    score_list.append(1.0)
            else:
                print(f"Failed to fetch {evaluator} data. Status code: {response.status_code}")
                print("Response:", response.text)

        if score_list[0] >= 0.9674999999999999 and score_list[1] >= 0.7738333333333334 and score_list[2] >= 0.769:
            print(f'evaluation end. The confidence scores are {score_list}')
            return dialogue, try_number
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
            while dialogue is None:
                print('Need to regenerate dialogue!')
                dialogue = llm_response(regenerate_prompt)

def read_dialogues_from_csv(file_path):
    dialogues = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            if 3 <= i <= 10:
                dialogues.append(row['Dialogue'])
    return dialogues

# Example usage
if __name__ == "__main__":

    csv_file_path = '../test_interlocutor_dialogues/A_Low_HW_example_dialogues.csv'

    output_csv_path = 'output_adapted_dialogues/A_Low_HW_HCD.csv'

    human_human_dialogues = read_dialogues_from_csv(csv_file_path)

    # 打开CSV文件准备写入
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as output_file:
        fieldnames = ['Index', 'Dialogue', 'Try_Number']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
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
            'Openness': 2.0
            HW tend to prefer routine and familiarity over novelty and variety. HW might not be very open to new experiences or unconventional ideas. This preference for the tried-and-true can make HW dependable and practical, but HW may sometimes struggle with adapting to change or thinking creatively. In relationships, HW might appreciate stability and clear boundaries. At work, HW likely excel in structured environments but may need encouragement to embrace innovation.
            'Conscientiousness': 1.0
            HW might find it challenging to stick to schedules and maintain organization. Spontaneity and flexibility could be more HW style, but this can sometimes lead to difficulties in meeting deadlines and achieving long-term goals. In relationships, HW relaxed approach can make HW easygoing and fun, but it may also frustrate more organized partners. At work, HW might thrive in roles that require adaptability rather than rigid planning.
            'Extraversion': 1.0
            HW are likely introverted and prefer solitary activities or spending time with a small, close-knit group of friends. Social interactions can be draining, and HW might need ample alone time to recharge. In relationships, HW value deep, meaningful connections over a large social circle. At work, HW might excel in tasks that require focus and independence, but collaborative projects may be more challenging for HW.
            'Agreeableness': 1.0
            HW might have a more competitive or skeptical nature and are less inclined to prioritize harmony over personal beliefs or goals. This trait can make HW strong-willed and decisive, but it might lead to conflicts or difficulties in compromising. In relationships, HW might be seen as assertive or blunt, which can sometimes cause friction. In a work setting, HW likely excel in roles that require critical thinking and decisiveness, though teamwork could be challenging.
            'Neuroticism': 7.0
            HW may experience high levels of emotional sensitivity and stress. Anxiety, worry, and mood swings could be common for HW. This heightened emotional response can make relationships challenging, as HW might be perceived as high-maintenance or easily upset. In HW professional life, managing stress and maintaining a calm demeanor might be difficult, potentially affecting HW performance. Finding effective coping strategies and supportive environments could be crucial for HW well-being.
            """

            additional_knowledge = """
            Differences Between Human Human Dialogue (HHD) and Human Computer Dialogue (HCD):

            Communication Styles:

            HCD: Interactions between humans and machines are characterized by brief, frequent exchanges that prioritize efficiency. Users expect clear, straightforward responses without unnecessary elaboration.
            Example: User: "What time is my next meeting?" System: "Your meeting starts at 2:00 PM in Conference Room B."

            HHD: Conversations between humans are more nuanced and context-rich, often incorporating additional details, shared thoughts, or collaborative reasoning.
            Example: Person A: "The weather app says it’ll stay clear, but the sky looks a bit hazy. Do you think we should leave earlier for the hike?" Person B: "Good point—maybe we can avoid the afternoon crowd too. Let’s aim for 8 AM instead!"

            Relational and Personality Expression:

            HCD: Interactions between humans and machines are transactional and lack emotional depth or personal connection, as machines are incapable of genuine empathy or emotional understanding.
            Example: User: "I’m overwhelmed with work deadlines." System: "Would you like me to schedule a reminder for your tasks?"

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

            while human_computer_dialogue is None:
                print('Need to regenerate initial dialogue!')
                human_computer_dialogue = llm_response(dialogue_transformation_prompt)

            # Evaluators and API URL
            evaluators = ["deepseek-r1:8b", "llama3.1:8b", "gemma2:9b"]
            api_url = "http://127.0.0.1:11434/api/generate"

            # Get final Human-Computer Dialogue
            final_dialogue, try_number = evaluate_dialogue(human_computer_dialogue, additional_knowledge, human_human_dialogue, evaluators,
                                       api_url, first_speaker, secondary_speaker)

            # Write the row with the index
            writer.writerow({'Index': index, 'Dialogue': final_dialogue, 'Try_Number': try_number})

            # Flush the buffer to ensure data is written to the file immediately
            output_file.flush()

            # Increment the index
            index += 1