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
        Here, DT and CO are their respective designations. Now I will provide you with DT's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where DT simulates the role of a Human (converting DT's utterances in the original Human Human Dialogue), and CO simulates the role of a Computer (converting CO's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("DT:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    DT: Nice to meet you. 
    CO: "Nice to meet you, too." 
    DT: Did you go out somewhere today? 
    CO: No, I stayed home all day. 
    DT: When it's hot, you don't feel like going out, right? 
    CO: I see. I opened the balcony, and it was too hot, so I didn't feel like going outside. 
    DT: Are you not good with summer? 
    CO: I like summer. I want to go out and have fun because I like things like the sea. 
    DT: I see. Did you go to the beach this year? 
    CO: I haven't gone. I don't think I'll go this year either. Not until the coronavirus ends. 
    DT: When will it end? 
    CO: "That's true. Won't it be over after autumn since the peak has passed?" 
    DT: Hmm, I wonder. It seems tough... 
    CO: Is it strict? 
    DT: We can't go on a trip, can we? 
    CO: I see. Do you like traveling? 
    DT: I like it. But I prefer overseas, so I can't go at all. 
    CO: I see. Where was the last place you traveled abroad? 
    DT: It is Sweden. 
    CO: "Is it Northern Europe? I wonder if it's cold." 
    DT: I went in September, but it was already cold. 
    CO: What is that place famous for? 
    DT: It is said to be the setting for Kiki's Delivery Service. 
    CO: I see. Wasn't IKEA from Sweden? 
    DT: That's right! There was no IKEA in the city, so I didn't go. 
    CO: Is it like that? As expected, you can go to IKEA in Japan, right? 
    DT: Sure. "Yes. IKEA is sufficient in Japan." 
    CO: "Is it often Europe? Travel" 
    DT: I see. I was flying around using LCC. 
    CO: Jealous. I want to go there someday.
    """

    sample_2_human_human_dialogue = """
    DT: Good evening. 
    CO: Good evening! 
    DT: Have you bought anything recently? Other than food. 
    CO: Recently, I bought things like clothes and bags. 
    DT: Do you often buy clothes? 
    CO: "Not really. I usually wear secondhand clothes, but this time I bought something for work." 
    DT: I see. Do you do more remote work or work in the office? 
    CO: I have been going to the office more frequently now. Things have settled down a bit. 
    DT: Do you wear a suit when you go to the office? 
    CO: Now it's office casual. It's okay to wear a shirt and pants. 
    DT: "It's easy and nice, isn't it?" 
    CO: Yes, I have a lot of fieldwork now, so I can wear sneakers, and they are really comfortable. 
    DT: That was good. It seems tough to work outside during the summer. 
    CO: "It's unbearable. I feel like I'm going to get heatstroke. Are you working?" 
    DT: It's essential to carry water with you. I am currently focusing on childcare. 
    CO: I see. Have you bought anything recently? 
    DT: Recently, I bought clothes for the baby. There are so many cute ones that just looking at them is fun. 
    CO: "Oh, does it become something like Nishimatsuya? Speaking of baby clothes." 
    DT: Yes. Akachan Honpo and such. 
    CO: I see. Sometimes I go to buy something for my friend's child. 
    DT: "Is that so? Are you giving a present?" 
    CO: Yes, when I was born. But I'm not sure what to buy. 
    DT: I think anything would make them happy. I think a small toy would be nice. 
    CO: I see, I was wondering if there are any preferences. Is any toy okay? 
    DT: "It seems like there are preferences for characters, so something other than characters. Like a rattle with animals on it." 
    CO: Ah, I see. That opinion is helpful. 
    DT: I was happy to receive a toy made of rice as a present from my cousin. 
    CO: Rice? That's unusual. Is it sold normally? 
    DT: "They sell it. I was impressed because it's made from rice, so I feel safe putting it in my mouth." 
    CO: Wow, that's interesting. I'll use it as a reference.
    """

    personality_traits = """
    Openness: 4.833333492279053
    DT is quite imaginative and open to new experiences. His/her curiosity about the world and new ideas drives him/her to seek out novel and unconventional perspectives. He/she is likely to appreciate art, creativity, and a wide range of cultural experiences.
    Conscientiousness: 3.5
    DT is moderately conscientious. He/she is capable of being organized and responsible, but may sometimes struggle with consistency in these areas. He/she can be dependable but might occasionally prioritize flexibility or spontaneity over rigid structure.
    Extraversion: 3.5833332538604736
    DT is somewhat outgoing and enjoys social interactions, but he/she also values alone time. He/she can be sociable and energetic in the right settings, but he/she does not always seek out social engagements and might sometimes prefer quieter activities.
    Agreeableness: 4.333333492279053
    DT tends to be friendly, compassionate, and cooperative. He/she is generally considerate of others' feelings and strives to maintain harmonious relationships. He/she values kindness and is likely to be trusting and supportive of those around him/her.
    Neuroticism: 4.583333492279053
    DT experiences a higher than average level of emotional sensitivity and may be prone to feeling anxious or stressed. He/she may often worry and could be more susceptible to experiencing mood swings. His/her emotional responses might be intense, but this can also make him/her more empathetic towards others' emotional states.    
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
    Here, DT and CO are their respective designations. Now I will provide you with DT's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with DT playing the role of the Human and CO playing the role of the Computer. Specifically, you need to transform DT's utterances based on DT's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CO's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, DT and CO are their respective designations. Now I will provide you with DT's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with DT playing the role of the Human and CO playing the role of the Computer. Specifically, you need to transform DT's utterances based on DT's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CO's utterances into a Computer style, also without altering the content and meaning.  

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

