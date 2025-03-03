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
        Here, GQ and EB are their respective designations. Now I will provide you with GQ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where GQ simulates the role of a Human (converting GQ's utterances in the original Human Human Dialogue), and EB simulates the role of a Computer (converting EB's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("GQ:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    GQ: Hello, nice to meet you. 
    EB: Hello - nice to meet you too. 
    GQ: After the typhoon passed, it became very cool, didn't it? 
    EB: That's right, it might drop below 20 degrees at night. 
    GQ: I didn't prepare the futon, so I feel like I'm going to catch a cold. 
    EB: Haha, we are still using a towel blanket. 
    GQ: "I also need to wash the blanket because I was fighting over the towel blanket with my child." 
    EB: "Yes, we should start preparing soon." 
    GQ: I need to prepare long sleeves too. 
    EB: "I have put out a few long-sleeved shirts, but I think it's not quite necessary yet." 
    GQ: Since I only prepared a light jacket, I also need to bring out something to wear underneath. 
    EB: "It's tough to put them away and take them out, isn't it?" 
    GQ: I see. Do you switch out your clothes yourself? 
    EB: The whole family will do it together. 
    GQ: Great job! I have to do it almost entirely by myself. 
    EB: I think that is tough! It’s quite heavy! 
    GQ: I have a backlog of taking my children's old clothes to the recycle shop, so I can't get it sorted out. 
    EB: Ah, I see! Nowadays, they come to pick it up for you! 
    GQ: Since I don't have such luxury items, I feel hesitant and will only bring my own. EB: You shouldn't worry about that anymore, since it's a service like that, you have to use it! 
    GQ: I will definitely try it next time. 
    EB: Yeah, yeah, it's better if we can reduce the burden. 
    GQ: Donating used clothes is also an option, right? 
    EB: That's true! Facilities are quite pleased with it. 
    GQ: I was thinking that maybe I didn't need it, but I might give it a try. 
    EB: Yes, yes, please try various things! It's become more convenient. 
    GQ: There are options where you just pack it in a cardboard box without bearing the shipping cost, aren't there? 
    EB: Yes, yes, as long as I have cardboard, I'm fine. 
    GQ: We have so much that the house will be full right away. 
    EB: "We don't really keep that many cardboard boxes."
    """

    sample_2_human_human_dialogue = """
    GQ: Hello, nice to meet you. 
    EB: Thank you in advance. 
    GQ: Do you play video games? 
    EB: "I only play games for work or with my kids." 
    GQ: Your job is related to games, isn't it? We have an elementary school boy, so it's all about the Switch. 
    EB: "It's not related to games, but as a translator, I work on translating and localizing overseas games." 
    GQ: There is such a job, isn't there? It will be a reference for my child's future. 
    EB: Before the coronavirus, I had a lot of work overseas, but now I do more translation work at home, like for dramas and movies. 
    GQ: It's my dream job. I love Western movies. 
    EB: I see! If I say too much, it will be obvious, so I've probably localized a movie you know. 
    GQ: Amazing! But I haven't been to the movie theater recently. 
    EB: It's quite difficult to get around, you know. When I went to see Evangelion, it was pretty empty. 
    GQ: Our high school student finally started watching foreign films with subtitles with us. 
    EB: "Yeah, yeah, for some movies I really recommend the subtitles." 
    GQ: That's right. It's difficult to watch with subtitles when the children are young. EB: Certainly, that's true. In our household, we speak in different languages inside the house to get used to a foreign language environment. 
    GQ: I respect you! I've failed many times because my parents can't speak. 
    EB: Ah, that's quite tough. I think the fact that the parents need to talk first is significant. 
    GQ: That's why I'm determined to have my children study abroad. 
    EB: I see, if you are going to study abroad, I recommend the UK. 
    GQ: You can speak beautiful English, right? Did you study in the UK? 
    EB: I am self-taught in English. The reason why the UK is good is because it has the most advanced independent education in the world. 
    GQ: Education that fosters independence is important, isn't it? 
    EB: Yeah, yeah, it doesn't mean anything if you study a lot and gain knowledge but can't do anything on your own. 
    GQ: I understand. Maybe the kids' room is already separate? 
    EB: The top is separate. 
    GQ: We have a bunk bed with two people on the top, and the elementary school child still sleeps with me. 
    EB: "I don't mind if you rely on me, but I've decided to do things for myself if I can." 
    GQ: Wonderful! I have the same idea, but we haven't been able to put it into practice. 
    EB: "It depends on the environment, so there's not much we can do about it."
    """

    personality_traits = """
    Openness: 4.58
    GQ is moderately open to new experiences and ideas. He/She enjoys exploring different concepts and engaging in creative activities, though not excessively. He/She values both novelty and tradition, striking a balance between the two.
    Conscientiousness: 3.67
    GQ has a somewhat average level of conscientiousness. He/She is reasonably organized and dependable, though there may be times when he/she prefers a more relaxed approach. He/She can be diligent and responsible but may not always prioritize meticulous planning.
    Extraversion: 6.5
    GQ is highly extroverted. He/She thrives in social situations, enjoying the company of others and seeking out interactions. He/She is energetic, talkative, and finds joy in being the center of attention, often feeling invigorated by social gatherings.
    Agreeableness: 6.33
    GQ scores high on agreeableness. He/She is compassionate, cooperative, and generally gets along well with others. He/She tends to prioritize harmony and is considerate of other people's feelings, often being seen as kind and empathetic.
    Neuroticism: 4.0
    GQ exhibits a moderate level of neuroticism. He/She may experience emotional ups and downs but is generally able to manage stress and anxiety. He/She is somewhat sensitive to emotional fluctuations yet maintains a fair level of emotional stability.
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
    Here, GQ and EB are their respective designations. Now I will provide you with GQ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with GQ playing the role of the Human and EB playing the role of the Computer. Specifically, you need to transform GQ's utterances based on GQ's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform EB's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, GQ and EB are their respective designations. Now I will provide you with GQ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with GQ playing the role of the Human and EB playing the role of the Computer. Specifically, you need to transform GQ's utterances based on GQ's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform EB's utterances into a Computer style, also without altering the content and meaning.  

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

