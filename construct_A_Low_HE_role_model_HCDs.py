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
        Here, HE and GU are their respective designations. Now I will provide you with HE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where HE simulates the role of a Human (converting HE's utterances in the original Human Human Dialogue), and GU simulates the role of a Computer (converting GU's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("HE:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    HE: Hello! 
    GU: Hello! 
    HE: Did you eat breakfast? 
    GU: One bread, please! 
    HE: What kind of bread is it? 
    GU: It's anpan! 
    HE: It goes well with milk! 
    GU: I just drank it! 
    HE: I laughed! 
    GU: This combination is good. 
    HE: I also like anpan. 
    GU: "Is it tsubu or koshi?" 
    HE: Is it the lower back? 
    GU: It's the same! 
    HE: "The texture of the grains is a bit...!" 
    GU: "I understand, there are many arguments, aren't there?" 
    HE: I'm a bit not good at it! 
    GU: It seems like I became someone who dislikes food without trying it. 
    HE: In the past? 
    GU: Yes, when I was little.
    HE: When we were little, we tended to have more foods we disliked without even trying them. 
    GU: If the first impression is not good. 
    HE: I used to dislike things like green peppers. 
    GU: It's the same. 
    HE: But now I love it! 
    GU: Is it a change in taste? 
    HE: I think it's big. 
    GU: That's right, there's no other way. 
    HE: "I'm willingly eating it." 
    GU: Me too.
    """

    sample_2_human_human_dialogue = """
    HE: Hello! 
    GU: Hello! 
    HE: Do you have a favorite food? 
    GU: "Is it fried rice?" 
    HE: Oh! 
    GU: I like it so much that I make it myself. 
    HE: "Will it become separated?" 
    GU: It happened! 
    HE: The results of your practice are showing! 
    GU: In the beginning, already...! 
    HE: Was it too much? 
    GU: Continuously failing. 
    HE: At first, it's like that! 
    GU: I was frustrated. 
    HE: Did you get used to it? 
    GU: Yes. And a wok, please. 
    HE: Did you go out of your way to buy it? 
    GU: I went out of my way to buy it! 
    HE: "That's amazing, it looks heavy." 
    GU: It's hard when it rains. 
    HE: "Do you dance? Cool!" 
    GU: It's no big deal! 
    HE: "But it looks good on you." 
    GU: Indeed, it is fun. 
    HE: I also want to try eating it. 
    GU: Is it the flaky one? 
    HE: Yes!!! 
    GU: I will make it someday! 
    HE: Is that true!? 
    GU: I will become a chef!!
    """

    personality_traits = """
    HE has a low score of 1.083 on Openness, indicating they are practical, prefer routine, and might not be very interested in abstract or imaginative activities. They like familiar things and are comfortable sticking with the status quo rather than exploring new ideas or experiences.
    With a high score of 5.5 on Conscientiousness, HE is highly organized, reliable, and disciplined. They set clear goals, plan methodically, and follow through with their commitments. They value order and are likely very detail-oriented and dependable.
    Scoring 4.5 on Extraversion, HE is outgoing and energetic. They enjoy social interactions, feel comfortable in group settings, and are likely to seek out social activities. HE has a positive outlook and draws energy from being around others, although they also appreciate some alone time.
    An Agreeableness score of 3.667 suggests HE is generally cooperative and gets along well with others, though they are capable of standing their ground when needed. They are considerate and friendly but can balance their own needs with those of others effectively.
    With a Neuroticism score of 2.583, HE is relatively stable and composed. They handle stress well and maintain an even-tempered disposition. While they may experience negative emotions occasionally, they are generally resilient and not easily overwhelmed by life's challenges.
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
    Here, HE and GU are their respective designations. Now I will provide you with HE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with HE playing the role of the Human and GU playing the role of the Computer. Specifically, you need to transform HE's utterances based on HE's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform GU's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, HE and GU are their respective designations. Now I will provide you with HE's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with HE playing the role of the Human and GU playing the role of the Computer. Specifically, you need to transform HE's utterances based on HE's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform GU's utterances into a Computer style, also without altering the content and meaning.  

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