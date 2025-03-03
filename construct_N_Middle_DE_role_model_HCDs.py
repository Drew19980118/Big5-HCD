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
        Here, DE and DD are their respective designations. Now I will provide you with DE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where DE simulates the role of a Human (converting DE's utterances in the original Human Human Dialogue), and DD simulates the role of a Computer (converting DD's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("DE:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    DE: Hello, nice to meet you. 
    DD: Hello! Nice to meet you! 
    DE: What did you have for lunch? 
    DD: I haven't had lunch yet. I had a late breakfast. What did you have? 
    DE: "Oh, is that so? I had deli bread and supermarket takoyaki." 
    DD: "Is it okay to ask what kind of savory bread it is?" 
    DE: It was a roll with cutlet and cabbage inside. It was delicious. 
    DD: Wow, that looks delicious! Maybe I will have some bread too. 
    DE: Do you like bread? What kind of bread do you want to eat? 
    DD: You really like bread! Recently, I've been hooked on the loaf bread from a nearby bakery and eat it often! 
    DE: It's delicious, isn't it? What kind of bread is it? 
    DD: "They are particular about the ingredients, so it's sweet and delicious even without adding anything." 
    DE: Recently, I feel like a lot of specialty bread shops have been opening. 
    DD: Yes, that's right! I've been seeing it quite often recently! 
    DE: I often see stores with long lines that sell out quickly, but I don't like waiting in line, so I haven't bought from them much. 
    DD: I don't feel like buying something if I have to wait in line. I definitely won't wait in line for ramen either. 
    DE: For some reason, people line up at the ramen shop. It's said that the neighborhood is relatively competitive when it comes to ramen. 
    DD: I see! Do you like ramen? 
    DE: I didn't like it much before, but I'm starting to like it because of my husband's influence. How about you? Do you like ramen? 
    DD: I don't really feel like I have to eat ramen, but since my food preferences have been changing recently, I think I'll give it a try. 
    DE: How about some somen or soba? 
    DD: I prefer udon over soba, but among noodle dishes, ramen might be my least favorite. 
    DE: Udon is delicious too. As for udon, I like Sanuki udon. 
    DD: Sanuki udon is delicious, isn't it? I've started thinking udon would be great for lunch too! Haha. 
    DE: "Is it bread or udon? I guess it's wheat flour. Hahaha." 
    DD: "Isn't it!! Maybe it's too much flour! I'll have rice for dinner! Haha." 
    DE: Recently, there's so much wheat flour in food that I sometimes wonder what it would be like to live without it. 
    DD: Ah, but there was a period when I was influenced by my family to go gluten-free, and it was tough. 
    DE: That's amazing. How was it difficult? 
    DD: As you mentioned, it's hard to find food without wheat, it's expensive, and I have to cook it myself.
    """

    sample_2_human_human_dialogue = """
    DE: Hello. Nice to meet you! 
    DD: Hello! Nice to meet you! 
    DE: Is your family home nearby? 
    DD: I live with my parents! 
    DE: That's nice. When I go back to my hometown, it takes half a day to get there as it's a distant place. 
    DD: I see! It's a case of wanting what you can't have, but sometimes I feel a bit envious of people who can go back to their hometown. 
    DE: A friend who was born and raised in Kanto often says the same thing. 
    DD: That's right! I'd like to do things like go back to my parents' house, take a short trip, or exchange things with each other. 
    DE: "Yes. It's a common issue when visiting home, but I have trouble choosing souvenirs." 
    DD: Certainly! What kind of things would make them happy? 
    DE: Basically, it depends on the recipient, but parents are usually happier with something other than sweets. 
    DD: I see! Do your parents not like sweets very much? 
    DE: Yes, that's right. Somehow, I've developed a very discerning palate and can't bring myself to buy something subpar. Haha. 
    DD: That's a high hurdle! It seems like you'll need to do some research and preparation first! Haha. 
    DE: "Is that so? Do you buy souvenirs for your family on your way back from work?" 
    DD: You buy quite a lot! Everyone in our family likes sweets, so we often buy sweet things! 
    DE: What kind of things have you eaten recently? 
    DD: Since I like Japanese sweets, I ate ohagi from the Japanese sweets shop in the department store! 
    DE: I also like wagashi. I feel that ohagi has recently become more stylish and delicious. 
    DD: That's right! It's fun just to look at them! It's tough because they don't last long and I can only buy a small amount. 
    DE: Certainly. When I was learning the tea ceremony before, I used to eat seasonal Japanese sweets almost every week. 
    DD: Wow! Tea ceremony, that sounds great! I've always admired it! Including the traditional sweets! Hehe. 
    DE: There is an elegance that cannot be expressed in the four seasons of spring, summer, autumn, and winter. It is refined and I love it. 
    DD: "That's lovely - it's making me want to drink some matcha." 
    DE: I drank matcha the day before yesterday. There is a Japanese-style cafe in the neighborhood that serves wagashi and matcha. 
    DD: There’s such a stylish café in your neighborhood? That's nice! Do you go there often? 
    DE: Yes, I might go about once a week. You can enter casually without any formalities. 
    DD: Then, you are a regular customer! 
    DE: "Yes. It is a store run by an acquaintance." 
    DD: That makes going even more easy and enjoyable! Thank you very much!
    """

    personality_traits = """
    Openness: 5.166666507720947
    DE is quite open to new experiences, showing a keen interest in exploring novel ideas and embracing creativity. He/she likely enjoys diverse artistic and intellectual pursuits and is open-minded towards different perspectives and unconventional approaches.
    Conscientiousness: 2.5
    DE exhibits moderate levels of conscientiousness, suggesting a somewhat laid-back approach towards organization and planning. He/she may struggle with self-discipline and consistency but can be flexible and spontaneous when needed.
    Extraversion: 4.75
    DE is moderately extraverted, enjoying social interactions and feeling energized by spending time with others. He/she is generally outgoing and assertive, often seeking out social engagement while also appreciating some moments of solitude.
    Agreeableness: 5.166666507720947
    DE scores high on agreeableness, indicating a compassionate and cooperative nature. He/she is likely considerate, empathetic, and enjoys helping others, striving to maintain harmony in interpersonal relationships.
    Neuroticism: 4.083333492279053
    DE has a moderate level of neuroticism, experiencing occasional emotional fluctuations and moments of stress or anxiety. He/she may be sensitive to criticism and can sometimes struggle with self-confidence but generally manages to cope with challenges over time.
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
    Here, DE and DD are their respective designations. Now I will provide you with DE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with DE playing the role of the Human and DD playing the role of the Computer. Specifically, you need to transform DE's utterances based on DE's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform DD's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, DE and DD are their respective designations. Now I will provide you with DE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with DE playing the role of the Human and DD playing the role of the Computer. Specifically, you need to transform DE's utterances based on DE's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform DD's utterances into a Computer style, also without altering the content and meaning.  

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