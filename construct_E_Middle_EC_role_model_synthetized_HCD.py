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
        Here, EC and DG are their respective designations. Now I will provide you with EC's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where EC simulates the role of a Human (converting EC's utterances in the original Human Human Dialogue), and DG simulates the role of a Computer (converting DG's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    EC: Good evening, thank you! 
    DG: Good evening, please. 
    EC: Did you go anywhere during the summer vacation? 
    DG: I will go out this weekend, but I will stay home otherwise. 
    EC: "My family is also staying indoors. Where are you planning to go this weekend?" 
    DG: "That's right. I'm participating in a music festival this weekend." 
    EC: "Festivals! I have never participated in one before! What is it like?" 
    DG: It's my first time being outdoors as well, but you can freely move around four different stages!
    EC: Outdoor festivals are so appealing! Is it like enjoying music by going around to various stages? 
    DG: I think there will also be festival food stalls! I'm looking forward to it! 
    EC: "Festival food is a new term to me! Looks delicious!!" 
    DG: "There are a lot of hearty dishes like meat bowls!" 
    EC: It's so appealing! With four stages and festival food, is one day enough? 
    DG: I have only secured a one-day ticket, but there are people going for both days! 
    EC: I see! Do you plan how you will go around, or do you go with the flow? 
    DG: I have made plans, but I am prepared for emergencies where I won't be able to go out due to COVID-19. 
    EC: "It would be extremely disappointing if we can't go despite having made such careful plans." 
    DG: That's right, but I'm also looking forward to meeting unknown artists without being bound by the schedule! 
    EC: Exploring new things is great! What kind of artists do you like? 
    DG: I often listen to King Gnu these days. 
    EC: "I have an image of a very beautiful voice!" 
    DG: I like that vocalist because they are charming. There is a gap. 
    EC: "I don't know what their face looks like! There's a gap, huh! I'll search for it next time." 
    DG: He's definitely a mysterious guy who's troubled by not being able to tidy up his own room. 
    EC: Mysterious guy! You have a unique personality. I'm intrigued! 
    DG: Yes, that's right, so I was doing an Instagram live about how I can't get married. 
    EC: I see. It seems like a lot of sisterly types who are totally okay with it would volunteer. 
    DG: "Indeed! But it's 3 AM, haha. Such an interesting personality!" 
    EC: "That's true! It's fascinating! Thank you for teaching me various things." 
    DG: No, no, I made you listen!
    """

    sample_2_human_human_dialogue = """
    EC: Hello, nice to meet you. 
    DG: Likewise, please take care of me! 
    EC: "Recently, is there anything you bought that you're glad you did? Something like, why didn't I buy this sooner?" 
    DG: Oh, I properly went back to using my own toothbrush. The angle might be a bit different though! 
    EC: Did you use an electric one before? 
    DG: Yes, I bought it because I admired it, but it didn't feel quite right, so I changed it! 
    EC: The commercial makes it seem like electric ones remove dirt really well, but they don't actually feel that refreshing. 
    DG: I feel like it's hard to polish the back and inside areas. 
    EC: I see! I was surprised because I thought it would be easy to polish. 
    DG: "Also, if it doesn't work out, you can still use it for cleaning." 
    EC: It's convenient, isn't it? I think one of the good points of manual toothbrushes is that they are cheap, so you can easily replace them if they get frayed. 
    DG: That's right, and with electric ones, you need to charge them and maintain them when they get dirty, so it wasn't an ideal situation. EC: Wow, that's a hassle. I don't want to deal with maintenance and such. It's far from an ideal world. 
    DG: "Somehow my laziness is gradually being revealed, but I just want to take it easy as much as possible!" 
    EC: I am also lazy, so I totally understand! You don't want to spend time taking care of your teeth, right? 
    DG: I see. <EC>, is there something you are glad you bought? 
    EC: The mouse with a button on the left thumb was convenient. I think most people are using it. 
    DG: "Huh, a button? I might not have one." 
    EC: It is called a 5-button mouse. 
    DG: "Heh! That's news to me! So it's not specifically for gaming?" 
    EC: That's not correct! It's around 1200 yen, so I think regular people are using it! 
    DG: When I looked it up just now, I found out you can also go back and forward with it. 
    EC: That's right, that's what's convenient about it. You don't have to go out of your way to move the cursor. 
    DG: "Eh! I updated my wish list!" 
    EC: Absolutely! If it's the same price, I definitely recommend the five-button one. 
    DG: I ended up talking about things I hadn't bought! 
    EC: No, no, I'm glad I got to hear it! I was interested in electric toothbrushes!
    DG: Everyone is different, but convenience might be inconvenient! 
    EC: "That's true! It was fun, thank you very much." 
    DG: "It is I who should be thanking you for the mouse information! Thank you very much."
    """

    personality_traits = """
    'Openness': 3.5
    EC are moderately open to new experiences and ideas. EC appreciate creativity and new perspectives but also value tradition and routine. In relationships, EC balance novelty with familiarity, and at work, EC can adapt to new situations while maintaining consistent performance. EC decision-making includes both innovative and practical considerations.
    'Conscientiousness': 4.416666507720947
    EC are quite organized and dependable, though EC still allow for some flexibility. EC manage EC responsibilities effectively and are reliable in EC commitments. In relationships, EC are seen as responsible and trustworthy. At work, EC are diligent and goal-oriented, which aids in achieving consistent results. EC decision-making process is systematic but can accommodate unforeseen circumstances.
    'Extraversion': 3.5833332538604736
    EC are moderately outgoing and sociable. While EC enjoy being around others and engaging in social activities, EC also value EC alone time. In relationships, EC are approachable and communicative but not overly reliant on social interaction. At work, EC can collaborate well in teams and also work independently. EC decision-making process benefits from both external input and personal reflection.
    'Agreeableness': 3.75
    EC tend to be cooperative and considerate, balancing EC own needs with those of others. EC get along well with people, valuing harmony in relationships while maintaining EC own viewpoint. At work, EC are a team player and can navigate interpersonal dynamics effectively. EC decision-making considers both EC interests and the well-being of others, striving for mutually beneficial outcomes.
    'Neuroticism': 6.666666507720947
    EC experience high levels of emotional intensity and may be more prone to stress and anxiety. This heightened sensitivity can make EC highly empathetic and in tune with EC own and others' emotions. In relationships, EC may require reassurance and support from loved ones. At work, stress management strategies are crucial for maintaining productivity. EC decision-making might be influenced by emotional fluctuations, emphasizing the need for coping mechanisms to ensure balanced judgments.
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
    Here, EC and DG are their respective designations. Now I will provide you with EC's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with EC playing the role of the Human and DG playing the role of the Computer. Specifically, you need to transform EC's utterances based on EC's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform DG's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, EC and DG are their respective designations. Now I will provide you with EC's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with EC playing the role of the Human and DG playing the role of the Computer. Specifically, you need to transform EC's utterances based on EC's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform DG's utterances into a Computer style, also without altering the content and meaning.  

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