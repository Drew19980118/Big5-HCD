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
        Here, CX and BU are their respective designations. Now I will provide you with CX's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where CX simulates the role of a Human (converting CX's utterances in the original Human Human Dialogue), and BU simulates the role of a Computer (converting BU's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    CX: Hello! Nice to meet you! 
    BU: Hello! Please! 
    CX: How is the weather there today? 
    BU: It's still sunny now. 
    CX: I see, it's also clear weather here today. 
    BU: The forecast says it's going to rain, but do you think a typhoon is coming? 
    CX: I saw it on the news. I hope it doesn't come. 
    BU: Will the typhoon hit? 
    CX: Actually, I'm in Hokkaido, so I haven't received that kind of information yet. 
    BU: By the time it gets around there, it will already have disappeared. It seems like there are fewer typhoons in Hokkaido. 
    CX: That's right. We don't usually get much impact from typhoons. 
    BU: "Sounds good. The humidity doesn't seem too high either." 
    CX: This year, it's been raining a lot and it's pretty humid. 
    BU: I see. If you come to Honshu, it will be even hotter. 
    CX: I went to Tokyo at the beginning of July this year, and it was too hot. 
    BU: That's right. When you return from Hokkaido, the moment you get off the plane it really hits you, doesn't it? 
    CX: Yes. The moment I landed at Haneda, it felt stuffy. 
    BU: The temperature is also a factor, but it's mostly the humidity. 
    CX: When it's humid, the discomfort index goes up and it's unpleasant, right? 
    BU: That's right. I don't mind it at all as long as it's dry. 
    CX: When the weather is dry and there is a moderate breeze, it feels cool, doesn't it? 
    BU: That's right. This season, Hokkaido seems really comfortable to live in, which is nice. 
    CX: It's often said, but recently Hokkaido has been quite hot. 
    BU: I see. But compared to here, I've only been there once, so I'd like to go again. 
    CX: Certainly, it's better compared to the Honshu region. 
    BU: I think it's quite an improvement. 
    CX: On the contrary, I want to go over there in winter. 
    BU: I hate winter, so I don't like anywhere. 
    CX: I see. Then winter must be tough. 
    BU: Yes, it's spicy. Thank you very much!
    """

    sample_2_human_human_dialogue = """
    CX: Nice to meet you. What are your hobbies and interests? 
    BU: Sure! Music, right? 
    CX: "Music? I like it too. What kind of music do you like?"
    BU: "Is it about your favorite genre?" 
    CX: "Whether it's a genre, a song, or an instrument." 
    BU: I listen to anything. I like songs and instrumentals, and I also like playing instruments. 
    CX: "You like all genres, don't you? What is your favorite right now?" 
    BU: I wonder what it is. I like 90s music. 
    CX: "That's great! Nostalgic melodies! I like them too!" 
    BU: What do you like? 
    CX: The first thing that came to mind was Kome Kome Club. 
    BU: "That's nice. So nostalgic." 
    CX: I often went to concerts after they disbanded and reformed, not in real time. 
    BU: You like it that much, huh? 
    CX: Once I went on a whim, I got hooked on the fun of concerts. 
    BU: Living is good, isn't it? I haven't been able to go at all recently. 
    CX: Since the pandemic started, concerts and other events have been canceled, making it difficult to attend them, right? 
    BU: That’s also true. 
    CX: When one member takes a break, it somehow feels a bit off. 
    BU: I see. Nowadays, everyone can have a good environment at home for listening, rather than live. 
    CX: Certainly. If the level of audio equipment and VR improves, it might be that we don't need to go out of our way anymore. 
    BU: "Indeed. Still, I understand the appeal of live performances. Festivals are nice during this season." 
    CX: That's right. But it's tough when performers cancel on the day of the festival. 
    BU: It's unfortunate for the people who were looking forward to that artist. But the person themselves is suffering the most. 
    CX: That's right. And that's also why it's difficult to attend live performances that are far away. 
    BU: When it’s far away, expenses add up besides just the ticket cost. 
    CX: It's true. It's too painful to spend a lot of money only to find out that the artist isn't there. 
    BU: Indeed. That is tough. Let's enjoy the festival itself. 
    CX: That's right. At a festival, you can enjoy artists other than your favorites as well. 
    BU: Yes. It was fun. Thank you very much!
    """

    personality_traits = """
    'Openness': 5.083333492279053
    CX are quite open-minded and enjoy exploring new ideas, experiences, and perspectives. This trait makes CX creative and imaginative, often seeking novelty and variety in CX life. In relationships, CX appreciate deep, meaningful conversations and are often seen as intellectually stimulating. CX work habits may involve thinking outside the box and finding innovative solutions. Decision-making for CX likely involves considering multiple viewpoints and being willing to take risks for the sake of growth and learning.
    'Conscientiousness': 4.083333492279053
    CX possess a moderate level of conscientiousness, indicating that CX are reliable and responsible but also balanced in CX approach to tasks and responsibilities. CX can be organized and thorough when needed, yet CX also know when to relax and take things as they come. In relationships, CX are dependable and can be trusted to follow through on commitments. CX work habits show a good balance between diligence and flexibility, allowing CX to adapt to different situations. CX decision-making process is generally careful, though CX are not overly rigid.
    'Extraversion': 5.0
    CX are fairly extraverted, enjoying social interactions and being energized by spending time with others. CX are likely outgoing, friendly, and comfortable in group settings. In relationships, CX thrive on social connection and tend to be the life of the party, bringing enthusiasm and energy to CX interactions. At work, CX work well in team settings and are often seen as approachable and communicative. CX decision-making can be quick and confident, often influenced by CX desire for engagement and collaboration with others.
    'Agreeableness': 4.916666507720947
    CX are generally warm, compassionate, and cooperative, valuing harmony in CX interactions. CX are empathetic and considerate, making CX a supportive and pleasant person to be around. In relationships, CX prioritize others' needs and strive to maintain positive connections. At work, CX are likely a team player who fosters a collaborative and amicable environment. CX decision-making process often involves considering the well-being of others and striving for outcomes that benefit everyone involved.
    'Neuroticism': 5.75
    CX experience a higher level of emotional sensitivity and are more prone to experiencing stress and anxiety. This trait means that CX may often feel worried or overwhelmed, but it also means CX are in tune with your emotions and those of others. In relationships, CX sensitivity can make you deeply empathetic and understanding, though it might also lead to seeking reassurance. At work, CX might be detail-oriented and cautious, aiming to avoid mistakes. CX decision-making process may involve careful consideration of potential risks and outcomes, as CX aim to create a sense of security and stability for yourself.
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
    Here, CX and BU are their respective designations. Now I will provide you with CX's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with CX playing the role of the Human and BU playing the role of the Computer. Specifically, you need to transform CX's utterances based on CX's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BU's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, CX and BU are their respective designations. Now I will provide you with CX's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with CX playing the role of the Human and BU playing the role of the Computer. Specifically, you need to transform CX's utterances based on CX's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BU's utterances into a Computer style, also without altering the content and meaning.  

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

