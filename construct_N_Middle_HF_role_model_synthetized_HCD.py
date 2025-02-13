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
        Here, HF and GL are their respective designations. Now I will provide you with HF's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where HF simulates the role of a Human (converting HF's utterances in the original Human Human Dialogue), and GL simulates the role of a Computer (converting GL's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    HF: Hello 
    GL: Hello, nice to meet you. 
    HF: Have you been into anything lately? 
    GL: That's right. Maybe it's decluttering. 
    HF: I see! You mean a minimalist! 
    GL: It's not to the point of being a minimalist, but it feels like I'm following the trend. 
    HF: What kind of things have you decluttered recently? 
    GL: Sure. The translated sentence is: "Yes, it is. Documents, books, clothes, and so on." 
    HF: I see! Was there a lot? 
    GL: Yes, I had been accumulating them for several years, so I disposed of them all at once! 
    HF: I see. Do you like reading books? 
    GL: I see. I haven't been reading much lately. So, I have gotten rid of most of them. 
    HF: What kind of genres did you read before? 
    GL: I see. Modern literature and self-help books, I suppose. 
    HF: That's nice! Do you read manga? 
    GL: "I have recently stopped reading manga altogether, do you read manga often?" 
    HF: I don't read much myself, but recently I've been following One Piece. 
    GL: I see. It looks like One Piece is available for free. There's also a movie playing. 
    HF: That's right. You can read it for free now! Have you ever read One Piece? 
    GL: Yes, the standalone books are probably in the first half, and the anime was up to a few years ago, but I have reviewed the story for now. HF: I see! What kind of manga have you been reading so far? 
    GL: I see. I was reading some old manga due to the influence of an acquaintance. Things like Dragon Ball and JoJo's Bizarre Adventure. 
    HF: I really like Dragon Ball a lot too! Have you watched the anime? 
    GL: I see. Yes, but I haven't watched the recent Dragon Ball anime. 
    HF: I don't know much about the recent ones either! Have you seen Z or GT? 
    GL: Yes, I've only watched up to a certain point in GT, but that's really all I've seen! 
    HF: I see! I really like GT's songs and listen to them often. 
    GL: That's right. I occasionally listen to music! 
    HF: Sounds good! Anime songs have many good tunes, so please try listening to various ones. 
    GL: Yes, thank you very much!
    """

    sample_2_human_human_dialogue = """
    HF: Hello! Nice to meet you. 
    GL: Hello, nice to meet you! 
    HF: What kind of club activities did you participate in during your undergraduate days? 
    GL: I was in the swimming club. 
    HF: How long have you been swimming? 
    GL: It's been 12 years. 
    HF: "It's long, isn't it! How old were you when you started?" 
    GL: Since about the age of 7. 
    HF: That's amazing! Do you still go swimming even now? 
    GL: Yes, it's not an exaggeration to say that this is the only sport I can do. 
    HF: I see! I'm envious of your ability to swim. 
    GL: No, no, did you play any sports? 
    HF: I was playing soccer and tennis. 
    GL: I see! Are both of them club activities? 
    HF: Both are club activities! 
    GL: Outdoor activities are tough in the heat, aren't they? 
    HF: It's tough! Even now, I still play soccer occasionally, but it's so hot that I get exhausted quickly. 
    GL: I see. I used to play soccer quite a while ago too, so I occasionally play futsal.
    HF: Were you taking soccer lessons? 
    GL: Yes, it was when I was young, for about six years. I'm not good at it. 
    HF: You were pretty good! Do you have a favorite soccer team? 
    GL: I see. I don't particularly have a favorite, but if I had to choose, it would be the local J-League team. 
    HF: I see! Have you ever been to a game? 
    GL: Yes, I went to watch it when I was young. I remember going down to the field and having some experiences too.
    HF: That's amazing! Haven't you gone recently? 
    GL: Yes, I haven't gone recently, so I would like to go if I have the chance. I mostly watch it on TV. 
    HF: After all, watching it on TV is more comfortable, isn't it? But if you actually go, it's really exciting, so please give it a try. 
    GL: I see! I definitely want to go. The sense of presence is different, isn't it? 
    HF: It's fun to sing cheering songs. 
    GL: Indeed, it gets exciting.
    """

    personality_traits = """
    'Openness': 4.583333492279053
    HF are relatively open to new experiences and enjoy exploring different ideas and perspectives. HF appreciate creativity and variety but are also grounded in practical realities. This balance allows HF to be flexible in HF thinking and adaptable in HF approach to new situations, making HF approachable and interesting in social settings.
    'Conscientiousness': 4.75
    HF are quite organized and responsible, often showing strong self-discipline and a commitment to HF goals. While HF value planning and efficiency, HF also know when to relax standards to accommodate unexpected changes. In both personal and professional arenas, people can rely on HF to follow through on commitments and manage HF time effectively.
    'Extraversion': 5.083333492279053
    HF are outgoing and sociable, thriving in environments where HF can interact with others. HF find energy in social activities and often take the initiative in group settings. HF enthusiasm and assertiveness can inspire others and foster strong connections, though HF also recognize the importance of occasional solitude to recharge.
    'Agreeableness': 5.333333492279053
    HF are highly empathetic and cooperative, often placing a strong emphasis on getting along with others. HF value harmony and are willing to make sacrifices for the well-being of those around HF. This trait makes HF a supportive friend and colleague, although it’s important for HF to maintain boundaries to avoid being overly accommodating.
    'Neuroticism': 3.4166667461395264
    HF are generally stable and composed, able to handle stress without becoming overwhelmed. While HF do experience negative emotions, they do not dominate HF life. This emotional resilience allows HF to maintain a positive outlook and cope effectively with challenges, contributing to HF overall well-being and balanced relationships.
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
    Here, HF and GL are their respective designations. Now I will provide you with HF's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with HF playing the role of the Human and GL playing the role of the Computer. Specifically, you need to transform HF's utterances based on HF's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform GL's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, HF and GL are their respective designations. Now I will provide you with HF's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with HF playing the role of the Human and GL playing the role of the Computer. Specifically, you need to transform HF's utterances based on HF's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform GL's utterances into a Computer style, also without altering the content and meaning.  

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