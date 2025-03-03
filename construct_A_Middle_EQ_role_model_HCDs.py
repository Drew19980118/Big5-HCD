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
        Here, EQ and DG are their respective designations. Now I will provide you with EQ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where EQ simulates the role of a Human (converting EQ's utterances in the original Human Human Dialogue), and DG simulates the role of a Computer (converting DG's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("EQ:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    EQ: Hello. 
    DG: Hello! 
    EQ: Did you go back to your hometown this summer? 
    DG: I went back to my parents' house, so I've been relaxing the whole time. 
    EQ: I see. It's nice to be able to take it easy. 
    DG: Did you go back to your hometown? 
    EQ: Yes. I went back to my hometown in Yamanashi. It was hot. 
    DG: Yamanashi is nice! I used to go there often to eat hoto (a type of noodle dish). EQ: Summer is hot. There are lots of delicious fruits. 
    DG: "It's really a very charming prefecture! Especially for someone who loves to eat!" 
    EQ: I see. Since I always have them sent to me, I've never bought grapes or peaches myself. 
    DG: "That's nice, peaches are nice. Recently, I've seen Yamanashi grape wine." 
    EQ: I mostly like California wine. 
    DG: I am not very knowledgeable, but I was impressed that there is delicious wine in Japan. 
    EQ: As someone from Yamanashi, that makes me happy! 
    DG: Do you often drink wine? 
    EQ: Since my husband likes it, I end up having more opportunities to drink. 
    DG: I see, is your husband knowledgeable about it? 
    EQ: I love it. There are many heavy drinkers around.
    DG: Ahaha, I also like drinking wine with him, but we both don't know much about it, so I'm envious. 
    EQ: "It's easy because it picks for me automatically. I usually find something cheap to drink." 
    DG: I also look for cheap ones when I drink alone! I can't quit alcohol. 
    EQ: Actually, you like alcohol too, don't you? 
    DG: "I quite like it. Yesterday, I had and was drinking grape liqueur." 
    EQ: If I had to choose, I prefer sweet and low-alcohol drinks. 
    DG: Do you drink chuhai? 
    EQ: I only drink chuhai when I go to an izakaya. 
    DG: I see. I drink green tea highballs at home. It seems like an old man's habit. 
    EQ: I have never had green tea highball. I want to try it. 
    DG: I ended up doing it with little guilt!
    """

    sample_2_human_human_dialogue = """
    EQ: Hello. How are you doing? 
    DG: Hello. I'm in a good mood listening to music. 
    EQ: What kind of music is it? 
    DG: I've been into a band called Maneskin lately. 
    EQ: I am not very familiar with it, but what genre would it be? 
    DG: It's rock music. I also encountered it for the first time at the festival the other day. 
    EQ: Oh. You went to a rock festival, didn't you? 
    DG: Yes, I participated for the first time in several years. It was tough because it was hot. 
    EQ: By the way, where was the location? 
    DG: It's Makuhari. 
    EQ: It looks like a lot of people will gather. 
    DG: There were quite a few people. More than I expected. 
    EQ: "Do you do that kind of thing at night?" 
    DG: It starts around 10 o'clock and continues until the evening. 
    EQ: "Is it that long? I wonder if I can go in and out?" 
    DG: "It's like securing a chair and taking a rest within the premises." 
    EQ: So, it's outdoors. 
    DG: Makuhari Messe was indoors and the stadium was outdoors! 
    EQ: So, the performance is indoors and the audience is outdoors? 
    DG: There were about six stages, and the stadium was the biggest stage. 
    EQ: "Does it mean that it progresses simultaneously on multiple stages?" 
    DG: That's right. I think there were about three indoor stages and about three outdoor ones.
    EQ: That's an incredible scale. If we could hear each other, our ears would probably go crazy. 
    DG: "The sound was fine, but the stage movement was too tough." 
    EQ: It means "It's quite spacious, isn't it?" 
    DG: Yes, I took the bus and such. I'm exhausted from the crowds that I haven't experienced in a while. 
    EQ: Bus! That's amazing. It looks like I'm going to get lost and separated from the people I went with. 
    DG: "A smartphone was absolutely necessary. The unfamiliar festival was tiring!" 
    EQ: But it's a good experience. I'm envious because I've never been there. 
    DG: Thank you very much for listening to all sorts of things. 
    EQ: "Likewise. Thank you for the enjoyable conversation."
    """

    personality_traits = """
    Openness: 4.333333492279053
    EQ has a moderately high level of openness, indicating a person who is curious, imaginative, and open to new experiences. He/she enjoys exploring new ideas and tends to be creative in his/her thinking and problem-solving.
    Conscientiousness: 4.916666507720947
    EQ is highly conscientious, showcasing a strong sense of responsibility and reliability. He/she is organized, dependable, and strives for excellence in his/her endeavors, often paying careful attention to detail.
    Extraversion: 4.5
    EQ is moderately extroverted, suggesting a sociable and energetic personality. He/she enjoys interacting with others and is often enthusiastic, drawing energy from social situations while also appreciating some downtime.
    Agreeableness: 4.916666507720947
    EQ scores very high in agreeableness, meaning he/she is compassionate, cooperative, and eager to maintain harmony in relationships. He/she tends to be considerate and understanding, often prioritizing others' needs.
    Neuroticism: 4.916666507720947
    EQ has a high level of neuroticism, indicating that he/she experiences emotions intensely and may be more prone to stress and mood fluctuations. He/she is sensitive and may often feel anxious or worried in uncertain situations.
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
    Here, EQ and DG are their respective designations. Now I will provide you with EQ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with EQ playing the role of the Human and DG playing the role of the Computer. Specifically, you need to transform EQ's utterances based on EQ's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform DG's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, EQ and DG are their respective designations. Now I will provide you with EQ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with EQ playing the role of the Human and DG playing the role of the Computer. Specifically, you need to transform EQ's utterances based on EQ's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform DG's utterances into a Computer style, also without altering the content and meaning.  

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