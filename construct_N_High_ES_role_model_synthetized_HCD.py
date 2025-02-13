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
        Here, ES and ER are their respective designations. Now I will provide you with ES's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where ES simulates the role of a Human (converting ES's utterances in the original Human Human Dialogue), and ER simulates the role of a Computer (converting ER's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    ES: Hello! 
    ER: Hello! Nice to meet you! 
    ES: What did you have for lunch? 
    ER: I had curry for lunch. 
    ES: Curry sounds good! Is it homemade? 
    ER: No, I ate at the restaurant. 
    ES: Is this a curry restaurant? 
    ER: Yes, this is Go! Go! Curry's sausage curry. 
    ES: "I've been interested in Go! Go! Curry!" 
    ER: You can choose various toppings and it's delicious! 
    ES: "Is it like CoCo Ichibanya?" 
    ER: I see. The roux is fixed, and you can choose items like fried shrimp or cutlets in addition to sausages. 
    ES: "The ingredients are luxurious! Do you always eat out for lunch?" 
    ER: It depends on the day. Today I had errands to run, so I ate out. 
    ES: I see. I always eat lunch at home, so I'm envious. 
    ER: "It's an occasional luxury. What did you have for lunch over there?" 
    ES: I am egg over rice. It's simple and I laughed at myself. 
    ER: I think tamago kake gohan is good! It's quick and easy to make. 
    ES: "That's right. Since I'm alone during the day, I'm not too particular. Besides curry, what do you often eat?" 
    ER: Usually, I have things like kimchi and rice, or ochazuke. 
    ES: When it comes to home-cooked meals, they are similar! 
    ER: I see, I'm usually indifferent since I eat lunch alone as well. 
    ES: When you're alone, you don't make much effort, do you? Frozen udon is also convenient and I often eat it. 
    ER: Frozen udon is also nice, and it seems delicious chilled during hot seasons. 
    ES: "There are many convenient ways to eat, right? Maybe I should try dining out once in a while too." 
    ER: I think it's good. I believe it will also be a nice change of pace! 
    ES: For now, I'll try Go! Go! Curry! 
    ER: Absolutely! Since there are various types initially and it can be confusing, it might be a good idea to research online beforehand. 
    ES: I'll check the internet right away! Thank you for letting me know. 
    ER: No, no, thank you!
    """

    sample_2_human_human_dialogue = """
    ES: Hello, nice to meet you. 
    ER: Hello! Nice to meet you! 
    ES: I am currently looking for a new hobby. Do you have anything you enjoy? 
    ER: I like playing musical instruments. 
    ES: "Wow, what kind of instrument is it?" 
    ER: I play the bass. 
    ES: The bass is nice! Do you attend any classes or something? 
    ER: No, I am practicing while watching practice videos on YouTube. 
    ES: Are you self-taught? That's amazing, I didn't know YouTube could be used that way. 
    ER: There are quite a few practice methods and sheet music on YouTube. I also thought it has become convenient. 
    ES: It's more freeing than attending classes, isn't it? Why did you decide to play the bass? 
    ER: I had friends who played the guitar and drums, so it was like, "Why not...?" 
    ES: You can form a band! 
    ER: That's right! I started practicing the bass here because I thought we could form a band. 
    ES: "I admire your band. Do you also double as the vocalist?" 
    ER: No, we asked another friend to do the vocals. 
    ES: "Then it's perfect! Playing instruments seems like it can relieve stress too, so it's great." 
    ER: Since it's a rental, I listen to sound through headphones, but playing sound loudly is a great stress relief. 
    ES: "It's convenient that you can do it even with headphones. I want to play a wind instrument, but since I live in a rental, I'll have to rent a place." 
    ER: Wind instruments can have sound leaks, you know. 
    ES: Well, I haven't quite been able to take the step yet. 
    ER: There are studios that become cheaper for individual practice, so it would be nice if there are such places. 
    ES: There's a studio like that! If I practice, please let me join the band. 
    ER: "Sounds good! Wind instruments really stand out! Which wind instrument do you want to play?" 
    ES: I am interested in the trumpet. After all, it feels so glamorous.
    ER: "Trumpet is nice. Is there any piece you would like to try playing?" 
    ES: I want to be able to play classic masterpieces. Masterpieces are cool, aren't they? 
    ER: That's right. Even if you play alone, the listeners will still be impressed! 
    ES: Sure, let's talk about music again sometime! 
    ER: Yes! Thank you very much!
    """

    personality_traits = """
    'Openness': 4.666666507720947
    ES are curious and imaginative, with a strong appreciation for art, adventure, and new experiences. ES openness leads ES to embrace change and seek out new knowledge, often thinking creatively and outside the box. This trait positively influences ES ability to adapt to different situations, appreciate diverse perspectives, and engage in innovative problem-solving.
    'Conscientiousness': 4.166666507720947
    ES are reliable, well-organized, and disciplined, often setting and achieving high standards for ES. This conscientiousness drives ES to be diligent in your tasks, managing ES time effectively, and paying attention to detail. ES work habits reflect a strong sense of responsibility, and ES can be counted on to follow through with ES commitments, which earns the trust and respect of those around ES.
    'Extraversion': 3.9166667461395264
    ES are moderately outgoing and sociable, enjoying social interactions and stimulating environments, but ES also appreciate some quiet, reflective time. ES balanced extraversion allows ES to connect well with others while maintaining ES independence. ES are likely to be comfortable in both social settings and solitary activities, which helps ES build meaningful relationships without feeling overwhelmed.
    'Agreeableness': 3.9166667461395264
    ES are generally kind, empathetic, and cooperative, valuing harmony and positive relationships. ES agreeableness makes ES a considerate and supportive friend, often placing a high value on helping others and resolving conflicts. While ES are compassionate and understanding, ES also balance ES own needs, ensuring that ES maintain healthy boundaries in ES interactions.
    'Neuroticism': 5.0
    ES experience emotional fluctuations and can be sensitive to stress, often feeling anxious or self-conscious in challenging situations. ES higher neuroticism means ES are attuned to potential threats and can be very self-aware. While this sensitivity can sometimes lead to worry, it also makes ES empathetic and emotionally expressive, fostering deep connections with others who appreciate ES openness about ES feelings.
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
    Here, ES and ER are their respective designations. Now I will provide you with ES's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with ES playing the role of the Human and ER playing the role of the Computer. Specifically, you need to transform ES's utterances based on ES's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform ER's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, ES and ER are their respective designations. Now I will provide you with ES's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with ES playing the role of the Human and ER playing the role of the Computer. Specifically, you need to transform ES's utterances based on ES's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform ER's utterances into a Computer style, also without altering the content and meaning.  

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