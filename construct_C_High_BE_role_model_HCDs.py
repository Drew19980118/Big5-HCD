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
        Here, BE and AQ are their respective designations. Now I will provide you with BE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where BE simulates the role of a Human (converting BE's utterances in the original Human Human Dialogue), and AQ simulates the role of a Computer (converting AQ's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("BE:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    BE: Hello! 
    AQ: Hello. 
    BE: What time did you wake up today? 
    AQ: It's 6 o'clock today. 
    BE: Early riser! 
    AQ: The child wakes up early. 
    BE: I see. It's not during summer vacation? 
    AQ: It's summer vacation. 
    BE: Even though it's your day off, it's impressive that you wake up early. 
    AQ: It seems I wake up naturally. 
    BE: Wonderful... 
    AQ: You have a good habit. 
    BE: "So, do you go to bed early at night?" 
    AQ: I see. I usually go to bed around 9 PM. 
    BE: It really is early to bed and early to rise. 
    AQ: I hope you will continue this. 
    BE: It seems that habits are hard to break! 
    AQ: I hope so. What time did you wake up? 
    BE: I am around 7 o'clock! 
    AQ: It's plenty early! 
    BE: Even if I wake up early, there's nothing special to do lol. 
    AQ: Haha. But I can finish the housework quickly. 
    BE: Yes, in the mornings I usually do cleaning. 
    AQ: Amazing! Do you clean every day? 
    BE: Almost every day! Because I like cleaning! 
    AQ: I'm really jealous. 
    BE: I'm not good at tidying up. 
    AQ: Yes, yes, I'm not good at either of them. 
    BE: "The person who is good at it should do it!" 
    AQ: Let's talk again.
    """

    sample_2_human_human_dialogue = """
    BE: Hello! 
    AQ: Hello. 
    BE: What is your hobby, <AQ>? 
    AQ: Self-taught piano, right? 
    BE: Amazing! And you learned it by yourself? 
    AQ: It's not a big deal. 
    BE: There was a piano lesson, but I was completely hopeless. 
    AQ: "It's difficult if you haven't learned it, isn't it?" 
    BE: First of all, I cannot read musical notes instantly. 
    AQ: I might not be able to read it instantly either. 
    BE: "I was counting them one by one and writing down how to read them." 
    AQ: Yes, yes, that's enough. Do you have any hobbies? 
    BE: Reading, I guess. 
    AQ: Intelligent! 
    BE: "It's just like in the manga!" 
    AQ: No, no! I'm the kind of person who just can't sit still. 
    BE: Isn't the piano staying still? 
    AQ: "Oh, you're right!" 
    BE: "Are you playing while moving? LOL" 
    AQ: "That was a sharp remark!" 
    BE: "I thought staying still was the best, haha." 
    AQ: "It's true! <BE> is so smart!" 
    BE: That's not true...! 
    AQ: "Are you into cultural activities?" 
    BE: Yes, I take pride in that. 
    AQ: "I got that impression." 
    BE: Maybe not an active person. 
    AQ: "Are you an indoor person?" 
    BE: "Purely an indoor person." 
    AQ: I see. Let's talk again.
    """

    personality_traits = """
    BE scores moderately high on Openness, indicating a person who enjoys exploring new experiences and ideas but is also grounded and practical. They appreciate creativity but balance it with realism.
    Their high score in Conscientiousness suggests that BE is reliable, organized, and prefers to plan ahead. They are disciplined and strive for achievement, often setting high standards for themselves.
    With a relatively high Extraversion score, BE is sociable, energetic, and enjoys being around others. They are likely to be enthusiastic and assertive in social situations.
    BE’s high Agreeableness indicates that they are compassionate, cooperative, and value getting along with others. They are empathetic, often putting others' needs before their own, and strive to maintain harmonious relationships.
    A moderately high score in Neuroticism implies that BE experiences emotions intensely and may be prone to stress or anxiety. They are sensitive to their environment and can be quite self-aware, but may need to manage their emotional responses carefully.
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

    sample_1_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_1_human_human_dialogue}
    Here, BE and AQ are their respective designations. Now I will provide you with BE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with BE playing the role of the Human and AQ playing the role of the Computer. Specifically, you need to transform BE's utterances based on BE's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AQ's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, BE and AQ are their respective designations. Now I will provide you with BE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with BE playing the role of the Human and AQ playing the role of the Computer. Specifically, you need to transform BE's utterances based on BE's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AQ's utterances into a Computer style, also without altering the content and meaning.  

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

