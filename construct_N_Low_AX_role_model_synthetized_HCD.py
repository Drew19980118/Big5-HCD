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
        Here, AX and AN are their respective designations. Now I will provide you with AX's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where AX simulates the role of a Human (converting AX's utterances in the original Human Human Dialogue), and AN simulates the role of a Computer (converting AN's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    AX: Good evening. I look forward to working with you. 
    AN: Good evening. Likewise, thank you in advance. 
    AX: The hot days continue, but are you doing well? 
    AN: Yes, fortunately, I've been healthy and doing well. Are you okay? 
    AX: For now, I'm okay. Thank you. The weather can be severe in some regions, can't it? 
    AN: Yes, there were regions that seemed to be having a hard time with the continuous heavy rain. 
    AX: I currently live in Kansai, and the rain was quite heavy on Saturday. 
    AN: Oh, I also live in Kansai. The rain wasn't that bad here. 
    AX: I see. Are you okay with the heat or the cold? 
    AN: I am not good with either, but I might be worse with the heat. 
    AX: If you're okay with the air conditioner and such, it's fine, but are you able to use it well? 
    AN: That's because I have poor circulation, so I really dislike air conditioning. 
    AX: There are quite a few people like that, aren't there? Our workplace is also very cold. 
    AN: Is that so? Are you taking a jacket or something? 
    AX: Yes. Two well-built women lower the temperature, right? 
    AN: Oh no, that's troublesome. 
    AX: Well, I won't say anything, but I'll wear this. It's impossible and unpleasant to do the opposite. 
    AN: You are so kind! Don't you get swollen when your body gets too cold? 
    AX: Your shoulders and head can start to hurt, right? When you go outside, it feels warm. 
    AN: That's right. I feel like my blood circulation has gotten worse. 
    AX: Since I am from Hokkaido, I might not be quite used to the air conditioning. 
    AN: Are you from Hokkaido? They don't really use air conditioners there, right? 
    AX: I see. I don't know about recently, but the heat doesn't last long.
    AN: Is that so? Is winter extremely cold after all? 
    AX: No, no. Well, places like Asahikawa go down to minus 20 or 30.
    AN: Incredible. It's a temperature beyond my imagination. 
    AX: It's the one where you can hammer a nail with a banana. 
    AN: It's a scene you often see in manga. 
    AX: Haha. That might be true. The usual way to use a banana is different, after all. 
    AN: I imagined it for a moment and laughed. Well, it's time, so I'll take my leave around here.
    """

    sample_2_human_human_dialogue = """
    AX: Thank you for your hard work. 
    AN: Thank you for your hard work. 
    AX: When it's hot, I tend to want to eat something cold, how about you? 
    AN: Same here. I had ice cream after my bath today too. 
    AX: That's nice. I heard they are having an AI expo in Osaka now. 
    AN: "Could it be the department store in Tennoji?" 
    AX: Yes, indeed. As expected from a local. Have you been there already? 
    AN: "Not yet. Have you already gone?" 
    AX: No. It's just that my wife is at her part-time job. 
    AN: Is that so? It sounds like a fun part-time job!
    AX: "They said it looked interesting and went. It seems Horiemon was there." 
    AN: "Horie-mon! Were you here as a customer?" 
    AX: Apparently, they were introducing the shop for a live stream. 
    AN: I see. Actually, I have never been to the AI Expo. 
    AX: I came to Kansai with the coronavirus three years ago, and this is said to be the first time in three years as well. 
    AN: Is that so! I've always wanted to go there, so maybe I'll give it a try. 
    AX: "I heard it will be going on until next week. I secretly want to go, too." 
    AN: If it's until next week, I think I can make time. Are you going to go see how your wife is doing at work? 
    AX: I think it's better not to see it. I'll go when they're not there. 
    AN: I see. The kids will probably be happy if we take them along, so we will go together.
    AX: Certainly. Our youngest child is in the third year of junior high school, so it's a delicate situation. 
    AN: "It's a chance to go out under the pretext of being able to eat ice cream!" 
    AX: That's right. We need to somehow convince them and get there.
    AN: When they become a third-year middle school student, do they already have a rebellious phase? 
    AX: My rebellious phase was around the upper grades of elementary school. I've calmed down quite a bit. 
    AN: Oh my, our oldest child is 5 years old now, but I wonder if they will go through a rebellious phase someday too? 
    AX: It's currently the most active time, and it feels like I can't take my eyes off. 
    AN: Yes, it's become much calmer. The younger one is 2 years old, so I can't take my eyes off this one. 
    AX: At 2 years old, you don't even know where you're going, right? I think it must be tough. 
    AN: Let's both do our best with raising our children.
    """

    personality_traits = """
    'Openness': 5.333333492279053
    AX are highly open to new experiences and ideas, enjoying creativity and innovation. AX likely have a strong appreciation for art, are intellectually curious, and are willing to explore new things. This trait can make you adaptable in changing environments and open-minded in AX relationships, often seeking out diverse perspectives and experiences.
    'Conscientiousness': 6.333333492279053
    AX are very organized, reliable, and disciplined. AX strong sense of duty and high level of self-control means AX are likely very dependable in both personal and professional settings. This trait helps AX achieve AX goals through careful planning and persistence, and makes AX a trustworthy and responsible individual in AX relationships and work habits.
    'Extraversion': 6.25
    AX are highly sociable, outgoing, and energetic. AX thrive in social situations, enjoy being the center of attention, and likely have a wide circle of friends. This trait makes AX enthusiastic and lively, often bringing a positive energy to group settings and excelling in roles that require teamwork and communication.
    'Agreeableness': 6.25
    AX are very compassionate, cooperative, and considerate. AX place a high value on getting along with others, showing empathy and understanding in AX interactions. This trait makes AX a supportive and nurturing friend, partner, or colleague, often putting others' needs before AX own and creating harmonious relationships.
    'Neuroticism': 1.0833333730697632
    AX are emotionally stable, calm, and resilient. AX tend to stay composed under stress and do not easily succumb to negative emotions like anxiety or sadness. This trait contributes to AX overall mental well-being, enabling AX to handle life's challenges with confidence and maintain positive relationships without being overwhelmed by emotional turbulence.
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
    Here, AX and AN are their respective designations. Now I will provide you with AX's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with AX playing the role of the Human and AN playing the role of the Computer. Specifically, you need to transform AX's utterances based on AX's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AN's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, AX and AN are their respective designations. Now I will provide you with AX's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with AX playing the role of the Human and AN playing the role of the Computer. Specifically, you need to transform AX's utterances based on AX's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AN's utterances into a Computer style, also without altering the content and meaning.  

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