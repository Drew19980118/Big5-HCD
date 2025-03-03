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
        Here, EA and CP are their respective designations. Now I will provide you with EA's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where EA simulates the role of a Human (converting EA's utterances in the original Human Human Dialogue), and CP simulates the role of a Computer (converting CP's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("EA:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    EA: Hello! 
    CP: Hello! 
    EA: "It's been hot lately, hasn't it? Are you doing anything to cope with it?" 
    CP: "I put up the bamboo blinds!"
    EA: "Is it a sudare? I've heard of it, but what kind was it again?" 
    CP: The thing woven from grass? that covers windows and such. 
    EA: Oh, I remember now! Is that used to open windows? 
    CP: No, no. It's to avoid the sunlight. Even with the windows closed, it creates a nice shade. 
    EA: "I see. Is it like a curtain?" 
    CP: Actually, I wanted to have a green curtain. 
    EA: "Is it a green curtain?" 
    CP: It's the thing where you let gourds and such climb on nets hanging from the second floor of the house. 
    EA: "Oh, it feels like a curtain made of plants. It seems like taking care of it would be quite difficult, right?" 
    CP: Goya can be left alone apparently. I find it troublesome to attach the net! 
    EA: Is that so! Can you eat it when the bitter melon grows? 
    CP: Of course! It's delicious, isn't it! 
    EA: "It's delicious, isn't it? I didn't like it much when I was a child, though." 
    CP: I understand. I started liking it after becoming an adult. 
    EA: Vegetables often give that kind of impression, don't they? Eggplants too. 
    CP: Yes, especially summer vegetables! 
    EA: Summer vegetables are nice! Like cucumbers. I feel like I've aged. 
    CP: Cucumber! It's the season for delicious whole bites. 
    EA: "It's fresh and delicious, right? It goes well with alcohol too." 
    CP: Right! By the way, how do you cook bitter melon? 
    EA: "I only know about goya champuru, what other dishes are there?" 
    CP: Champuru is nice! I also make tsukudani and salad. 
    EA: Both the tsukudani and the salad look delicious! Maybe I'll look up a recipe and try making them next time. 
    CP: Definitely! Salad mixed with canned tuna is quite good! 
    EA: "It looks like it can be done easily! It seems good for summer as well." 
    CP: Yes! It also goes well with alcohol!
    """

    sample_2_human_human_dialogue = """
    EA: Nice to meet you, hello. 
    CP: Nice to meet you! 
    EA: Did you take any lessons or classes when you were a child? 
    CP: I used to do piano and swimming. 
    EA: Do you still like piano and swimming? 
    CP: "I can't read sheet music for the piano, you know. I still swim!" 
    EA: Does that mean you didn't play the piano for a very long period of time? 
    CP: No, I've actually been playing quite a bit. I can even play some relatively difficult songs. 
    EA: Is that so? It's something you can play even if you can't read sheet music! 
    CP: It's mysterious, isn't it? The teacher was surprised. 
    EA: It feels like you've completely memorized it with your fingers. I really sense an incredible talent. 
    CP: No, no. I really guessed! Just somehow! Because of that, it seems like no matter how hard I try, I can't play it. 
    EA: I see. Are you very good at swimming since you've been doing it for a long time? 
    CP: The time is not so fast anymore, but I can keep swimming for one or two kilometers continuously. 
    EA: "Wow, that's amazing! I'm struggling with even 25 meters. I probably can't do it now." 
    CP: I see. Did you take any lessons? 
    EA: "You played tennis, right? For about 4 to 5 years?" 
    CP: Tennis! Amazing! Was it around the time you were in elementary school? 
    EA: "I started in middle school. My friends invited me. I'm not that good at it though!" 
    CP: I see. Is it hardball? 
    EA: It's hardball. I've also experienced softball in school classes, but it was completely different. 
    CP: You say so, right? I've played softball for fun. 
    EA: I remember it being fun to hit with all my strength in the softball. In the hardball, my grip strength was trained. 
    CP: Oh, really? That much of a difference. By the way, what is your grip strength? EA: Around 50. How about you? 
    CP: "Amazing, amazing! Umm, probably less than 20." 
    EA: As I thought, you can't improve your grip strength without training, huh? It was the same for the people around me too. 
    CP: I see. I certainly don't remember ever working out. 
    EA: "In hardball tennis, if you don't have grip strength, the racket will fly away." 
    CP: I see! I didn't know that!
    """

    personality_traits = """
    Openness: 4.833333492279053
    EA is quite open to new experiences and ideas. His/her imagination and curiosity drive him/her to explore new concepts and embrace unconventional perspectives. This score indicates a balanced appreciation for both novel and traditional elements, suggesting EA is adaptable and willing to consider different viewpoints.
    Conscientiousness: 3.8333332538604736
    EA has a moderate level of conscientiousness, reflecting a tendency to be responsible and organized, but also allowing for some flexibility and spontaneity. He/she likely plans ahead and strives for efficiency in his/her endeavors, but isn’t overly rigid in his/her approach.
    Extraversion: 3.8333332538604736
    EA enjoys social interactions and draws energy from engaging with others, but is also comfortable spending time alone. He/she has a balanced approach to socializing, enjoying the company of friends and family without needing constant interaction to feel fulfilled.
    Agreeableness: 4.166666507720947
    EA tends to be cooperative, compassionate, and friendly. He/she is likely to be considerate of others' feelings and strives to maintain harmony in his/her relationships. This score indicates a strong preference for positive social interactions and a willingness to put others' needs alongside or occasionally ahead of his/her own.
    Neuroticism: 3.3333332538604736
    EA experiences a moderate level of emotional reactivity. He/she may sometimes feel anxious or stressed, but generally manages to cope well with life's challenges. This score suggests that while EA might occasionally experience emotional ups and downs, he/she has a fairly stable and resilient disposition.
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
    Here, EA and CP are their respective designations. Now I will provide you with EA's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with EA playing the role of the Human and CP playing the role of the Computer. Specifically, you need to transform EA's utterances based on EA's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CP's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, EA and CP are their respective designations. Now I will provide you with EA's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with EA playing the role of the Human and CP playing the role of the Computer. Specifically, you need to transform EA's utterances based on EA's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CP's utterances into a Computer style, also without altering the content and meaning.  

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