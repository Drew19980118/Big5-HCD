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
        Here, AH and AQ are their respective designations. Now I will provide you with AH's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where AH simulates the role of a Human (converting AH's utterances in the original Human Human Dialogue), and AQ simulates the role of a Computer (converting AQ's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    AH: Hello! 
    AQ: Hello. 
    AH: It was quite hot today. 
    AQ: It's hot, isn't it? Are you staying inside the house all the time? 
    AH: I was outside in the morning. 
    AQ: Are you shopping? 
    AH: No, it's a walk. 
    AQ: You're great for going on a walk! 
    AH: I haven't been exercising much lately. 
    AQ: Me too. 
    AH: I thought I could manage walking by myself, so I am doing it. 
    AQ: "That's amazing. It's outside, right?" 
    AH: Yes, it's outside! 
    AQ: It looks like I'm going to get drenched in sweat. 
    AH: Yes, I was sweating a lot halfway through. 
    AQ: That's right. But it's better in the morning, isn't it? 
    AH: Yes, it seems it will get hotter in the afternoon. 
    AQ: I can't walk from the afternoon. 
    AH: Yes, I want to stay at home from the afternoon. 
    AQ: Yes, yes, but recently I've been staying at home all day. 
    AH: It looks comfortable and I'm envious. 
    AQ: "Work was also remote until last month." 
    AH: It seems convenient since you don't have to go out when working remotely. 
    AQ: Once you get used to remote work, you won't be able to go out to work. 
    AH: Certainly, the habit of going outside has been interrupted. 
    AQ: That's right. It's so comfortable that I can't escape. 
    AH: I would also like to try remote work. 
    AQ: Please give it a try if you have the chance. 
    AH: Yes, I would like to consider such a type of job as well. 
    AQ: Let's talk again.
    """

    sample_2_human_human_dialogue = """
    AH: Hello! 
    AQ: Hello. 
    AH: Which season do you like?
    AQ: It is summer. 
    AH: Is it summer? It feels kind of unusual. 
    AQ: "Is that so? There are a lot of fireworks and events, right?" 
    AH: I see, there were indeed fireworks festivals and summer festivals. 
    AQ: That's right. I hate the heat, but I like sweating, such a contradiction. 
    AH: Do you exercise? 
    AQ: "Not at all now, but I like exercising." 
    AH: I respect people who can exercise. 
    AQ: Is that so? Don't you exercise? 
    AH: I am not good at intense exercise. 
    AQ: I wonder if they're not good at volleyball or something. 
    AH: I was not good at things that use balls. 
    AQ: Hmm. It's difficult, isn't it? 
    AH: Yes, it was difficult to throw the ball to the intended position. 
    AQ: "It's difficult, isn't it? Did you have marathon events during your school days?" 
    AH: Found it! 
    AQ: "For people who are not good at that, it's like hell, isn't it?" 
    AH: Yes, the practice was quite tough. 
    AQ: I feel like I was made to run quite a distance. 
    AH: I think it was about one kilometer from my place. 
    AQ: Huh? Was it just that much? 
    AH: It might be different depending on the school. 
    AQ: That's right. I think it was 10 km during high school. 
    AH: It seems like it will take about an hour. 
    AQ: "That's right. It's already hell." 
    AH: It seems like I would collapse if I don't stay hydrated. 
    AQ: That's really true. Thank you very much.
    """

    personality_traits = """
    'Openness': 5.25
    AH are a curious and imaginative individual who values creativity and new experiences. AH are likely to enjoy exploring different cultures, ideas, and unconventional ways of thinking. This trait makes AH open-minded and receptive to change, often leading AH to seek out diverse perspectives and innovative solutions in your personal and professional life.
    'Conscientiousness': 3.1666667461395264
    AH are moderately organized and reliable, though AH may sometimes struggle with maintaining consistent levels of discipline and planning. While AH are capable of setting goals and working towards them, AH might occasionally procrastinate or find it challenging to stay focused. In AH's relationships and work, AH's balance spontaneity with responsibility, often adapting to the needs of the moment.
    'Extraversion': 3.3333332538604736
    AH have a balanced level of extraversion, enjoying social interactions and activities while also valuing AH's alone time. AH can be outgoing and energetic in social settings, but AH also appreciate periods of solitude to recharge. This trait allows AH to be adaptable in various social environments, maintaining meaningful connections without feeling overwhelmed.
    'Agreeableness': 4.166666507720947
    AH are generally kind, empathetic, and cooperative, often striving to maintain harmony in AH's relationships. AH value getting along with others and are usually willing to compromise to avoid conflicts. This trait helps AH build strong, supportive relationships, though AH might sometimes prioritize others' needs over AH's own.
    'Neuroticism': 4.416666507720947
    AH are somewhat prone to experiencing stress and emotional fluctuations, often feeling worried or anxious about potential problems. While this can sometimes lead to moments of self-doubt or moodiness, it also means AH are highly aware of AH's emotions and can be very empathetic towards others. AH's sensitivity allows AH to navigate and respond to emotional situations thoughtfully.
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
    Now I will provide you with a Human-Human Dialogue as follows:  
    ## Human-Human Dialogue:  
    {sample_1_human_human_dialogue}
    Here, AH and AQ are their respective designations. Now I will provide you with AH's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human-Human Dialogue and Human-Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human-Computer Dialogue, with AH playing the role of the Human and AQ playing the role of the Computer. Specifically, you need to transform AH's utterances based on AH's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AQ's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human-Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, AH and AQ are their respective designations. Now I will provide you with AH's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with AH playing the role of the Human and AQ playing the role of the Computer. Specifically, you need to transform AH's utterances based on AH's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AQ's utterances into a Computer style, also without altering the content and meaning.  

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

