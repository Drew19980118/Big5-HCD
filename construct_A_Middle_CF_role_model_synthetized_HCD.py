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
        Here, CF and BW are their respective designations. Now I will provide you with CF's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where CF simulates the role of a Human (converting CF's utterances in the original Human Human Dialogue), and BW simulates the role of a Computer (converting BW's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    CF: Good evening. The rain is intense, isn't it? How is it over there? 
    BW: Good evening! It doesn't seem to be raining right now. 
    CF: I see! It's raining heavily here right now. 
    BW: I see, it does vary depending on the location after all. A typhoon is coming, right? 
    CF: That's right. I was thinking of going to the convenience store, but I gave up. 
    BW: I see, it doesn't look like it'll stop soon like a sudden shower. 
    CF: It seems like it will rain harder than a sudden shower, but it is expected to be sunny tomorrow. 
    BW: It will stop soon, I heard that Tohoku and Hokkaido might be in trouble. 
    CF: It's Tokyo here, and it looks like the rain will stop by midnight. The convenience store might open in the morning. 
    BW: I see, I hope it passes quickly. 
    CF: "Yes. I'm thinking of going out tomorrow." 
    BW: That makes it even more surprising, especially since it often rains suddenly even in summer recently. 
    CF: Thunder often rumbles and strikes quite a bit, doesn't it? I'm worried about electrical appliances when it thunders. 
    BW: "Has it fallen? Yes, it seems like the electrical appliances are not working well." 
    CF: I am worried because on the day after a lightning strike in the past, the computers at my workplace stopped working. 
    BW: "Did that really happen? It would make it impossible to work. And there's no way to be careful about it either." 
    CF: That's right. The work that day was hopeless. 
    BW: That must have been tough; I hope you get to go home. 
    CF: I couldn't go home that day, but on another day when a typhoon came, I was told to go home, and I ended up going to see a movie. BW: Certainly, when a typhoon comes, we can go home early. Did you go to the movies? That's nice. 
    CF: It was quite a while ago. There were only about three people, so it was comfortable! 
    BW: The movie theater on weekdays looks comfortable! That's when I want to go to the movies. 
    CF: You want to watch quietly, right? Do you often go to the movie theater? 
    BW: Recently, I haven't been able to go at all, but I love watching movies in the theater. How about you? 
    CF: I also like watching movies in the theater. I especially like the early morning or late night shows. 
    BW: Ah, that's nice, it doesn't seem too crowded, so it looks like we can watch comfortably. 
    CF: That's right. I'm going to watch Pokémon at the movie theater for the first time in a while, probably around the week after next. 
    BW: "Pokemon is on right now! Do you go during less crowded hours?" 
    CF: It seems there is a revival screening of old Pokémon, so I'm taking the kids. We'll go in the evening! 
    BW: I see, please have a great time! 
    CF: Thank you very much!
    """

    sample_2_human_human_dialogue = """
    CF: Good evening! 
    BW: Good evening, please take care of me! 
    CF: "Likewise, thank you. Are you going to visit the grave during Obon?" 
    BW: Yes, I plan to go on the 15th. Are you going? 
    CF: I am not going. One reason is that many people around me have contracted COVID. 
    BW: I see, I live in the neighborhood. 
    CF: It's close and easy to get to. 
    BW: That's right, it becomes difficult if you have to go on a long trip. 
    CF: I heard that an acquaintance who had returned to their hometown also got COVID-19 today, and I thought that it is indeed spreading. 
    BW: The fact that it’s widespread means that anyone can get the disease, right? 
    CF: I see. This lifestyle has been going on for a long time, so I hope it ends soon. 
    BW: It seems that only Japan is continuing, while abroad people seem to be living as if it never happened. 
    CF: I'm a little envious. Are you interested in traveling abroad? 
    BW: Yes, I like going abroad, so I want to visit various places. Do you like it too? 
    CF: Actually, I don't have any experience abroad, but I want to go. 
    BW: I've only been to China, but I've always dreamed about it. 
    CF: Oh! China, huh. How is it? 
    BW: "It was quite a long time ago, but it was a bit different from Japan and interesting." 
    CF: I see. Since I love eating, I'm interested in the food situation. 
    BW: If it's a proper place, it's fine, but it's better to avoid shabby stores on street corners. 
    CF: I see, that's how it is. The people over there are strong. 
    BW: Yes, Japanese people are considerate, but people over there are strong in various ways. 
    CF: It's a forward-thinking idea and a sensibility that Japanese people don't have. I respect that aspect. 
    BW: That's right, if Japanese people can remain humble while becoming assertive, they would be unbeatable. 
    CF: That's right! Japanese people have good qualities. 
    BW: There are also many foreigners who like Japan. 
    CF: I understand. Before COVID-19, there was a lot of bustling tourism. 
    BW: I see, it seems to be avoided now because the regulations are too strict, it's sad. 
    CF: I hope Japan returns to how it was before COVID-19. Thank you for the conversation! 
    BW: "Thank you very much!"
    """

    personality_traits = """
    'Openness': 4.333333492279053
    CF are moderately open to new experiences and ideas. CF appreciate creativity and enjoy exploring different perspectives, but CF also value tradition and practicality. This balance allows CF to be innovative while still considering realistic constraints. In relationships, CF are open-minded and willing to try new things, but CF may prefer a certain level of stability. At work, CF can adapt to change but also understand the importance of proven methods.
    'Conscientiousness': 3.3333332538604736
    CF have an average level of conscientiousness, meaning CF are somewhat reliable and organized but may struggle with consistency. CF can be diligent and responsible when motivated, but may also be prone to procrastination. In CF relationships, CF are dependable, but sometimes might not follow through on all commitments. At work, CF perform well when engaged but may need external structure to maintain focus and productivity.
    'Extraversion': 3.4166667461395264
    CF exhibit moderate extraversion, enjoying social interaction and group activities, but also valuing CF alone time. CF can be outgoing and energetic in social settings but appreciate moments of solitude to recharge. In relationships, CF balance sociability with introspection, making CF approachable yet self-sufficient. At work, CF thrive in collaborative environments but can also work independently when necessary.
    'Agreeableness': 4.083333492279053
    CF are fairly agreeable, meaning CF are compassionate, cooperative, and good-natured. CF value harmony and are often considerate of others' feelings. In CF relationships, CF are empathetic and tend to avoid conflict, fostering a supportive and understanding environment. At work, CF collaborative nature makes CF a valuable team member, though CF may sometimes prioritize others' needs over CF own.
    'Neuroticism': 5.833333492279053
    CF have a high level of neuroticism, indicating a tendency towards emotional sensitivity and experiencing stress or anxiety. CF may often feel worried or insecure and have strong emotional reactions. In relationships, CF might require more reassurance and support from CF partners. At work, CF could be highly conscientious about performance but may struggle with stress management. Developing coping strategies and seeking supportive environments can be beneficial.
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
    Here, CF and BW are their respective designations. Now I will provide you with CF's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with CF playing the role of the Human and BW playing the role of the Computer. Specifically, you need to transform CF's utterances based on CF's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BW's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, CF and BW are their respective designations. Now I will provide you with CF's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with CF playing the role of the Human and BW playing the role of the Computer. Specifically, you need to transform CF's utterances based on CF's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BW's utterances into a Computer style, also without altering the content and meaning.  

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