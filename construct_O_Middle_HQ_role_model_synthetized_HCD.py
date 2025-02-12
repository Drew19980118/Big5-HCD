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
        Here, HQ and GR are their respective designations. Now I will provide you with HQ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where HQ simulates the role of a Human (converting HQ's utterances in the original Human Human Dialogue), and GR simulates the role of a Computer (converting HQ's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    HQ: Hello 
    GR: Hello 
    HQ: The weather continues to be bad, doesn't it?
    GR: Let's see, today it’s barely not raining. 
    HQ: Is it sunny? GR: "It's not clear, it's cloudy." 
    HQ: "I hope it will be sunny." 
    GR: Yes, it's always raining and it makes me feel down. 
    HQ: The temperature difference is also extreme. 
    GR: It seems that drastic temperature changes can negatively affect mental health. 
    HQ: I wonder if that's why I feel uneasy. 
    GR: Maybe so. 
    HQ: It's getting colder, but it feels more like winter than autumn, doesn't it? 
    GR: It feels like we've stepped into winter but have managed to recover. 
    HQ: It was cold, so I turned on the heater. 
    GR: Is that so? That's a bit early. 
    HQ: We were using the air conditioner until recently, but now we're using the heater. 
    GR: I bought a blanket. 
    HQ: "A blanket sounds good. I need to buy one too."
    GR: I am worried if I can get by with just a blanket since I don't have a comforter. 
    HQ: Aren't you going to buy it? 
    GR: I haven't bought it because I thought I might have trouble finding a place to store it in summer. 
    HQ: Indeed, even when compressed, it still takes up space. 
    GR: It seems like we'll have to rely on the heater. 
    HQ: I think I need to clean the air conditioner. 
    GR: I have to call the contractor too. 
    HQ: It's kind of moldy. 
    GR: It gets moldy quickly, doesn't it? 
    HQ: It's scary if I mess up cleaning it myself and end up breaking it. 
    GR: That's right.
    """

    sample_2_human_human_dialogue = """
    HQ: Hello 
    GR: Hello 
    HQ: What were you doing during the three-day weekend? 
    GR: Apart from going out for a drink, I didn't do anything else. 
    HQ: It was raining, wasn't it? 
    GR: I see. What were you doing, <HQ>? 
    HQ: I was also at home the whole time. It seems my friend went to Atami. 
    GR: That sounds great. Is it a hot spring trip? 
    HQ: "It seems like it's a hot spring trip. Apparently, it was quite crowded." 
    GR: "It's a three-day weekend." 
    HQ: I guess it's better to go on ordinary weekdays. 
    GR: It would be nice if I had weekdays off from work. 
    HQ: That's right. If you have weekends off, you'll have to take paid leave. 
    GR: "That's right. But I want to go to a hot spring." 
    HQ: There are spas in the city, but isn't that kind of thing no good? 
    GR: It's a bit expensive, isn't it? 
    HQ: "Well, yeah, it might be expensive." 
    GR: "In the end, it's crowded in the city and you can't relax." 
    HQ: "That's certainly true in Tokyo. Maybe the super sentos in slightly out-of-the-way places are less crowded." 
    GR: It seems that there are many elderly people. 
    HQ: That might be the case. 
    GR: There's a super sento in the neighborhood, but the price is ridiculously high. 
    HQ: How much is it? 
    GR: It's about 3000 yen. 
    HQ: Ah, it might be a little expensive. 
    GR: "There are also non-chain public baths, and those cost around 500 yen." 
    HQ: "It's cheap, isn't it! Have you been there?" 
    GR: "I haven't been yet, but I'm thinking of going." 
    HQ: If the 500 yen one is nicer, then that one is fine, right? 
    GR: I see.
    """

    personality_traits = """
    'Openness': 3.1666667461395264
    HQ are moderately open to new experiences, balancing a healthy curiosity with practicality. HQ appreciate creative ideas and cultural experiences but are not excessively adventurous. In relationships and work, HQ value both innovation and tradition, making HQ versatile in adapting to different scenarios without losing sight of what's practical.
    'Conscientiousness': 4.666666507720947
    HQ are highly conscientious, demonstrating a strong sense of responsibility and organization. HQ likely plan ahead, set goals, and are committed to achieving them, which makes HQ reliable in both personal and professional settings. This trait aids in making thoughtful decisions and maintaining productive work habits, though it may sometimes lead to stress if perfection is overemphasized.
    'Extraversion': 4.166666507720947
    HQ are fairly extraverted, enjoying social interactions and drawing energy from being around people. HQ are outgoing and likely thrive in group settings, often taking on leadership roles. In relationships, HQ are enthusiastic and communicative, while in work, HQ sociability helps HQ build networks and collaborate effectively, though HQ also appreciate occasional solitude.
    'Agreeableness': 4.416666507720947
    HQ are quite agreeable, showing warmth, kindness, and a strong preference for harmony in interactions. HQ are likely empathetic and cooperative, often putting others' needs ahead of HQ own. This makes HQ a supportive friend and a team player at work, though it’s essential to ensure HQ own needs are also met to avoid burnout.
    'Neuroticism': 3.8333332538604736
    HQ experience a moderate level of neuroticism, meaning HQ are somewhat prone to stress and emotional fluctuations. While HQ might occasionally feel anxious or moody, these moments are balanced with periods of calm. This trait can make HQ sensitive and attuned to others' emotions, though it may also require HQ to develop coping mechanisms to manage stress effectively in personal and professional life.
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
    Here, HQ and GR are their respective designations. Now I will provide you with HQ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human-Human Dialogue into a Human Computer Dialogue, with HQ playing the role of the Human and GR playing the role of the Computer. Specifically, you need to transform HQ's utterances based on HQ's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform GR's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, HQ and GR are their respective designations. Now I will provide you with HQ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human-Human Dialogue into a Human Computer Dialogue, with HQ playing the role of the Human and GR playing the role of the Computer. Specifically, you need to transform HQ's utterances based on HQ's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform GR's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_1_human_computer_dialogue = llm_response(sample_1_dialogue_transformation_prompt)

    sample_1_dialogue_transformation_human_feedback = """
    """

    sample_1_regenerated_human_computer_dialogue = evaluate_dialogue(sample_1_human_human_dialogue, sample_1_human_computer_dialogue, personality_traits, additional_knowledge, sample_1_dialogue_transformation_human_feedback)

    print('Final sample 1 HCD: ', sample_1_regenerated_human_computer_dialogue)

    sample_2_human_computer_dialogue = llm_response(sample_2_dialogue_transformation_prompt)

    sample_2_dialogue_transformation_human_feedback = """
    """

    sample_2_regenerated_human_computer_dialogue = evaluate_dialogue(sample_2_human_human_dialogue, sample_2_human_computer_dialogue, personality_traits, additional_knowledge, sample_2_dialogue_transformation_human_feedback)

    print('Final sample 2 HCD: ', sample_2_regenerated_human_computer_dialogue)

