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
        Here, DG and BA are their respective designations. Now I will provide you with DG's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where DG simulates the role of a Human (converting DG's utterances in the original Human Human Dialogue), and BA simulates the role of a Computer (converting BA's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("DG:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    DG: Good evening. 
    BA: Good evening! 
    DG: Were you okay with the typhoon yesterday? 
    BA: I was okay! How about you? 
    DG: It was okay, but when the rain stopped, the cicadas started a grand chorus. 
    BA: Interesting 
    DG: You're so noisy! 
    BA: It's noisy, isn't it? 
    DG: This month is already halfway over in the blink of an eye. 
    BA: It's true, isn't it! Did you do anything summery? 
    DG: No, I've been staying home a lot! Did you go somewhere? 
    BA: The sea and the pool, I guess. 
    DG: It's an incredible summer, isn't it? Did you get a tan? 
    BA: It's doing it repeatedly. 
    DG: Oh, I'm not good at it because I get really red. I'm envious. 
    BA: I see! 
    DG: Yes, but the sunlight is really strong this year. 
    BA: Are you doing UV care? 
    DG: I'm applying it just in case, but I'm worried about how effective it is. 
    BA: You don't understand, right? 
    DG: Yes, I got a little tan. 
    BA: It's completely impossible, isn't it? 
    DG: "Yes. I admire tanned skin." 
    BA: "Is that so? It will get covered in stains!" 
    DG: There are already spots on my arm! 
    BA: Oh! Can people who blush also get spots? 
    DG: Somehow I turn red for a moment and then remain without realizing it. 
    BA: That's unpleasant. 
    DG: I need to be careful! Thank you very much. 
    BA: Thank you very much.
    """

    sample_2_human_human_dialogue = """
    DG: Nice to meet you. 
    BA: Nice to meet you. 
    DG: Is there anything you've been into recently? 
    BA: Hmmm, I wonder, who are you? 
    DG: "Maybe things like watching movies." 
    BA: I like it too! What have you watched recently? 
    DG: I went to see the new One Piece release. 
    BA: You watch anime too, right? 
    DG: I see. At home, we watch a lot of Western movies. 
    BA: I also like Western movies.
    DG: Do you have any favorite works or actors? 
    BA: I like Ryan Gosling. 
    DG: What were you in? My memory is vague. 
    BA: "The Notebook for you!" 
    DG: Oh! Are you from La La Land? 
    BA: That's right! 
    DG: "That actor is great, isn't he? I also liked the role he played in 'Kimi ni Yomu'." 
    BA: "That's nice! Who is the person you like?" 
    DG: "Old Johnny Depp." 
    BA: "When was it aired?" 
    DG: Hmm. I like a movie called "Chocolat". 
    BA: Is it no good recently? 
    DG: It's not that it's bad, but I liked it when he teamed up with Tim Burton. 
    BA: I see. 
    DG: "Recently there haven't been many interesting new releases, so it's mostly Prime." 
    BA: I am Netflix. 
    DG: Netflix originals have increased! 
    BA: "It has increased quite a lot, hasn't it? We can't keep up." 
    DG: "That's true. It's a convenient world." 
    BA: It’s true, isn’t it?
    """

    personality_traits = """
    Openness: 4.833333492279053
    DG is relatively open to new experiences and ideas. He/she enjoys exploring creative and intellectual pursuits but may have a balanced approach, not being overly avant-garde or rigid in his/her thinking.
    Conscientiousness: 4.25
    DG is quite dependable and organized, often completing tasks with a sense of responsibility. He/she values structure but might not be overly meticulous, allowing for some flexibility.
    Extraversion: 4.416666507720947
    DG is sociable and enjoys being around others. He/she tends to be outgoing and energetic, thriving in social settings but also values moments of solitude to recharge.
    Agreeableness: 3.75
    DG is somewhat cooperative and empathetic but also balances his/her own needs with those of others. He/she may be seen as fair and considerate without being overly accommodating.
    Neuroticism: 6.083333492279053
    DG experiences a higher level of emotional sensitivity and may be prone to stress and anxiety. He/she might frequently worry and react strongly to various situations, indicating a need for reassurance and stability.
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
    Here, DG and BA are their respective designations. Now I will provide you with DG's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with DG playing the role of the Human and BA playing the role of the Computer. Specifically, you need to transform DG's utterances based on DG's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BA's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, DG and BA are their respective designations. Now I will provide you with DG's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with DG playing the role of the Human and BA playing the role of the Computer. Specifically, you need to transform DG's utterances based on DG's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform BA's utterances into a Computer style, also without altering the content and meaning.  

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

