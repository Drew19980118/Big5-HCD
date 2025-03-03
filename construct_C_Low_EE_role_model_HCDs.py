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

def evaluate_dialogue(human_human_dialogue, human_computer_dialogue, personality_traits, additional_knowledge, human_feedback):

        regenerate_prompt = f"""
        Now, I will give you a Human Human Dialogue. The content is as follows:
        ## Human Human Dialogue:
        {human_human_dialogue}
        Here, EE and BL are their respective designations. Now I will provide you with EE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where EE simulates the role of a Human (converting EE's utterances in the original Human Human Dialogue), and BL simulates the role of a Computer (converting BL's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
        ## Human Computer Dialogue:
        {human_computer_dialogue}
        The conversion of this Human Human Dialogue into Human Computer Dialogue is based on the following Additional Knowledge:
        ## Additional Knowledge
        {additional_knowledge}
        Now, I have received several different evaluators’ feedback regarding the issues with this transformed Human Computer Dialogue:
        {human_feedback}

        Your task is to revise this Human Computer Dialogue based on the feedback (you may need to refer to the original Human Human Dialogue, Personality traits score & Personality Traits Description and Additional Knowledge) and output a completely new Human Computer Dialogue. The output format should remain consistent with the original Human Computer Dialogue.

        **Important!!!** The newly generated Human Computer Dialogue must consider the content of each feedback simultaneously. Your response should only include the newly generated Human Computer Dialogue and no additional titles or information.
        """

        return llm_response(regenerate_prompt)

