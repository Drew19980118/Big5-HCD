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
        Here, DM and BP are their respective designations. Now I will provide you with DM's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where DM simulates the role of a Human (converting DM's utterances in the original Human Human Dialogue), and BP simulates the role of a Computer (converting BP's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    DM: Good evening, nice to meet you. 
    BP: Good evening, nice to meet you. 
    DM: What were you doing today? 
    BP: Today, I did a lot of cleaning in the morning and then relaxed with my child. 
    DM: It's the last day of Obon, isn't it? 
    BP: "That's right. I also lit the sending fire." 
    DM: I ended up spending my time lazily without even going back to my hometown. 
    BP: I see. My family gathered on the 13th because my parents' house is in the city. 
    DM: Does it feel like we gathered for the first time in a while? 
    BP: That's right. It's been a while since we got together. Out of the four siblings, three of them came with their kids. 
    DM: That's wonderful. Everyone seems to get along well. 
    BP: Yes, thanks to you, my family and siblings get along well. 
    DM: How old is your child? 
    BP: The children are in 6th grade of elementary school and 9th grade of junior high school. 
    DM: "You are preparing for an exam, right?" 
    BP: "That's right. This summer is hectic." 
    DM: "Is your child not showing any signs of being nervous yet?" 
    BP: Yes, sometimes they say "I'm nervous!" but it seems like they haven't really felt it yet. 
    DM: I caused a lot of trouble for my parents during my exam period, haha. 
    BP: Everyone goes through times like that, don't they? I feel like I was also irritable for some reason. 
    DM: I appreciate your understanding. 
    BP: My children also get irritated sometimes. They want to be alone. 
    DM: "It might be common to want to be alone." 
    BP: Yes! In a lecture for parents on how to deal with adolescence, we were told that parents just have to be prepared to be completely worn out. 
    DM: So there is such a lecture, huh. Is it held at the school? 
    BP: I received a flyer from the school and attended a lecture hosted by the city. 
    DM: I think it is admirable how much you care for your child. 
    BP: No, no, I went through the same path myself, so I thought I should be prepared. 
    DM: "I am cheering you on from the shadows. Please do your best without overworking yourself." 
    BP: Thank you very much! Well then, let's call it a day.
    """

    sample_2_human_human_dialogue = """
    DM: Nice to meet you. Please. 
    BP: Thank you very much! 
    DM: Do you have any hobbies? 
    BP: Recently, I enjoy watching analyses and explanations of dramas on YouTube. 
    DM: "Is it on YouTube? I didn't know there were such videos!" 
    BP: That's right. There are many analysis drama series and historical drama series that come up when you search for them. 
    DM: Dramas are quite intricate and difficult, aren't they? 
    BP: That's right. During the previous season, I was watching analysis videos of My Family. 
    DM: Does the investigation enjoy reasoning? 
    BP: I see. In "My Family," there are several suspects and the real culprit, and we were trying to figure out who that is. 
    DM: Did you win? 
    BP: My reasoning was correct! But, I didn't understand the motive for the crime at all. 
    DM: "That's amazing! Why did you think it was the culprit?" 
    BP: "There were actions and words that raised flags along the way, so I thought it might be this person!" 
    DM: You're sharp, haha. I find it difficult and am not good at it, haha. 
    BP: It might be fun once you start watching. Don't you watch YouTube much? 
    DM: I watch YouTube quite a bit! 
    BP: I see. My children don't watch TV either; they only watch YouTube. 
    DM: Are kids these days like that? 
    BP: It seems so. Nowadays, you can watch it on TV, and each person has their own tablet. 
    DM: I see. Actually, I don't own a TV either. 
    BP: "Oh, really? It seems like the number of young people like that is increasing these days." 
    DM: It seems like if I have a TV, I'll end up leaving it on and lazing around, haha. 
    BP: I see. You can also watch TV programs on Tver now. 
    DM: "I saw it in an advertisement. Was it a service like catch-up streaming?" 
    BP: Yes, after it's broadcast on TV, you can watch it for free for about a week. 
    DM: It's convenient. I've become interested in recent dramas, so maybe I'll give them a watch. 
    BP: That's right! The drama currently airing, where Mei Nagano-chan rides a unicorn, is interesting. 
    DM: Thank you for the recommendation! I definitely want to check it out. 
    BP: Yes, I'm glad I could be of help. Thank you very much.
    """

    personality_traits = """
    'Openness': 5.083333492279053
    DM are highly imaginative and open to new experiences. This score suggests a strong appreciation for art, adventure, unusual ideas, curiosity, and variety of experience. DM are likely to enjoy exploring different cultures, philosophies, and innovative ways of thinking. This trait enhances DM creativity and problem-solving skills, making DM adaptable and forward-thinking in both personal and professional settings.
    'Conscientiousness': 3.75
    DM show moderate levels of organization and reliability. This score indicates that DM can be diligent and disciplined, but DM also allow yourself flexibility. DM are capable of planning and executing tasks effectively, but DM might not be overly rigid about deadlines. In relationships and work, DM balance responsibility with spontaneity, which helps DM stay productive while still enjoying leisure time.
    'Extraversion': 5.083333492279053
    DM are quite sociable and energetic, enjoying being around people and engaging in social activities. This score reflects a tendency to be outgoing, enthusiastic, and assertive. DM likely find it easy to make new friends and thrive in environments that require interaction and collaboration. This trait often makes DM the life of the party and a natural leader in group settings.
    'Agreeableness': 5.75
    DM are exceptionally kind, cooperative, and empathetic towards others. This score reveals a strong inclination to be compassionate, considerate, and trusting. DM relationships are marked by a high level of harmony and mutual respect. In professional and personal interactions, DM are likely to prioritize collaboration and conflict resolution, often putting others' needs before DM own.
    'Neuroticism': 3.5833332538604736
    DM experience moderate levels of emotional instability and stress. This score suggests that while DM can sometimes be prone to anxiety and mood swings, DM generally manage to cope with life's pressures relatively well. DM may occasionally feel overwhelmed, but DM are also resilient and capable of finding balance. In relationships and work, this trait might make DM sensitive to criticism but also empathetic towards others' struggles.
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
    Here, DM and BP are their respective designations. Now I will provide you with DM's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with DM playing the role of the Human and BP playing the role of the Computer. Specifically, you need to transform DM's utterances based on DM's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BP's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, DM and BP are their respective designations. Now I will provide you with DM's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with DM playing the role of the Human and BP playing the role of the Computer. Specifically, you need to transform DM's utterances based on DM's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BP's utterances into a Computer style, also without altering the content and meaning.  

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