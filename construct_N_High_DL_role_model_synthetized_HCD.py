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
        Here, DL and DY are their respective designations. Now I will provide you with DL's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where DL simulates the role of a Human (converting DL's utterances in the original Human Human Dialogue), and DY simulates the role of a Computer (converting DY's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("DL:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    DL: Good evening. Nice to meet you. 
    DY: Good evening, nice to meet you. 
    DL: Suddenly, but do you read manga or anything like that? 
    DY: I often read manga! 
    DL: Do you have any favorite works? 
    DY: Recently, I found a jazz manga called "Blue Giant" interesting. 
    DL: "I have heard of it! Is it a currently ongoing series?" 
    DY: Yes, it is being serialized. Since I only read the compiled volumes, I don't know which magazine it is serialized in. 
    DL: "It seems like a Big Comic. It appears to have been made into a movie as well. I'm getting a little curious about it." 
    DY: It's really interesting. Even though it's a manga, it has the intensity that makes it feel like you can hear the sounds. 
    DL: I'll look it up and read it later! It's nice that we can easily read the first episode if we're interested. 
    DY: Certainly, it's helpful that we can read things now. Is there anything interesting on your side? 
    DL: I like works like "March Comes in Like a Lion," "Raika Days," and "Hatarakanai Futari," although they might be considered minor. 
    DY: "I used to read 'Hatarakanai Futari' a long time ago! It's the one about the NEET siblings, right!" 
    DL: That's right, that's right! I feel happy about it! Since it is updated every week, I look forward to reading it every week. 
    DY: It's nice and peaceful, isn't it? I also read a bit of March Comes in Like a Lion. It's the one about shogi, right? 
    DL: It seems to be quite well-read. I'm really happy because it feels like I've made some friends! Do you have any other manga recommendations? 
    DY: We might have similar tastes in manga. Also, do you know Blue Period? It's one of my favorites. 
    DL: "Is it the one in the afternoon?" 
    DY: That's right! It's the art manga one. 
    DL: You like intense plots in manga, don't you! 
    DY: Sure! Here's the translation: "That's right! I might like intense developments. However, I don't read manga as much as I used to." 
    DL: Oh, have you become busy with work or found a new hobby? 
    DY: I think I spend a lot of time lazily watching YouTube. 
    DL: "That is a time thief, isn't it? What kind of videos do you watch?" 
    DY: That's right, it's a time thief. I often end up watching game playthroughs idly. 
    DL: Ah! I get it now. Interesting people are really interesting, aren't they? And each video is so long. Before you know it, it's already this late! Something like that. 
    DY: That's true, and before you know it, it's time to sleep. Do you watch YouTube? 
    DL: I wouldn't say I watch it closely; it's more like I listen to it while doing housework, like a radio. It helps me clear my mind quite a bit. 
    DY: Indeed, there are times when I just listen without watching!
    """

    sample_2_human_human_dialogue = """
    DL: Good evening. Please take care of me. 
    DY: Good evening, thank you in advance. 
    DL: Recently, is there anything you're having trouble with? 
    DY: "Is something troubling you? I guess it's just that my job is too boring." 
    DL: "Is it boring? Are you doing clerical work instead of a professional job?" 
    DY: Since I am a system engineer, it is a specialized job, but I have stopped feeling very fulfilled by it. 
    DL: Is that so? I had an impression that creating various systems would be quite glamorous. Is that not the case? 
    DY: It's tough having too many working hours. It's like working until midnight every day was normal. But now I'm in a different department, so it's okay. 
    DL: "Until late at night!? Is it such a hard job!?" 
    DY: It's like catching the last train every day. Working late into the night is just normal! Though I think it's improved compared to the past. 
    DL: By the way, did you properly receive overtime pay!? It seems like it would be a lot if it was every day. 
    DY: Since it was a company that paid overtime, that was good. But I ended up thinking I didn't need to work that much. 
    DL: "Yes! Health is important! So, are you leaving work on time more often now?" 
    DY: Yes, that's right, I work 1 to 2 hours of overtime a day. But since I started teleworking, it's been really easy because I'm at home. 
    DL: It was good! But earlier, you said it was boring. Does that mean the job is too easy or something like that? 
    DY: I think it's because I don't feel a sense of fulfillment. I used to build systems, but now I'm managing people. 
    DL: Managing people doesn't seem interesting to you. You prefer creating systems, don't you? 
    DY: That might be the case. However, for those who create systems, it involves long working hours, being busy, and tension. It's a difficult problem. 
    DL: Both sides have their own issues, don't they? It's a tough decision on which to prioritize. Have you ever thought about changing jobs? 
    DY: Since I have a family, I realized I couldn't go on adventures. I'm not dissatisfied with the financial aspect, so I thought it would be best to leave it as it is! 
    DL: I see. You have found an answer. That's good. Indeed, having a family can sometimes restrict your freedom, right? 
    DY: Yes! Having a family has given me a place to calm my mind, so I think that has been good too. 
    DL: Somehow I felt relieved. By the way, how did you meet your wife? 
    DY: I met my wife through a matching app, it's quite rare, isn't it! 
    DL: Yes! That's a bit surprising. Do your hobbies and interests match? I'm curious. 
    DY: My hobby was not that much, but our values really matched well! 
    DL: That's really important, isn't it! I often hear that it can be quite painful when values are different. 
    DY: I think so. It's really fun to be together because I don't have to pretend or put on any airs when I'm with you! 
    DL: A very happy atmosphere is being conveyed. Wishing you happiness forever! 
    DY: Thank you very much!
    """

    personality_traits = """
    DL is someone with a balanced level of curiosity and openness to new experiences, demonstrating a willingness to explore new ideas and embrace change, but not excessively so. 
    They are very organized, dependable, and have a strong sense of duty, making them reliable and diligent in their endeavors. 
    DL is moderately outgoing and sociable, enjoying the company of others while also valuing some time alone. 
    They are highly agreeable, showing a great deal of empathy, kindness, and a cooperative nature in interactions with others. 
    However, DL tends to experience high levels of emotional instability, often feeling anxious and sensitive to stress, which can impact their overall sense of well-being.
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
    Here, DL and DY are their respective designations. Now I will provide you with DL's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with DL playing the role of the Human and DY playing the role of the Computer. Specifically, you need to transform DL's utterances based on DL's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform DY's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, DL and DY are their respective designations. Now I will provide you with DL's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with DL playing the role of the Human and DY playing the role of the Computer. Specifically, you need to transform DL's utterances based on DL's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform DY's utterances into a Computer style, also without altering the content and meaning.  

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