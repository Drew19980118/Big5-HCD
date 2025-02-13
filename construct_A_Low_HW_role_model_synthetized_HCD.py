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
        Here, HW and CA are their respective designations. Now I will provide you with HW's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where HW simulates the role of a Human (converting HW's utterances in the original Human Human Dialogue), and CA simulates the role of a Computer (converting CA's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    HW: Hello! 
    CA: Hello! 
    HW: It's hot again today, isn't it? 
    CA: It's really hot, isn't it? 
    HW: "It's hot, isn't it? Eating something cold is a relief." 
    CA: Sounds good! I'll eat a lot of ice cream. 
    HW: "Ice cream is delicious, isn't it? What flavor of ice cream do you like?" 
    CA: "Maybe vanilla~ How about you, Sukiyaki Cat?" 
    HW: I love matcha flavor! I always have matcha-flavored PALM in the refrigerator. 
    CA: Wow! Matcha ice cream is great! 
    HW: Yes! I like anything with matcha flavor. 
    CA: I haven't tried the matcha flavor of Palmo yet, so listening to this made me want to eat it. 
    HW: It's delicious, so I recommend it! The chocolate coating on the outside is thick and satisfying. 
    CA: I'll try eating it the next time I buy ice cream! 
    HW: Please try it! 
    CA: Speaking of ice, I went to eat shaved ice the other day and found an interesting one. 
    HW: What kind of shaved ice is it? I'm curious. 
    CA: It's tiramisu shaved ice. 
    HW: Wow! That looks delicious!! 
    CA: Before eating it, I wondered what it would be like, but after tasting it, it really had a solid tiramisu flavor. 
    HW: That's interesting! What did the shaved ice look like? 
    CA: It felt like there was cream on top, and cocoa sprinkled over it. 
    HW: At first glance, it looks Western! It seems like it would look great on Instagram and is lovely. 
    CA: It seems that customers come from outside the prefecture as well. 
    HW: "It has become a specialty, hasn't it? I would like to try it once." 
    CA: I thought shaved ice was the same everywhere, but when I went and saw it, I understood why people line up. 
    HW: Delicious things do indeed gain a reputation! 
    CA: It will be.
    HW: I will look up tiramisu shaved ice next time! Thank you very much. 
    CA: Absolutely! Thank you very much!
    """

    sample_2_human_human_dialogue = """
    HW: Hello! 
    CA: Hello! 
    HW: Do you usually sleep on a bed or a futon? 
    CA: I'm a futon person. How about you, <HW>? 
    HW: Recently, I switched from a bed to a bunk bed! 
    CA: Oh, nice! Why a bunk bed? 
    HW: My room is too small, so I bought a bunk bed that was on sale. 
    CA: I see! That's a clever way to use it! 
    HW: The bunk bed has storage underneath, so my room feels more spacious now! 
    CA: I'd love to learn more interior tips from you, <HW>! 
    HW: The advantage of beds and futons is that you can roll out of them easily. 
    CA: The rolling-out technique is the best! 
    HW: Exactly! With bunk beds or loft beds, you have to climb down every time, which is a hassle. 
    CA: That does add extra steps, doesn't it? 
    HW: If I had a futon or a regular bed, I wouldn't have been late so many times... 
    CA: Hahaha, you were just a few seconds away, huh? 
    HW: Exactly. Last night was a tropical night, and it was so hot near the ceiling. 
    CA: Oh right... Hot air rises. That must have been tough. 
    HW: Lately, the temperature doesn't drop even at night, right? 
    CA: Absolutely. It's impossible without air conditioning. 
    HW: Yes. I feel like air conditioning works better with futons or beds. Do you use air conditioning at night? 
    CA: I use it at night too. Even with the window open, it's still too hot. How about you, <HW>? 
    HW: I use it every night. But my bed is right under the air conditioner, so the cold air hits me directly. 
    CA: Wow, that's cool but also sounds uncomfortable in another way. 
    HW: Exactly. If I don't use it, it gets too hot, but if I turn it on, the cold air hits me directly. 
    CA: How about sleeping on the lower bunk? 
    HW: I'd like to, but the lower bunk is full of stuff, so I just wrap myself in a futon with the air conditioner on. 
    CA: Having stuff on the top bunk makes it unstable, right? 
    HW: I see! I hadn't thought of putting stuff on the top. Thanks for the great advice! 
    CA: I hope you can sleep well. Let's talk again! 
    HW: Yes, let's talk again soon!
    """

    personality_traits = """
    'Openness': 2.0
    HW tend to prefer routine and familiarity over novelty and variety. HW might not be very open to new experiences or unconventional ideas. This preference for the tried-and-true can make HW dependable and practical, but HW may sometimes struggle with adapting to change or thinking creatively. In relationships, HW might appreciate stability and clear boundaries. At work, HW likely excel in structured environments but may need encouragement to embrace innovation.
    'Conscientiousness': 1.0
    HW might find it challenging to stick to schedules and maintain organization. Spontaneity and flexibility could be more HW style, but this can sometimes lead to difficulties in meeting deadlines and achieving long-term goals. In relationships, HW relaxed approach can make HW easygoing and fun, but it may also frustrate more organized partners. At work, HW might thrive in roles that require adaptability rather than rigid planning.
    'Extraversion': 1.0
    HW are likely introverted and prefer solitary activities or spending time with a small, close-knit group of friends. Social interactions can be draining, and HW might need ample alone time to recharge. In relationships, HW value deep, meaningful connections over a large social circle. At work, HW might excel in tasks that require focus and independence, but collaborative projects may be more challenging for HW.
    'Agreeableness': 1.0
    HW might have a more competitive or skeptical nature and are less inclined to prioritize harmony over personal beliefs or goals. This trait can make HW strong-willed and decisive, but it might lead to conflicts or difficulties in compromising. In relationships, HW might be seen as assertive or blunt, which can sometimes cause friction. In a work setting, HW likely excel in roles that require critical thinking and decisiveness, though teamwork could be challenging.
    'Neuroticism': 7.0
    HW may experience high levels of emotional sensitivity and stress. Anxiety, worry, and mood swings could be common for HW. This heightened emotional response can make relationships challenging, as HW might be perceived as high-maintenance or easily upset. In HW professional life, managing stress and maintaining a calm demeanor might be difficult, potentially affecting HW performance. Finding effective coping strategies and supportive environments could be crucial for HW well-being.
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
    Here, HW and CA are their respective designations. Now I will provide you with HW's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with HW playing the role of the Human and CA playing the role of the Computer. Specifically, you need to transform HW's utterances based on HW's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CA's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, HW and CA are their respective designations. Now I will provide you with HW's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with HW playing the role of the Human and CA playing the role of the Computer. Specifically, you need to transform HW's utterances based on HW's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CA's utterances into a Computer style, also without altering the content and meaning.  

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