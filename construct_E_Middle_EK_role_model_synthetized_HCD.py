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
        Here, EK and CN are their respective designations. Now I will provide you with EK's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where EK simulates the role of a Human (converting EK's utterances in the original Human Human Dialogue), and CN simulates the role of a Computer (converting CN's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("EK:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    EK: Good evening! 
    CN: Good evening. 
    EK: It's hot again today, isn't it? 
    CN: "It's hot, isn't it? Are you doing anything to cope with the heat?" 
    EK: Basically, the air conditioning is left on 24 hours a day. 
    CN: "Same here. Are you drinking plenty of fluids?" 
    EK: I am quite careful about staying hydrated, including using oral rehydration solutions. 
    CN: If you get heatstroke, oral rehydration solutions are important, right? Do you keep them on hand? 
    EK: "I always keep it on hand. I make sure to bring it whenever I go out!" 
    CN: Sounds good! I often bring sports drinks. 
    EK: It's essential during this season, isn't it? Do you spend a lot of time outdoors? 
    CN: Basically, I stay indoors a lot. How about you? 
    EK: I'm half and half! I like exercise, so I go jogging even if it's hot. 
    CN: Amazing! How far do you run? 
    EK: It's not that much. I usually just jog about 5 kilometers. On a good day, I can manage around 10 kilometers. Do you exercise? 
    CN: I only go for walks. I do it after it gets cool in the evening. 
    EK: Sounds good. I haven't done it yet, but I'm also interested in trekking! 
    CN: If it's trekking, it seems like equipment might be necessary. Do you have any? 
    EK: Recently, I only bought shoes. Somehow, they seem to be in fashion, right? 
    CN: "Outdoor activities are becoming popular, aren't they? Do you go camping?" 
    EK: "It's not that I followed the trend, but I recently resumed camping!" 
    CN: "That's nice. Which campsite did you go to recently?" 
    EK: We went to the campsite in Karuizawa! It was too hot and not a summer resort at all. CN: "It's hot even in Karuizawa! The recent heatwave is incredible.." 
    EK: It's worrisome to think about what things will be like in 10 years, isn't it? 
    CN: Summer is almost like the tropics, isn't it? What did you make for camp meals? 
    EK: I just cooked and ate rice, but for some reason, it was delicious. 
    CN: Food tastes strangely good when you eat it outside, doesn’t it? Even convenience store bread tastes somehow delicious when eaten outside. 
    EK: That's right. With a little ingenuity, you can enjoy anything. 
    CN: It's true!
    """

    sample_2_human_human_dialogue = """
    EK: Good evening! 
    CN: Good evening. 
    EK: I've been staying up late recently. 
    CN: Oh, are you working? 
    EK: No, just lounging around. Watching movies and stuff. 
    CN: What movie did you watch recently? 
    EK: The most recent movie I watched was Jurassic World! Do you know it? 
    CN: I know. You are doing it right now, aren't you? 
    EK: That's it! 
    CN: I've heard it's interesting, but since I haven't seen the previous work, it's difficult... 
    EK: It was interesting! I definitely want you to watch it. 
    CN: "Is it okay even if I haven't seen the previous work?" 
    EK: It might make more sense if you've seen the previous work, but even if you haven't, it's exciting enough to enjoy on its own! 
    CN: Sounds good! Do you like action movies? 
    EK: I like it! Because I can watch without thinking much. Do you often watch movies? 
    CN: I don't watch much, but recently I watched a Dragon Ball movie. 
    EK: Ah, nostalgic! I love it! 
    CN: "You can enjoy that without thinking too much about it, right?" 
    EK: Right. I also like Evangelion when it comes to anime. 
    CN: It's interesting! Eva makes you think a bit, doesn't it! 
    EK: No matter how much I think about it, I can't understand it. 
    CN: "It's complicated, isn't it?" 
    EK: That's right. Watching movies at home is nice too, but I realized the other day that it's really different when you watch them in a movie theater. 
    CN: "The impact of the big screen is impressive, isn't it? The sound quality is great too!" 
    EK: I was quite surprised at how much it has evolved! 
    CN: Watching at home is nice and relaxing, but the cinema experience is different! 
    EK: It is unfortunate that movie theaters seem to be decreasing in rural areas. 
    CN: That's unfortunate... Is it difficult to attract customers? 
    EK: I thought so. I'm going to support the movie theater! 
    CN: That's nice!
    """

    personality_traits = """
    EK demonstrates a moderate level of openness, suggesting a balanced approach to new experiences and creativity. They appreciate new ideas and art but also value tradition and familiarity.
    With a high score in conscientiousness, EK is highly responsible, organized, and dependable. They likely excel at planning, goal-setting, and completing tasks with efficiency and reliability.
    A moderate score in extraversion indicates EK enjoys social interactions and has an energetic personality, but also values alone time for introspection and recharging.
    EK's high agreeableness score reflects a compassionate, cooperative, and empathetic nature. They are likely to be considerate, good-natured, and eager to help others, fostering harmonious relationships.
    Scoring moderately high in neuroticism, EK may experience some emotional sensitivity and occasional stress or anxiety, but they likely possess a good degree of resilience and emotional stability in handling life's challenges.
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
    Here, EK and CN are their respective designations. Now I will provide you with EK's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with EK playing the role of the Human and CN playing the role of the Computer. Specifically, you need to transform EK's utterances based on EK's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CN's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, EK and CN are their respective designations. Now I will provide you with EK's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with EK playing the role of the Human and CN playing the role of the Computer. Specifically, you need to transform EK's utterances based on EK's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CN's utterances into a Computer style, also without altering the content and meaning.  

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