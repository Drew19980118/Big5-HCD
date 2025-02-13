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
        Here, GV and GL are their respective designations. Now I will provide you with GV's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where GV simulates the role of a Human (converting GV's utterances in the original Human Human Dialogue), and GL simulates the role of a Computer (converting GL's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    GV: Hello. Nice to meet you. 
    GL: Hello, nice to meet you too! 
    GV: Are you doing any part-time job? 
    GL: I'm not doing anything special right now! My main work is short-term part-time jobs, so are you doing any part-time jobs? 
    GV: I can't write in detail, but right now I'm working in customer service. I'm not a host or anything like that. 
    GL: I see. I have also experienced working in customer service in the past! 
    GV: You could say short-term, I also did some one-off part-time jobs! I still do them occasionally now. 
    GL: I see. Which do you prefer, short-term or long-term part-time jobs? Does it depend on the content? 
    GV: I think single-day jobs are generally better. The pay is relatively good, and if you don't like the place, you can quit after one day. 
    GL: "That's right. I think both relationships and money are better on a one-time basis! Where are you registered?" 
    GV: I can't mention the name here, but it's in a pretty famous place! 
    GL: I see! I'm sorry for bringing up something so personal. There are pros and cons depending on the location, aren't there! 
    GV: That's right. It really varies from bad to good. 
    GL: What type of part-time job do you prefer, working (tasks) or customer service? 
    GV: "Is it work? Actually, I'm not very good at customer service." 
    GL: I understand. I also prefer doing the work, but I feel there are more job listings for customer service. 
    GV: I think it's a good idea to improve your communication skills through customer service work in preparation for future job hunting. 
    GL: That's right. Human relationships are important, aren't they? People have likes and dislikes, but we can't afford to be leisurely about it, can we? 
    GV: When you join a company, you can't choose who you interact with. I'm not in a position to speak authoritatively, though. 
    GL: No, no, that's right. It's difficult because we have to interact with people at the very least. 
    GV: Which industry are you considering for employment? 
    GL: At the moment, it's in the medical field! 
    GV: "That's cool! Does that mean university lasts for six years?" 
    GL: That's right. Since you need to attend for 6 years to be qualified! 
    GV: "Medical school? I've heard that the studies are incredibly tough. Good luck!" 
    GL: No, no, it's not that grand! Medical school is cool. I used to aim for it before! 
    GV: "So, does that mean pharmacy or nursing?" 
    GL: That kind of thing! GV: I hope COVID-19 has subsided by the time we graduate. 
    GL: Yes, I would be happy if it improves even a little!
    """

    sample_2_human_human_dialogue = """
    GV: Hello! What kind of hobbies do you have? 
    GL: I don't particularly have any hobbies, but if I had to say, it would be swimming. 
    GV: I also go swimming at the municipal pool sometimes! 
    GL: Really? I also occasionally go swimming at the community gym! Did you do swimming? 
    GV: I used to attend a swimming class when I was in elementary school. 
    GL: I see. I haven't been exercising much lately, and I thought I should move my body once in a while... 
    GV: I originally didn't exercise at all, but recently I've been going to the gym to lose weight!
    GL: I see! How many times a week do you go to the gym? 
    GV: About 5 times a week. On days when I don't have plans, I usually go without fail. 
    GL: Eh, you go there a lot! That's amazing! 
    GV: "I have already finished job hunting and earned all my credits, so I have a lot of free time now." 
    GL: I see. So, you have time now! What are you doing at the gym? 
    GV: The main equipment is a bicycle machine. I ride about 20km a day and burn around 300kcal. 
    GL: Bikes are nice. I like them too! Oh, that's quite amazing! 
    GV: It is said that 300 kcal is a rough guideline, so I follow that. I also do some strength training. 
    GL: I see! What kind of strength training do you do? 
    GV: I don't understand the terms, but I'm doing things like pulling weights down with my hands. 
    GL: Oh, I've seen that! It looks pretty intense!
    GV: You can adjust the weight yourself there, so there is no problem! 
    GL: I see! I'm currently going to a kickboxing gym! 
    GV: I see! Is it like kicking a sandbag with your foot? 
    GL: Sure! That menu is available too, but face-to-face interactions are more common, right? 
    GV: That's amazing! It seems a bit scary for me, and I don't think I could easily try it. 
    GL: No, no, I'm not good at sports at all and I'm not strong in fights, and I don't get into them! 
    GV: The best thing is not to fight. I also basically never do. 
    GL: Yes! I still want to get stronger, so I'm going to a gym that a friend of mine goes to! 
    GV: I have similar motivations, and after joining the company, I didn't want to be underestimated by those around me, so I've been working hard on strength training! 
    GL: I see. It's true that if you're muscular, you're less likely to be underestimated! 
    GV: I think it's quite an important element after all. 
    GL: Let's work hard on strength training together!
    """

    personality_traits = """
    'Openness': 3.5
    GV are moderately open to new experiences and ideas. GV enjoy creativity and thinking outside the box but may also appreciate some structure and routine in GV life. In relationships, GV can balance novelty with stability, making GV adaptable yet dependable. At work, GV are open to new methods and improvements but might also rely on proven techniques.
    'Conscientiousness': 2.8333332538604736
    GV exhibit low to moderate conscientiousness, indicating a laid-back and flexible approach to tasks and deadlines. GV may struggle with organization and time management but can also be more spontaneous and adaptable. In relationships and work, GV might prefer a more relaxed and less structured environment, which allows GV to be versatile and handle unexpected changes.
    'Extraversion': 2.1666667461395264
    GV are relatively introverted, finding comfort in solitude and intimate gatherings rather than large social settings. GV recharge through alone time and deep, meaningful conversations. In relationships, GV value quality over quantity, fostering strong bonds with a few close individuals. At work, GV may excel in roles that require focus and independence, avoiding highly stimulating environments.
    'Agreeableness': 4.583333492279053
    GV are quite agreeable, showing a genuine concern for others and a tendency to be cooperative and harmonious in GV interactions. GV prioritize empathy and compassion, making GV a trusted and supportive friend or colleague. In both personal and professional settings, GV tend to avoid conflict and strive for consensus, often placing others' needs above GV own.
    'Neuroticism': 6.166666507720947
    GV have a high level of neuroticism, which means GV are more prone to experiencing anxiety, mood swings, and stress. GV may often find yourself worrying about various aspects of life and can be sensitive to criticism. This heightened emotional reactivity can impact GV relationships and work, sometimes causing GV to feel overwhelmed. However, this trait also means GV are deeply in touch with GV emotions and highly empathetic towards others' feelings.
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
    Here, GV and GL are their respective designations. Now I will provide you with GV's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with GV playing the role of the Human and GL playing the role of the Computer. Specifically, you need to transform GV's utterances based on GV's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform GL's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, GV and GL are their respective designations. Now I will provide you with GV's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with GV playing the role of the Human and GL playing the role of the Computer. Specifically, you need to transform GV's utterances based on GV's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform GL's utterances into a Computer style, also without altering the content and meaning.  

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