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
        Here, CO and CN are their respective designations. Now I will provide you with CO's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where CO simulates the role of a Human (converting CO's utterances in the original Human Human Dialogue), and CN simulates the role of a Computer (converting CN's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("CO:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    CO: Good morning! 
    CN: Good morning! 
    CO: What do you do on your days off? 
    CN: Doing housework and reading. 
    CO: Do you like reading? 
    CN: I like you! 
    CO: What have you read recently? 
    CN: I am reading a book on health management. 
    CO: Oh, that's interesting. 
    CN: Lately, I've been feeling unwell more often. 
    CO: I see. Has it not been managed until now? 
    CN: I haven't done much. 
    CO: Was it due to an unhealthy lifestyle? 
    CN: I think the biggest factor is that commuting has decreased due to COVID-19, and thus my level of physical activity has decreased. 
    CO: I see. Are you doing something now? 
    CN: I try to walk for about 30 minutes. 
    CO: Sounds good. I'm doing it too. 
    CN: Have you decided on a course? 
    CO: Yes, there is a park, and it has been decided that it will be held there. 
    CN: Sounds good. Our house is near the road. 
    CO: I see. How far do you walk?
    CN: It is about 1 to 2 kilograms. 
    CO: That’s good. Continuing is important, isn’t it? 
    CN: I see. I feel like I sleep well when I exercise. 
    CO: Certainly, I feel that too. 
    CN: If I don't leave the house, I don't sleep well. 
    CO: Is it good to get moderately tired? 
    CN: I feel the need to move my body. 
    CO: Talking about this kind of thing motivates me. 
    CN: When you realize that there are other people doing it, right!
    """

    sample_2_human_human_dialogue = """
    CO: Good morning! 
    CN: Good morning! 
    CO: Do you like watching sports? 
    CN: I like it! I often watch baseball. 
    CO: Is that so? High school baseball has started. 
    CN: "It has started. My home prefecture lost early on." 
    CO: I see, is the opponent a strong team? 
    CN: They are a strong team. It was worth watching. 
    CO: "Do you actually go to see it?" 
    CN: "I used to go watch professional baseball games." 
    CO: I see, that sounds good, the stadium. 
    CN: Baseball is fun, and recently you can also enjoy ballpark gourmet food. 
    CO: I don't know about ballpark food. 
    CN: "There is a menu produced by the athlete." 
    CO: Oh, that sounds interesting. I didn't know because I haven't been there recently. 
    CN: The favorite foods of that athlete and local specialties are featured. 
    CO: Do you have any recommendations? 
    CN: It changes every season, but the karaage bowl was delicious. 
    CO: Oh, I will check it out next time. Do you have a favorite baseball team? 
    CN: I watch because I like the Carp. 
    CO: Are you from Hiroshima? 
    CN: Yes. Do you have a favorite baseball team, <CO>? 
    CO: When I was a child, I liked the Giants. 
    CN: Oh, are you not currently supporting any particular team? 
    CO: Yes, now it has become soccer. 
    CN: "I see, where do you watch soccer?" 
    CO: I often watch the matches of Japanese athletes overseas. 
    CN: "Overseas ones are really impressive, aren't they? Japanese ones are also great, though." 
    CO: Yes, but the match is in the middle of the night, which is tough. I end up sleep-deprived. 
    CN: I see, there's a time difference.
    """

    personality_traits = """
    Openness: 4.83
    CO has a relatively high level of openness, suggesting a curious and imaginative individual who is open to new experiences and enjoys exploring novel ideas. His/her interests are likely diverse, and he/she appreciates creativity and unconventional thinking.
    Conscientiousness: 4.25
    With a score indicating a good level of conscientiousness, CO is likely disciplined, reliable, and well-organized. He/she tends to plan ahead, set goals, and work diligently to achieve them, showing a strong sense of responsibility and dependability.
    Extraversion: 3.92
    CO's moderate level of extraversion suggests a balanced social life. He/she enjoys social interactions and can be outgoing and energetic in the right situations but also values some quiet, solitary time. His/her social activities are likely enjoyable but not overwhelmingly necessary for well-being.
    Agreeableness: 4.5
    CO demonstrates a high level of agreeableness, indicating a compassionate, cooperative, and friendly nature. He/she is likely to be considerate, altruistic, and eager to maintain harmonious relationships, often putting others’ needs and feelings first.
    Neuroticism: 3.17
    With a moderate score on neuroticism, CO experiences some degree of emotional variability but generally maintains a balance. He/she might occasionally feel anxious or moody but usually can manage stress and maintain a positive outlook. This balance helps in coping with life's challenges without being overly affected.
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
    Here, CO and CN are their respective designations. Now I will provide you with CO's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with CO playing the role of the Human and CN playing the role of the Computer. Specifically, you need to transform CO's utterances based on CO's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CN's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, CO and CN are their respective designations. Now I will provide you with CO's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with CO playing the role of the Human and CN playing the role of the Computer. Specifically, you need to transform CO's utterances based on CO's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CN's utterances into a Computer style, also without altering the content and meaning.  

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