def count_ct_occurrences(dialogue):
    return dialogue.count("EE:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    EE: Hello, nice to meet you. 
    BL: Hello. Nice to meet you. 
    EE: What do you do on your days off? 
    BL: Looking at your smartphone, going shopping, and studying. 
    EE: I am similar. What do you often do on your smartphone? 
    BL: There is a lot of research to do. 
    EE: I see. Don't you play games or anything? 
    BL: I hardly play games. 
    EE: I see. I often read manga on my smartphone. 
    BL: Do you have any manga apps installed? 
    EE: Putting it in. 
    BL: "Manga also often comes through advertisements, doesn't it?" 
    EE: Jumping from interesting ads, I end up adding more and more apps. 
    BL: Is your smartphone's storage capacity okay? 
    EE: Since I am using an Android, I can increase the storage capacity with an SD card. BL: "Can apps also be stored on the SD card?" 
    EE: Mainly, I store photo data. 
    BL: I am also including the photos. 
    EE: Are you using an Android? 
    BL: I have both an android and an iPhone. 
    EE: It is the same!! 
    BL: How do you differentiate between them? 
    EE: Mainly use Android and only take out the iPhone when I need to use it. 
    BL: I see. 
    EE: How do you differentiate between using <BL>? 
    BL: "It's for calling and communication." 
    EE: I see! I also often use my iPhone for calls. 
    BL: I'm the opposite. I use an Android for calls. 
    EE: I see. 
    BL: "It's convenient to use them differently, isn't it?"
    """

    sample_2_human_human_dialogue = """
    EE: Hello 
    BL: Hello. 
    EE: What is your favorite household chore? 
    BL: "If I had to say, maybe hanging out the laundry?" 
    EE: I understand! I don't know why, but it's fun, isn't it? 
    BL: It feels refreshing to hang out things that have become clean. 
    EE: I see, that is certainly true. The laundry hung out after smoothing out the wrinkles looks very good. 
    BL: On the other hand, if you leave it in the washing machine for a long time, it feels unfortunate. 
    EE: If you forget about it, it will start to smell like it's only half dry. 
    BL: The smell is one thing, but it also easily wrinkles. 
    EE: Certainly. I make sure to iron clothes just before hanging them up to dry. 
    BL: "It's fully automatic, right? Are you intentionally stopping it?" 
    EE: "I set the dehydration to 0 minutes and run it on the course up to rinsing." 
    BL: I see. Our washing machine doesn't have that function. That's nice. 
    EE: Items that easily wrinkle are convenient because the dehydration time can be shortened. 
    BL: When that happens, I press the stop button. I want that feature! 
    EE: The timing seems difficult. 
    BL: That's right, it's difficult to get the timing right when you're doing other things. EE: In the future, if possible, I want a fully automatic washer-dryer. 
    BL: "Then household chores will become quite a bit easier, right!" 
    EE: If it automatically dries as well, there wouldn't be the enjoyment of hanging clothes, but I think it would be very convenient. 
    BL: Then, I think I'll start wanting other convenient household items as well. 
    EE: I also want a Roomba. 
    BL: Me too. I'd also like to have a dishwasher. 
    EE: It's the modern version of the three sacred treasures. 
    BL: That's right! I think it will save a lot of time. 
    EE: The world has become a convenient place, hasn't it? 
    BL: The only thing left is for the Roomba to move the luggage out of the way as it goes, and it would be perfect. 
    EE: Certainly. I'm looking forward to the update. 
    BL: Looking forward to the update!
    """

    personality_traits = """
    Openness: 4.25
    EE shows a moderate level of openness. This suggests that he/she enjoys exploring new ideas and experiences, but also values stability and routine. He/she is imaginative and open to trying new things, while still being practical and grounded.
    Conscientiousness: 2.1666667461395264
    EE tends to be less focused on organization and detail. He/she may be more spontaneous and flexible, often preferring to go with the flow rather than sticking to a strict plan or schedule. This can make him/her adaptable, though it might also result in occasional lapses in discipline or reliability.
    Extraversion: 3.8333332538604736
    EE is moderately extraverted, enjoying social interactions and being around others, but also appreciating some alone time. He/she is sociable and energetic in social settings, though he/she does not require constant social stimulation to feel content.
    Agreeableness: 3.9166667461395264
    EE has a balanced approach to agreeableness. He/she is generally kind and cooperative, willing to help others and show empathy, yet also capable of standing up for himself/herself when necessary. This balance helps EE navigate social situations effectively.
    Neuroticism: 5.25
    EE experiences higher levels of emotional sensitivity and may often feel anxious or stressed. He/she is more likely to react strongly to stressors and may struggle with emotional stability at times. However, this trait also suggests that he/she is highly empathetic and deeply affected by emotional experiences.
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

    sample_1_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_1_human_human_dialogue}
    Here, EE and BL are their respective designations. Now I will provide you with EE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with EE playing the role of the Human and BL playing the role of the Computer. Specifically, you need to transform EE's utterances based on EE's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BL's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, EE and BL are their respective designations. Now I will provide you with EE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with EE playing the role of the Human and BL playing the role of the Computer. Specifically, you need to transform EE's utterances based on EE's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BL's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_1_human_computer_dialogue = llm_response(sample_1_dialogue_transformation_prompt)

    sample_1_dialogue_transformation_human_feedback = """
    """

    sample_1_human_human_ct_count = count_ct_occurrences(sample_1_human_human_dialogue)
    sample_1_human_computer_ct_count = count_ct_occurrences(sample_1_human_computer_dialogue)

    sample_1_regenerated_human_computer_dialogue = evaluate_dialogue(sample_1_human_human_dialogue, sample_1_human_computer_dialogue, personality_traits, additional_knowledge, sample_1_dialogue_transformation_human_feedback)

    print('Final sample 1 HCD: ', sample_1_regenerated_human_computer_dialogue)

    sample_2_human_computer_dialogue = llm_response(sample_2_dialogue_transformation_prompt)

    sample_2_dialogue_transformation_human_feedback = """
    """

    sample_2_human_human_ct_count = count_ct_occurrences(sample_2_human_human_dialogue)
    sample_2_human_computer_ct_count = count_ct_occurrences(sample_2_human_computer_dialogue)

    sample_2_regenerated_human_computer_dialogue = evaluate_dialogue(sample_2_human_human_dialogue, sample_2_human_computer_dialogue, personality_traits, additional_knowledge, sample_2_dialogue_transformation_human_feedback)

    print('Final sample 2 HCD: ', sample_2_regenerated_human_computer_dialogue)

