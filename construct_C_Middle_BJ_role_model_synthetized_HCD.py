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
        Here, BJ and BS are their respective designations. Now I will provide you with BJ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where BJ simulates the role of a Human (converting BJ's utterances in the original Human Human Dialogue), and BS simulates the role of a Computer (converting BS's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    BJ: Hello! 
    BS: Hello! 
    BJ: How often do you usually watch TV? 
    BS: One way or another, I end up watching it every day. During breakfast and dinner. 
    BJ: Oh! Do you have any favorite shows? 
    BS: I like Kaji Yaro and Banana Man's Sekkaku Gourmet! 
    BJ: It feels like dinner time! You like comedians, don't you? 
    BS: That's right. If anything, I like food, so I guess you could say I like it. Do you watch TV? 
    BJ: I see. Hmm, about once or twice a week, I guess. 
    BS: Do you feel like watching a specific program? 
    BJ: "Well, it's probably something like 'Wednesday Downtown'." 
    BS: "Was it the program that starts around 10 PM?" 
    BJ: That's right! Haven't you seen it? 
    BS: It seems like something I've seen before... I think it was a program verifying some theory... 
    BJ: Yes, that's right. Pranks are mainstream, I suppose. 
    BS: Is that so! Do you like pranks? Or is it comedians that you like? 
    BJ: I like pranks and comedians too! Do you have a favorite comedian? 
    BS: I see! Is it Sandwich Man? And Jiro from Shisonnu just makes me laugh by looking at him. 
    BJ: Both of them are very wonderful people! I like them too. 
    BS: Sure. Here is the translated sentence: "That's nice. The Sandwichman duo is also great because their hosting is steady." 
    BJ: No matter how many times I watch the year Sandwichman won the M-1, I end up crying. 
    BS: I see! I'll take a look! Do you have a favorite comedian? 
    BJ: Hmmm. I think the amazing one is Mr. Tanaka from Ungirls. 
    BS: What do you think is amazing about it? 
    BJ: Not only are they a weird character, but I also think they must be smart because they're strong in comedy improvisation! 
    BS: You are also good at Ogiri! You certainly have an intelligent image. 
    BJ: I get the feeling of an entertainer. 
    BS: Certainly. I do miss the Janga Janga era. 
    BJ: Wow, that brings back memories. Well then, let's end here for today. Thank you very much. 
    BS: Thank you very much!
    """

    sample_2_human_human_dialogue = """
    BJ: Hello! 
    BS: Hello! 
    BJ: I want to start something new, but what do you do on your days off? 
    BS: That's nice! Lately, I've been going to the library a lot. 
    BJ: Library! It's really wonderful! 
    BS: There is a relatively large library quite close to my house! 
    BJ: Do you like books? 
    BS: That's right. I love books! Digital ones are nice, but I like the feel of paper. 
    BJ: "Sounds good. I haven't read a book recently." 
    BS: I see. Is there a library or bookstore nearby? 
    BJ: Neither of them are at the nearest station. What kind of books do you like? 
    BS: That's unfortunate. I used to read novels in the past, but recently it's more practical books and self-help genres. 
    BJ: So, if I think about it, it might have been years since I last read properly. If you have any recommendations, I would love to hear them! 
    BS: I see. The book that helped lower the hurdle of finding cooking a hassle during this season was a book called "Tsumamimeshi"! 
    BJ: "I have never heard of tsumami-meshi!" 
    BS: Do you know the culinary researcher Ryuji? 
    BJ: I know! I often watch recipe videos. 
    BS: "The video is interesting, isn't it! It's that person's recipe book!" 
    BJ: "You're the one who cooks while getting drunk, right?" 
    BS: Yes, yes. He is the one who is drunk on YouTube but proper on terrestrial television. 
    BJ: Ah, you are publishing a book. That seems useful. 
    BS: "Yes. It's quick to make, so it helps during dinner time." 
    BJ: "Is that book also available in the library!?" 
    BS: Yes, it's there! There are also quite a few recipe books, which is very helpful. 
    BJ: Amazing, it seems to be quite a big place. I feel like going to the library again after a long time. 
    BS: Yes, I think the library is a good idea! They also have magazines and such! 
    BJ: More than anything, it's free, right? It would be great if there was a movie version of the library too. 
    BS: Oh, the library I go to also allows you to watch DVDs! 
    BJ: Such an amazing place! I will try to visit next time. Thank you for the wonderful suggestion. 
    BS: Yes, please enjoy.
    """

    personality_traits = """
    'Openness': 5.5
    BJ are highly imaginative and open to new experiences. BJ appreciate art, adventure, and unconventional ideas. This makes BJ curious and open-minded in both personal and professional realms, often seeking novelty and variety.
    'Conscientiousness': 3.0
    BJ tend to be flexible and spontaneous, perhaps sometimes struggling with organization and consistency. BJ might prefer to go with the flow rather than plan meticulously, which can make BJ adaptable but may sometimes lead to challenges in meeting deadlines or achieving long-term goals.
    'Extraversion': 5.083333492279053
    BJ are outgoing and sociable, enjoying the company of others and actively seeking social interactions. This trait helps BJ build networks and relationships easily and brings energy and enthusiasm into group settings. However, BJ may occasionally need to balance BJ social life with moments of solitude to recharge.
    'Agreeableness': 4.333333492279053
    BJ are generally warm and cooperative, valuing harmony and getting along well with others. This makes BJ a supportive friend and colleague, often willing to compromise for the greater good. At times, BJ might need to assert yourself more to avoid being taken advantage of.
    'Neuroticism': 5.166666507720947
    BJ experience emotions intensely and are somewhat sensitive to stress and negative emotions. This heightened sensitivity can make BJ more empathetic but also prone to anxiety and mood swings. Managing stress through healthy coping mechanisms is important for your well-being.
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
    Here, BJ and BS are their respective designations. Now I will provide you with BJ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with BJ playing the role of the Human and BS playing the role of the Computer. Specifically, you need to transform BJ's utterances based on BJ's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BS's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, BJ and BS are their respective designations. Now I will provide you with BJ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with BJ playing the role of the Human and BS playing the role of the Computer. Specifically, you need to transform BJ's utterances based on BJ's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BS's utterances into a Computer style, also without altering the content and meaning.  

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

