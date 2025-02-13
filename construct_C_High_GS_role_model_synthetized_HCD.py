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
        Here, GS and CH are their respective designations. Now I will provide you with GS's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where GS simulates the role of a Human (converting GS's utterances in the original Human Human Dialogue), and CH simulates the role of a Computer (converting CH's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    GS: Hello. Nice to meet you. 
    CH: Hello, nice to meet you. 
    GS: Do you have any hobbies or special skills? 
    CH: Cooking and reading are my hobbies. Recently, I've been enjoying games as well. 
    GS: Cooking is nice, but I'm not very good at it. 
    CH: I enjoy making the things I want to eat. 
    GS: "Also, I heard you play games; specifically, what kind of games do you play?" 
    CH: I am currently playing a game called Elden Ring. I play it on my PC. 
    GS: I've heard of it. I also play games occasionally, but they are mostly simulations. 
    CH: I see, there are various types of simulations from city-building to strategy and combat.
    GS: That's right, I have played a city-building game called "Let's Go by A Train." 
    CH: "Is it the A-Train? I haven't played it, but I generally understand its content." 
    GS: Is that so? It's fun because you can make it quite faithfully according to the actual town. 
    CH: Nowadays, unlike the past, we calculate various factors, so it can be enjoyable no matter how many times you do it, right? 
    GS: That's right, in the past, there were quite a few simple things. 
    CH: "Yes. Still, I was having fun playing back then." 
    GS: By the way, do you know a simulator game called Train Simulator GO!? 
    CH: "I know. My friend even bought a dedicated controller, so I got to play it." 
    GS: Is that so? I played so much that I even considered buying a dedicated controller. 
    CH: At first, I splendidly overran and made the passengers fall. 
    GS: The G-sensor deducts quite a bit, so it's tough to apply the brakes correctly, isn't it? 
    CH: Yes, that’s right. Stopping in a way that takes the long inertia into account was difficult. 
    GS: There are people who stop exactly at 0cm on YouTube, which is amazing, isn't it? 
    CH: "It's interesting to watch things like that, isn't it? Like when you let an old man who used to be a professional do it, and he was super good at it." 
    GS: Certainly, I'd like to see that. I've heard that Shinkansen drivers have particularly advanced skills. 
    CH: Recently, VR has advanced, so train and flight simulations might be even more interesting with VR. 
    GS: I haven't played many flight games, but I think I would like to try them someday. 
    CH: I am more into combat aircraft than flights, but I used to play those kinds of games quite a lot. 
    GS: "Is it a fighter jet game? I used to play it occasionally too."
    CH: I see. The control system might be the most enjoyable aspect of the game's evolution.
    """

    sample_2_human_human_dialogue = """
    GS: Hello. Nice to meet you. 
    CH: Hello, nice to meet you. 
    GS: I travel quite a lot as a hobby; do you often go on trips? 
    CH: "I don't travel more than most people, but I do go on trips occasionally. Have you been anywhere recently?" 
    GS: Yes, in August, I went to Tokyo and Yokohama. 
    CH: It's an urban area, isn't it? Tokyo is a city, but it also has many temples and shrines. 
    GS: I like to see beautiful night views, so I went to the city with my friend. We didn't really see many temples or shrines. 
    CH: I see. So, you viewed the night scenery from a tall building, right? 
    GS: Yes, I have booked all the hotel rooms on the 30th floor or higher. 
    CH: Oh, you are thorough. Speaking of tall things, I lived in a place where I could see the Sky Tree during its construction. 
    GS: Did you live in Tokyo? I'm a bit envious because I'm from the countryside. 
    CH: After it was completed, I thought I could go anytime, but I ended up moving in the meantime. 
    GS: So, have you never been to the Skytree? 
    CH: I see. No, I didn't go inside to the observatory. I watched it from the outside the whole time. 
    GS: I see. You should go at least once. The elevator is also faster than anything I've ever experienced. 
    CH: The elevators in skyscrapers are amazing, aren't they? 
    GS: Do you know Yokohama Landmark Tower? Apparently, the descending elevator is the fastest in the world. 
    CH: The elevator at Landmark Tower is really impressive. No matter how many times I ride it, it always feels fast. 
    GS: Actually, when I went on a trip in August and rode it for the first time, I was really surprised. 
    CH: "The elevator is more of a landmark than the building itself." 
    GS: Certainly, that's true. Have you ever stayed at the Royal Park Hotel inside? 
    CH: "I have never stayed there. Did you stay there during your trip?" 
    GS: Yes, I stayed there this time, and since the guest rooms are on the 52nd floor and above, it felt like staying at the observation deck. CH: Aha, that sounds nice. I'd love to look at it while having a drink. 
    GS: Moreover, the price is quite reasonable, you can stay for about 8000 yen per person without meals. 
    CH: Oh, it's unexpectedly cheap. Could it be because the number of customers is decreasing? 
    GS: I don't think that's the case, when I went there, there were an incredible number of people even though it was a weekday. 
    CH: I see, if it's bustling then that's great. The tourism industry has been going through a tough time these past couple of years. 
    GS: "Yes, it's hard to hear the news that the inn we stayed at before is closing." 
    CH: Indeed. I want to return to previous levels soon.
    """

    personality_traits = """
    'Openness': 4.833333492279053
    GS are relatively open to new experiences and ideas. GS have a good balance of creativity and practicality, enjoying novelty but also appreciating routine. This balance helps GS adapt well to change while maintaining stability. In relationships, GS are open-minded and receptive to different perspectives, enriching GS interactions. At work, GS can think innovatively but also stay grounded in realistic solutions, making GS versatile in problem-solving.
    'Conscientiousness': 5.083333492279053
    GS are quite conscientious, demonstrating a strong sense of responsibility and organization. GS tend to be reliable, diligent, and goal-oriented, which often leads to high productivity and success in GS endeavors. In relationships, GS dependability makes GS a trusted friend and partner. GS work habits are disciplined and structured, enabling GS to manage tasks efficiently and meet deadlines consistently. GS decision-making process is careful and well-considered, minimizing impulsive actions.
    'Extraversion': 4.416666507720947
    GS exhibit moderate extraversion, enjoying social interactions and being around others, but also valuing GS alone time. GS strike a good balance between being sociable and introspective, making GS adaptable in various social settings. In relationships, GS can be engaging and energetic but also respect the need for personal space. At work, GS can collaborate effectively with colleagues while also being comfortable working independently. GS decision-making can be influenced by both external input and internal reflection.
    'Agreeableness': 4.583333492279053
    GS are fairly agreeable, showing kindness, empathy, and a cooperative nature. GS tend to be considerate and understanding in GS interactions, fostering harmonious relationships. GS compassion and ability to get along with others make GS a valuable team player and supportive friend. At work, GS are likely to prioritize collaboration and conflict resolution, contributing to a positive work environment. GS decision-making often takes into account the well-being of others, aiming for outcomes that benefit everyone involved.
    'Neuroticism': 5.583333492279053
    GS have a higher level of neuroticism, which means GS may experience emotional fluctuations and stress more intensely. GS might be more sensitive to negative emotions and prone to anxiety. In relationships, GS may need reassurance and support from GS close ones to feel secure. At work, stress management techniques and a stable environment can help GS maintain GS well-being. GS decision-making may be influenced by emotional factors, so it's beneficial to practice mindfulness and seek balance to mitigate the impact of stress.
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
    Here, GS and CH are their respective designations. Now I will provide you with GS's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with GS playing the role of the Human and CH playing the role of the Computer. Specifically, you need to transform GS's utterances based on GS's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CH's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, GS and CH are their respective designations. Now I will provide you with GS's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with GS playing the role of the Human and CH playing the role of the Computer. Specifically, you need to transform GS's utterances based on GS's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CH's utterances into a Computer style, also without altering the content and meaning.  

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

