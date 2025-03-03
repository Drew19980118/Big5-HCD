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
        Here, BJ and AN are their respective designations. Now I will provide you with BJ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where BJ simulates the role of a Human (converting BJ's utterances in the original Human Human Dialogue), and AN simulates the role of a Computer (converting AN's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("BJ:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    BJ: Good morning! 
    AN: Good morning! 
    BJ: What are you going to do today? 
    AN: Today, I'm going blueberry picking in the afternoon! 
    BJ: Wow! How fun! 
    AN: That's right. I found a blueberry farm by chance while taking a walk near my house. 
    BJ: It's wonderful to have something like that in the neighborhood. Are blueberries in season during the summer? 
    AN: It seems to be in season until the end of August. 
    BJ: I see. It's nice, picking fruit is fun, isn't it? 
    AN: It's fun, isn't it! I went strawberry picking in the spring! 
    BJ: "That's quite frequent! You must really like fruit." 
    AN: I love fruits. My kids also love fruits. 
    BJ: Sounds good. The last time I went grape picking was some years ago. 
    AN: Is that so? Are you picking Delaware grapes? Or Kyoho grapes? 
    BJ: It was Shine Muscat. To Yamanashi! 
    AN: "Shine Muscat? It looks really delicious!" 
    BJ: The food was delicious, but I ended up eating a lifetime's worth. I haven't had Shine Muscat since that day. 
    AN: "It seems like there aren't many opportunities to eat Shine Muscat grapes until you're full. What a valuable experience!" 
    BJ: "Certainly. What is your favorite fruit?" 
    AN: What could it be? A cherry or a strawberry? 
    BJ: Cherries are nice, aren't they? I haven't eaten them in a long time. 
    AN: Likewise, I couldn't eat cherries this year. 
    BJ: When you try to buy them, fruits are expensive, aren't they! 
    AN: "It's expensive. Cherries and such are luxuries." 
    BJ: I also only eat bananas in my daily life lol. 
    AN: Speaking of bananas, haven't they been getting more expensive lately? 
    BJ: "Eh, really? It doesn't feel real." 
    AN: Around here, you used to be able to buy bananas for about 100 yen, but lately, they cost around 200 yen. 
    BJ: Eh, that's expensive. 
    AN: That's right. I hope prices stabilize too. Well, I guess it's about time to wrap it up around here!
    """

    sample_2_human_human_dialogue = """
    BJ: Hello! 
    AN: Hello! 
    BJ: Is it summer vacation now? 
    AN: Yes. The children are now on summer vacation. 
    BJ: Sounds good. Are you going somewhere far? 
    AN: During the summer, we usually just play nearby. We plan to go camping in September. 
    BJ: Camping! Sounds great. 
    AN: I'm looking forward to it. Are you going anywhere? 
    BJ: Oh, there are so many places I want to go, but... 
    AN: In this day and age, it's hard to go out, isn't it? 
    BJ: It's true, isn't it? I want to go abroad. 
    AN: "I understand. It's been three years since I last went." 
    BJ: Where did you go last? 
    AN: The last one was Taiwan. 
    BJ: "Taiwan is nice, isn't it? I went there a few years ago too." 
    AN: The food is delicious, it's close and cheap, so I want to go there again sometime. 
    BJ: Is it Taipei? 
    AN: I went around Taipei and Taichung. Next, I want to go to Tainan. 
    BJ: That's nice. Taiwan really has a sense of familiarity, doesn't it? 
    AN: I see. So, I hope that an emergency situation in Taiwan does not occur. 
    BJ: "That's true... Peace is the best." 
    AN: Really? Where do you want to go next overseas? 
    BJ: If it's nearby, maybe Korea or Vietnam. 
    AN: Vietnam sounds great. South Korea has already reopened for tourism, right? 
    BJ: Ah, I wonder how it is. 
    AN: I believe that was the case. My husband mentioned that there were a lot of tourists when he went on a business trip. 
    BJ: Oh! I hope I can go soon. I want the various restrictions to be lifted quickly. 
    AN: That's right. If the waiting period is eliminated, it will be easier to go. 
    BJ: I am looking forward to that day. See you around! 
    AN: Yes. Thank you very much!
    """

    personality_traits = """
    BJ is a curious and imaginative individual who enjoys exploring new ideas and experiences (Openness: 5.5). 
    They can sometimes be spontaneous and may struggle with sticking to routines or long-term plans (Conscientiousness: 3.0). 
    BJ is sociable and enjoys being around others, often feeling energized in social settings (Extraversion: 5.083). 
    They are generally kind-hearted and cooperative, valuing harmony in their interactions but are not afraid to stand their ground when necessary (Agreeableness: 4.333). 
    BJ tends to experience a range of emotions intensely and may frequently feel anxious or stressed, indicating a higher level of emotional sensitivity (Neuroticism: 5.167).
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
    Here, BJ and AN are their respective designations. Now I will provide you with BJ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human-Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with BJ playing the role of the Human and AN playing the role of the Computer. Specifically, you need to transform BJ's utterances based on BJ's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AN's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, BJ and AN are their respective designations. Now I will provide you with BJ's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with BJ playing the role of the Human and AN playing the role of the Computer. Specifically, you need to transform BJ's utterances based on BJ's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AN's utterances into a Computer style, also without altering the content and meaning.  

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

    sample_2_human_human_ct_count = count_ct_occurrences(sample_2_human_human_dialogue)
    sample_2_human_computer_ct_count = count_ct_occurrences(sample_2_human_computer_dialogue)

    sample_2_dialogue_transformation_human_feedback = """
    """

    sample_2_regenerated_human_computer_dialogue = evaluate_dialogue(sample_2_human_human_dialogue, sample_2_human_computer_dialogue, personality_traits, additional_knowledge, sample_2_dialogue_transformation_human_feedback)

    print('Final sample 2 HCD: ', sample_2_regenerated_human_computer_dialogue)

