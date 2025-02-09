import requests
import json

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

def evaluate_dialogue(dialogue, additional_knowledge, human_human_dialogue, evaluators, api_url, try_number = 1):
    while True:
        feedback_list = []
        new_feedback_list = []
        score_list = []
        feedback_counter = 1

        for evaluator in evaluators:
            payload = {
                "model": evaluator,
                "prompt": f"""
Now, I will give you a Human-Human Dialogue. The content is as follows:  
## Human-Human Dialogue:  
{human_human_dialogue}
Then, I will give you a Human-Computer Dialogue based on this Human-Human Dialogue, where AH simulates the role of a Human (converting AH's utterances in the original Human-Human Dialogue), and AQ simulates the role of a Computer (converting AQ's utterances in the original Human-Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.  
## Human-Computer Dialogue:
{dialogue}

The conversion of this Human-Human Dialogue into Human-Computer Dialogue is based on the following Additional Knowledge:  
## Additional Knowledge   
{additional_knowledge}
Now, your task is to analyze whether this Human Computer Dialogue strictly follows the Additional Knowledge to transform the original Human Human Dialogue.

Your output must only have two kinds:
1. If you believe the task is complete. The final output is 'Task Completed'.
2. If you think the task is incomplete, provide a confidence score (ranging from 0 to 1) indicating the extent to which you believe the Human-Computer Dialogue strictly follows the Additional Knowledge to transform the original Human-Human Dialogue, along with your feedback.
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

        # if not feedback_list or all(score >= 0.8 for score in score_list):
        #     if len(feedback_list) == 0:
        #         print("All evaluators fully agree. Final Human-Computer Dialogue is ready.")
        #     else:
        #         print(f"All evaluators partly agree. Partly agreed confidence scores are {score_list}. Final Human-Computer Dialogue is ready.")
        #     return dialogue

        average_score = sum(score_list) / len(score_list) if score_list else 0
        if not feedback_list or average_score >= 0.8:
            if len(feedback_list) == 0:
                print("All evaluators fully agree. Final Human-Computer Dialogue is ready.")
            else:
                print(f"All evaluators partly agree. Average confidence scores are {average_score}. Final Human-Computer Dialogue is ready.")
            return dialogue

        else:
            for feedback in feedback_list:
                if feedback.startswith("Feedback"):
                    cleaned_response = feedback[len("Feedback:"):].strip()
                    formatted_feedback = f"Feedback {feedback_counter}:\n{cleaned_response}"
                    new_feedback_list.append(formatted_feedback)
                    feedback_counter += 1

            output_feedback = "\n\n".join(new_feedback_list)

        regenerate_prompt = f"""
Now, I will give you a Human-Human Dialogue. The content is as follows:
## Human-Human Dialogue:
{human_human_dialogue}
Here, AH and AQ are their respective designations. Now I will provide you with AH's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
## Personality traits score & Personality traits description:  
{personality_traits}
Then, I will give you a Human-Computer Dialogue based on this Human-Human Dialogue, where AH simulates the role of a Human (converting AH's utterances in the original Human-Human Dialogue), and AQ simulates the role of a Computer (converting AQ's utterances in the original Human-Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
## Human-Computer Dialogue:
{dialogue}
The conversion of this Human-Human Dialogue into Human-Computer Dialogue is based on the following Additional Knowledge:
## Additional Knowledge
{additional_knowledge}
Now, I have received several different evaluators’ feedback regarding the issues with this transformed Human Computer Dialogue:
{output_feedback}

Your task is to revise this Human Computer Dialogue based on the feedback (you may need to refer to the original Human Human Dialogue, Personality traits score & Personality traits description and Additional Knowledge) and output a completely new Human-Computer Dialogue. The output format should remain consistent with the original Human-Computer Dialogue.

**Important!!!** The newly generated Human Computer Dialogue must consider the content of each feedback simultaneously. Your response should only include the newly generated Human Computer Dialogue and no additional titles or information.
"""
        print(f'regenerate {try_number} times. The confidence scores are {score_list}.')
        try_number += 1
        dialogue = llm_response(regenerate_prompt)
        while dialogue is None:
            print('Need to regenerate dialogue!')
            dialogue = llm_response(regenerate_prompt)

# Example usage
if __name__ == "__main__":
    human_human_dialogue = """
    AH: Hello! 
    AQ: Hello. 
    AH: Do you eat breakfast? 
    AQ: I will eat. 
    AH: Could you tell me what kind of menu it is? 
    AQ: Most of the time, it's plain white rice with natto. 
    AH: Natto rice is easy to make and delicious, isn't it! 
    AQ: That's right. Sometimes I even put in raw eggs. 
    AH: Raw eggs, natto, and rice seem to be a great match! 
    AQ: "It's delicious. Can you eat natto?" 
    AH: Yes, I eat it every night. 
    AQ: That is wonderful. 
    AH: It seems to be good for health. 
    AQ: Oh, by the way, it seems that this is the number one food recommended by doctors. 
    AH: It was so good that even the doctor recommended it. 
    AQ: "It seems so. They said it on the news." 
    AH: I didn't think it was that good. 
    AQ: Yeah, yeah. They say it also affects lifespan. 
    AH: Fermented foods are said to be good for your health. 
    AQ: In short, that's what it means. 
    AH: I think the person who ate it first is amazing. 
    AQ: "That's certainly true." 
    AH: If there are rotten items, I will throw them away. 
    AQ: Certainly. Something so slimy. 
    AH: I also think that the person who came up with that sauce made a great invention. 
    AQ: Got it! I like that thing. Something with natto and a raw egg. 
    AH: I also love that sauce! 
    AQ: Did you understand? Good. 
    AH: Yes, I never thought that there would be other people who think the same thing. 
    AQ: Hahaha. Let's talk again.
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
    Differences Between Human Human Dialogue (HHD) and Human Computer Dialogue (HCD):
    Communication Styles:
    HCD: Interactions between humans and machines are characterized by brief, frequent exchanges that prioritize efficiency. Users expect clear, straightforward responses without unnecessary elaboration.
    Example: "It’s 72°F and sunny."
    HHD: Conversations between humans are more nuanced and context-rich, often incorporating additional details, shared thoughts, or collaborative reasoning.
    Example: "It’s 72°F and sunny, but should we bring an umbrella later?"
    Relational and Personality Expression:
    HCD: Interactions between humans and machines are transactional and lack emotional depth or personal connection, as machines are incapable of genuine empathy or emotional understanding.
    Example: When a user expresses stress, a machine might respond neutrally, e.g., "I'm here to help."
    HHD: Human interactions are infused with emotional expression, humor, and openness, fostering trust and mutual understanding. These exchanges often include empathy, support, and shared problem-solving.
    Example: A friend might respond empathetically, e.g., "I understand how you feel. Let’s figure this out together."
    """

    dialogue_transformation_prompt = f"""
    Now I will provide you with a Human-Human Dialogue as follows:  
    ## Human-Human Dialogue:  
    {human_human_dialogue}
    Here, AH and AQ are their respective designations. Now I will provide you with AH's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human-Human Dialogue and Human-Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human-Human Dialogue into a Human-Computer Dialogue, with AH playing the role of the Human and AQ playing the role of the Computer. Specifically, you need to transform AH's utterances based on AH's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AQ's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human-Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    # First transformation
    human_computer_dialogue = llm_response(dialogue_transformation_prompt)

    if human_computer_dialogue is None:
        print('unexpected error')
        exit(1)

        # Evaluators and API URL
    evaluators = ["deepseek-r1:8b", "llama3.1:8b", "gemma2:9b"]
    api_url = "http://127.0.0.1:11434/api/generate"

    # Get final Human-Computer Dialogue
    final_dialogue = evaluate_dialogue(human_computer_dialogue, additional_knowledge, human_human_dialogue, evaluators, api_url)
    print(final_dialogue)