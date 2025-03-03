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
        Here, CC and AY are their respective designations. Now I will provide you with CC's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where CC simulates the role of a Human (converting CC's utterances in the original Human Human Dialogue), and AY simulates the role of a Computer (converting AY's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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

def count_ct_occurrences(dialogue):
    return dialogue.count("CC:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    CC: Nice to meet you! 
    AY: Nice to meet you! 
    CC: Did you participate in any summer-like events? 
    AY: The only thing that felt like summer was eating ice cream! How about you? 
    CC: I see. I went to the local festival which was revived for the first time in three years. AY: Oh! How was it? 
    CC: The fireworks were beautiful. 
    AY: "There were fireworks!" 
    CC: I thought all the festivals had resumed, but it seems there are still some that can't take place yet. 
    AY: I see. It might not be the case for us yet. 
    CC: I see. 
    AY: Yes. Did you do things like goldfish scooping? 
    CC: I didn't do it, lol. 
    AY: Well then, did you eat anything? 
    CC: That's right. We watched fireworks while eating fried chicken. 
    AY: Oh! Summer! That feeling is wonderful! 
    CC: I'm satisfied that I could also drink beer. 
    AY: "Beer, huh! Can you drink quite a lot?" 
    CC: It's about average. How about you? 
    AY: I'm not good with beer. 
    CC: Oh, I see. Are you not good with alcohol in general? 
    AY: I like sweet things! 
    CC: So you drink cocktails, huh! 
    AY: That's right! Like Horoyoi. 
    CC: I see. Do you also drink alone? 
    AY: Mostly with friends and family. 
    CC: I also only drink alcohol when I am with someone else. 
    AY: I see! It sounds like a lot of fun. 
    CC: Isn't it! 
    AY: Please tell me more again.
    """

    sample_2_human_human_dialogue = """
    CC: Nice to meet you! 
    AY: Yes. Likewise! 
    CC: What do you usually do when you have time? 
    AY: Hmm. Maybe the TV or a game. 
    CC: Are you more of an indoor person? 
    AY: "I'm a hardcore indoor person!" 
    CC: "I'm also a hardcore indoor person!" 
    AY: "It's hot outside, it's impossible!" 
    CC: Certainly. What kind of TV programs do you watch? 
    AY: Recently, there are a lot of dramas, aren't there? 
    CC: "My favorite is the magical renovation. As for the drama." 
    AY: Ah! That is interesting! I am watching it too. 
    CC: "I wasn't expecting much, but it was surprisingly interesting." 
    AY: That's right. It's easy to watch and enjoyable. 
    CC: The uncles are cute, aren't they? 
    AY: Hahaha! Yeah, yeah! It has quite a good flavor, and it might be stealing the spotlight. 
    CC: What other dramas are you watching? 
    AY: This season, I'm watching Old Rookie. 
    CC: Oh, I'm watching it too. 
    AY: "A drama that is educational in various ways!" 
    CC: "That's right! Since I'm not familiar with sports, this is a good learning experience." 
    AY: Yes. And the main character is cute! 
    CC: Ayano Go can do both cute and cool roles, which is amazing. 
    AY: "That's right. He plays the wimp role perfectly, too!" 
    CC: Also, I thought having such a nice wife was enviable. 
    AY: "Your wife is too perfect!" 
    CC: Is there really someone as bright and kind as that? 
    AY: Hey! And it seems like you can make some money too. 
    CC: I also want to marry Kanako-chan. 
    AY: "If I were a man, I'd want to marry you!"
    """

    personality_traits = """
    Openness: 6.25
    CC is highly open to new experiences and values creativity and innovation. He/she enjoys exploring new ideas, learning new things, and is often curious about the world. This openness makes him/her adaptable and imaginative.
    Conscientiousness: 3.0
    CC has a moderate level of conscientiousness. He/she may not be particularly focused on organization or detailed planning, but can still complete tasks and meet responsibilities. His/her approach may be more flexible and spontaneous rather than strictly disciplined.
    Extraversion: 3.3333332538604736
    CC has a balanced level of extraversion. He/she enjoys social interactions and can be outgoing and energetic in social situations, but also values and needs some time alone to recharge. This balance allows him/her to be adaptable in both social and solitary settings.
    Agreeableness: 5.333333492279053
    CC is quite agreeable, displaying warmth, kindness, and a cooperative nature. He/she is likely to be empathetic and considerate towards others, valuing harmonious relationships and often putting others' needs before his/her own.
    Neuroticism: 3.0833332538604736
    CC has a relatively average level of neuroticism. He/she may experience occasional stress or emotional fluctuations, but generally manages to maintain a balanced emotional state. This level allows him/her to be resilient in most situations without being overly affected by negative emotions.
    """

    additional_knowledge = """
    Differences Between Human Human Dialogue (HHD) and Human Computer Dialogue (HCD):

    Communication Styles:

    HCD: Interactions between humans and machines are characterized by brief, frequent exchanges that prioritize efficiency. Humans expect clear, straightforward responses without unnecessary elaboration.
    Example: Human: "What time is my next meeting?" System: "Your meeting starts at 2:00 PM in Conference Room B."

    HHD: Interactions between humans are more nuanced and context-rich, often incorporating additional details, shared thoughts, or collaborative reasoning.
    Example: Person A: "The weather app says it’ll stay clear, but the sky looks a bit hazy. Do you think we should leave earlier for the hike?" Person B: "Good point—maybe we can avoid the afternoon crowd too. Let’s aim for 8 AM instead!"

    Relational and Personality Expression:

    HCD: Interactions between humans and machines are transactional and lack emotional depth or personal connection, as machines are incapable of genuine empathy or emotional understanding.
    Example: Human: "I’m overwhelmed with work deadlines." System: "Would you like me to schedule a reminder for your tasks?"

    HHD: Human interactions are infused with emotional expression, humor, and openness, fostering trust and mutual understanding. These exchanges often include empathy, support, and shared problem-solving.
    Example: Person A: "I’ve been swamped with deadlines all week—it’s exhausting." Person B: "That sounds rough. Want to grab coffee later? We can brainstorm ways to tackle it together."
    """

    sample_1_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_1_human_human_dialogue}
    Here, CC and AY are their respective designations. Now I will provide you with CC's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with CC playing the role of the Human and AY playing the role of the Computer. Specifically, you need to transform CC's utterances based on CC's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AY's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, CC and AY are their respective designations. Now I will provide you with CC's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with CC playing the role of the Human and AY playing the role of the Computer. Specifically, you need to transform CC's utterances based on CC's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AY's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_1_human_computer_dialogue = llm_response(sample_1_dialogue_transformation_prompt)

    sample_1_dialogue_transformation_human_feedback = """
    """

    sample_1_human_human_ct_count = count_ct_occurrences(sample_1_human_human_dialogue)
    sample_1_human_computer_ct_count = count_ct_occurrences(sample_1_human_computer_dialogue)

    sample_1_regenerated_human_computer_dialogue = evaluate_dialogue(sample_1_human_human_dialogue, sample_1_human_computer_dialogue, personality_traits, additional_knowledge, sample_1_dialogue_transformation_human_feedback)

    print('Final sample 1 HCD: ', sample_1_regenerated_human_computer_dialogue)

    sample_2_human_computer_dialogue = llm_response(sample_2_dialogue_transformation_prompt)

    sample_2_dialogue_transformation_human_feedback = """
    """

    sample_2_human_human_ct_count = count_ct_occurrences(sample_2_human_human_dialogue)
    sample_2_human_computer_ct_count = count_ct_occurrences(sample_2_human_computer_dialogue)

    sample_2_regenerated_human_computer_dialogue = evaluate_dialogue(sample_2_human_human_dialogue, sample_2_human_computer_dialogue, personality_traits, additional_knowledge, sample_2_dialogue_transformation_human_feedback)

    print('Final sample 2 HCD: ', sample_2_regenerated_human_computer_dialogue)