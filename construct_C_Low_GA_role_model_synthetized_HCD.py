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
        Here, GA and CB are their respective designations. Now I will provide you with GA's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where GA simulates the role of a Human (converting GA's utterances in the original Human Human Dialogue), and CB simulates the role of a Computer (converting CB's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    GA: Good evening. 
    CB: Good evening. 
    GA: Have you already eaten dinner? 
    CB: Yes, I ate! It was something simple like fried rice though. 
    GA: "Fried rice looks good! Did you make it from scratch?" 
    CB: There was quite a lot of leftover rice, so I used it to make this. 
    GA: I see. We had vegetables, fish cooked in miso, and avocado. 
    CB: How was the avocado eaten? 
    GA: Dip it in soy sauce and eat it! Delicious! 
    CB: "It's delicious, isn't it! Isn't it difficult to choose when buying? The degree of damage." 
    GA: I live with my parents, and my mother cooks for us, but this dish comes up quite often on the menu. It happens so frequently that I didn't realize it. 
    CB: I see. It's nutritious too! It's a well-balanced menu. 
    GA: Maybe they're not considering balance. And they're not very conscious of it. But it's super delicious every day. 
    CB: "That’s great! Your mother is a good cook, isn’t she? Do you have a favorite dish?" 
    GA: I've never heard of it... I don't really seem to like cooking that much. There are days when I just get prepared dishes from the supermarket. But just having meals prepared for me is enough. 
    CB: Yes, that's right. I have trouble with the menu because if I don't make it myself, no one else will. 
    GA: I think that if I were to live alone, I definitely wouldn't cook for myself, and since I'm lazy, I'd probably skip meals without a second thought. 
    CB: When you're alone, there are times like that, aren't there? My kids are at home now because their classes have been closed. 
    GA: If you have children, it seems like it would be tough... When I was a child, my mother often asked me what I wanted on the menu. 
    CB: Our family generally asks, but my brother and sister often choose different menus. 
    GA: But you are allowed to give your opinion, right? I always said anything was fine or ordered curry rice, so it seemed troublesome to my parents. 
    CB: I might have been like that too. 
    GA: "That's right. There are so many things that I don't know what to say."
    CB: "It's amazing that so many menu ideas come to mind. Do you eat at home for all three meals?" 
    GA: Mostly just dinner. 
    CB: Are you at work or school during the day? 
    GA: It's work. 
    CB: Was work today? 
    GA: "Yes, I'm tired." 
    CB: Good work! I was working too, so now I'm taking a break.
    """

    sample_2_human_human_dialogue = """
    GA: Please! 
    CB: Thank you in advance. 
    GA: What kind of music do you usually listen to? 
    CB: Yorushika, Humbert Humbert, Yoasobi, and various others. 
    GA: "I've only just heard of Humbert Humbert! Are they a recent artist?" 
    CB: "Not recently. It's often played in commercial songs too!" 
    GA: Is it the pattern that I am listening to it unconsciously! Can you tell me the title? 
    CB: "Misawa Home or something?" 
    GA: "That's true! I just looked it up and I've heard of it before." 
    CB: Is that so? I'm happy. 
    GA: I used to listen to Yorushika and YOASOBI a lot. Maybe not so much recently. 
    CB: "I'm not always listening to music, but I listen to female vocalists the most. What do you listen to?" 
    GA: Recently, I've been listening to nothing but songs from the unit called DIALOGUE+. 
    CB: I heard it for the first time! 
    GA: "It seems to be an idol group of new voice actors. Their recognition might still be low." 
    CB: I just searched on Amazon Music. 
    GA: The song itself is really good because it's produced by Tabuchi-san from UNISON SQUARE GARDEN. 
    CB: I see. I'm listening to it now, and it has a nice pop feel to it. 
    GA: Basically, it's pop. Sometimes it changes to a cooler vibe or the atmosphere changes dramatically. 
    CB: I see. Do you also go to concerts and such? 
    GA: I went there for the first time the day before yesterday! 
    CB: Oh, that's hot. How was it? 
    GA: The seats were close, so I felt a great sense of satisfaction. They were cute and cool, and the lingering effect is still strong. 
    CB: Sounds good. It's exciting to go in person. 
    GA: I like live band performances, and since it was a venue with a capacity of 1000 people, the impact was incredible! 
    CB: So it was a box that could hold that much! 
    GA: "The venue didn't seem like a live house, did it? Even so, since they are still new, I think it was still relatively small." 
    CB: "Even though you're new, it's impressive that you can gather so many people. You're popular, aren't you?" 
    GA: I think it’s only been about 2 or 3 years since their debut, but I feel like they’re putting a lot of effort into it. 
    CB: Thank you for teaching me because I don't know much about idols!
    """

    personality_traits = """
    'Openness': 2.75
    GA tend to prefer routine and familiarity over new experiences. This may mean GA are more practical and grounded but might be less open to change or unconventional ideas. In relationships and work, GA value stability and may sometimes be seen as resistant to trying new approaches.
    'Conscientiousness': 1.92 
    GA might struggle with organization and long-term planning. This could make it challenging to meet deadlines and maintain structured habits. In GA career, GA may find it difficult to stay on task, and in personal life, GA might lean towards spontaneity over predictability.
    'Extraversion': 3.17 
    GA exhibit a balanced approach to socializing. GA enjoy company but also value GA alone time. This moderate level of extraversion means GA can adapt well to social situations and solitary tasks, making GA flexible in both work and personal relationships.
    'Agreeableness': 5.25 
    GA are very cooperative and compassionate towards others, often putting their needs above GA own. This trait helps GA build strong, trusting relationships. However, it might also lead to situations where GA compromise too much or struggle to assert GA.
    'Neuroticism': 4.92 
    GA experience a high level of emotional sensitivity and may often feel anxious or stressed. This can affect GA decision-making and relationships, as GA might worry about potential problems. It’s important to find healthy coping mechanisms to manage stress effectively.
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
    Here, GA and CB are their respective designations. Now I will provide you with GA's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with GA playing the role of the Human and CB playing the role of the Computer. Specifically, you need to transform GA's utterances based on GA's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CB's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, GA and CB are their respective designations. Now I will provide you with GA's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with GA playing the role of the Human and CB playing the role of the Computer. Specifically, you need to transform GA's utterances based on GA's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CB's utterances into a Computer style, also without altering the content and meaning.  

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

