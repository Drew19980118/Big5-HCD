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
        Here, AC and AA are their respective designations. Now I will provide you with AC's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where AC simulates the role of a Human (converting AC's utterances in the original Human Human Dialogue), and AA simulates the role of a Computer (converting AA's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    AC: Hello! Nice to meet you. 
    AA: Hello, thank you in advance. 
    AC: Today, the weather is a bit cooler and comfortable. 
    AA: Really! I hope you can keep up this pace tomorrow as well. 
    AC: "That's true! Having over 35 degrees every day is murderous." 
    AA: Really! I spent my time wondering what on earth it was. 
    AC: "Right! Which do you tolerate better, heat or cold?" 
    AA: I prefer it to be cold. 
    AC: Me too! I crawl under the down comforter when it's cold. 
    AA: I understand. If it's cold, you can just put on more clothes, but if it's hot, there's nothing you can do about it. 
    AC: Yes, exactly! And also, sweat! 
    AA: That's right!!! It's stuck on and unpleasant. 
    AC: Yes! I feel like the concentration of my sweat has increased with age.
    AA: I kind of understand. I feel like it was smoother when I was younger. 
    AC: "Sure! When I was a child, I felt more at ease."
    AA: Really. I shouldn't have disliked summer either. 
    AC: That's right! Actually, I liked summer more for various reasons. 
    AA: Summer vacation is long, isn't it? 
    AC: Yes, yes. Did you finish your summer vacation homework early? 
    AA: It should have been the type to finish by early August. I might be idealizing it too much, though. 
    AC: "Great job! I remember almost crying towards the end." 
    AA: So you were the type to leave it until the end. 
    AC: Um, the picture diary? That was the most painful! 
    AA: Ah, that! It's something you have to write every day. 
    AC: Yes, yes. If you keep that bottled up, it’s disastrous. 
    AA: I don't even remember things from a few days ago. 
    AC: Hey. I feel like I only wrote about things like what I ate for breakfast every day. 
    AA: You were writing about breakfast, how cute. 
    AC: No, no, I should have been writing properly every day! Well then, that's all for today! 
    AA: Yes, thank you very much!
    """

    sample_2_human_human_dialogue = """
    AC: Hello! Nice to meet you! 
    AA: Hello! Nice to meet you! 
    AC: Do you have any plans to go out today? 
    AA: There is nothing after this! 
    AC: It feels like relaxing at home! 
    AA: That's right! After all, home is the most relaxing place. 
    AC: I also love being at home. What do you do at home? 
    AA: At home, I watch videos, read books, and take naps. 
    AC: I also watch videos occasionally. Do you have any favorite YouTube channels? 
    AA: I don't have any favorites, I just kind of stare off into space watching something. 
    AC: I see. Related videos keep coming up, don't they? 
    AA: Related videos are amazing, aren't they? They always match my preferences. 
    AC: I agree! What kind of things are on display these days? 
    AA: "The animals are lined up, aren't they? It's so calming." 
    AC: "I also have quite a few. Mostly Mochimaru-sama." 
    AA: "Wow, that's nice!" 
    AC: "Also, Akina Nakamori and other idols from the 80s have been coming up recently." 
    AA: Oh, do you often hear about that area? 
    AC: No, not really, but when I searched for Masayuki Suzuki the other day, it came up. 
    AA: Related videos, you work fast. 
    AC: "That's right. Thanks to that, I'm indulging in nostalgic songs from the '80s." 
    AA: "It becomes enjoyable, doesn't it? Like, oh that happened, or something like that." 
    AC: Yes! There were some really nostalgic songs, and the music shows were nostalgic too. 
    AA: I don't really understand the current music programs, so seeing something like that makes me happy. 
    AC: Me too. When I watched the video of the night hit studio, it had a strong Showa era feel. 
    AA: Why does nostalgia make us feel this strange way? 
    AC: The memories of that time come flooding back with the songs, right? Like the theme songs of dramas. 
    AA: Theme song of the drama! It totally feels like that. 
    AC: That's right! When you spend time at home today, check out some nostalgic songs! 
    AA: I will do that, thank you!
    """

    personality_traits = """
    'Openness': 2.0833332538604736
    AC tend to favor routine and familiar experiences over novelty and variety. AC prefer practical, straightforward solutions and are likely more conservative in AC tastes and views. This might make AC more comfortable in structured environments but less inclined to seek out creative or unconventional paths.
    'Conscientiousness': 3.75
    AC exhibit a moderate level of conscientiousness, suggesting AC are reliable and responsible but not overly meticulous. AC strike a balance between planning and spontaneity, likely managing AC tasks efficiently without becoming overly rigid. This balance helps in maintaining productivity without excessive stress.
    'Extraversion': 3.1666667461395264
    AC are relatively reserved but can be sociable and outgoing in the right settings. While AC might enjoy social interactions, AC also value your alone time. This balanced approach helps AC recharge without feeling overwhelmed by constant social demands, making AC a versatile companion.
    'Agreeableness': 3.6666667461395264
    AC are generally kind and cooperative, but AC also know when to assert yourself. This trait allows AC to maintain harmonious relationships while standing up for AC own needs and opinions. AC tend to be supportive and considerate, which makes AC a trusted friend and colleague.
    'Neuroticism': 6.666666507720947
    AC experience emotions intensely and may be prone to stress and anxiety. This sensitivity can make AC highly empathetic and aware of others' feelings, but it might also mean AC struggle with self-doubt and worry. Learning coping strategies could help AC manage stress more effectively, enhancing AC overall well-being and resilience.
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
    Here, AC and AA are their respective designations. Now I will provide you with AC's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with AC playing the role of the Human and AA playing the role of the Computer. Specifically, you need to transform AC's utterances based on AC's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AA's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, AC and AA are their respective designations. Now I will provide you with AC's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with AC playing the role of the Human and AA playing the role of the Computer. Specifically, you need to transform AC's utterances based on AC's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform AA's utterances into a Computer style, also without altering the content and meaning.  

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

