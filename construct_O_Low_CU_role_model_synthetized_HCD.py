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
        Here, CU and CA are their respective designations. Now I will provide you with CU's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
        ## Personality traits score & Personality traits description:  
        {personality_traits}
        Then, I will give you a Human Computer Dialogue based on this Human Human Dialogue, where CU simulates the role of a Human (converting CU's utterances in the original Human Human Dialogue), and CA simulates the role of a Computer (converting CA's utterances in the original Human Human Dialogue). In this simulation, only the style of each utterance will be changed without altering its content and meaning.
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
    return dialogue.count("CU:")

# Example usage
if __name__ == "__main__":
    sample_1_human_human_dialogue = """
    CU: Thank you in advance! 
    CA: Thank you in advance! 
    CU: Have you decided on your lunch for today? 
    CA: "I'm still undecided. I'm thinking about what to choose. Have you decided, <CU>?" 
    CU: Today, my husband and child have gone fishing, so it seems like they will bring back McDonald's on their way home, haha. 
    CA: McDonald's is great! Did you have any specific requests among their menu? 
    CU: I always end up choosing the teriyaki burger. 
    CA: Ah! It's delicious, isn't it!! I'm starting to want to eat it. 
    CU: "It's a limited-time item, but actually my favorite is the Chicken Tatsuta!" 
    CA: Chicken Tatsuta! That's the one they used to advertise in Touch's commercials! 
    CU: That's right! Have you ever eaten it? 
    CA: Actually, I haven't eaten it yet. Is this sold regularly every year like the Tsukimi Burger? 
    CU: For now, I feel like it's being sold once a year! 
    CA: Wow!! I'll try to eat it next time!! 
    CU: I think it was always around spring. The buns are fluffy and delicious, so definitely try them! 
    CA: The buns are different too! I'm looking forward to next spring!! 
    CU: What kind of fast food do you like, <CA>? 
    CA: I quite like the Twister from KFC, and I occasionally buy it as a treat. 
    CU: I know! It's delicious, isn't it? That thing that looks like naan is tasty. 
    CA: That's right! The texture of the dough is indescribable! I love KFC too, but I also love this. 
    CU: I also like Japanese-style cutlet sandwiches. I guess I really like the sweet and savory taste, haha. 
    CA: Ah! There it is! It really is sweet and spicy! There are definitely flavors you prefer, right? 
    CU: Sure. How about having fast food today as well? (laughs) 
    CA: Talking about it made me want to go buy some! Should I go to McDonald's or KFC? 
    CU: Let's do that. It's Obon, and it's nice to take it easy. 
    CA: I will consider it as having a meal together with our ancestors. 
    CU: Indeed. Our ancestors might also be pleased with the rare food. 
    CA: "Hehehe. That would be nice. By the way, there were also people who liked Twister. Maybe I'll go buy it." 
    CU: I see. The weather looks bad, but please be careful and take care. 
    CA: Thank you very much. Let's talk again!
    """

    sample_2_human_human_dialogue = """
    CU: Hello! 
    CA: Hello! 
    CU: Recently, there's been a lot of strange weather, it's scary, isn't it? 
    CA: Really. Even though the rainy season has ended, it's been nothing but rain, and it also pours heavily, doesn't it? 
    CU: There are damages in various places, you know. Was your place okay? 
    CA: I am fine, thanks. How about you, <CU>? 
    CU: I was also fortunately okay. But it's scary to think about what would happen if water came here. 
    CA: Really. It gives me the chills when I watch TV. Do you usually take any disaster prevention measures, not just for rain? 
    CU: "I have prepared an emergency evacuation bag." 
    CA: It's prepared, isn't it! 
    CU: Yes, sort of. But since I don't regularly review the contents, it's no good. 
    CA: "Just having it makes a big difference! I need to prepare something that can be taken out too." 
    CU: At my house, we just put things like flashlights, portable toilets, water, and non-perishable food in a regular backpack. 
    CA: A portable toilet will be necessary, right? If we can't flush water. 
    CU: "Yes. If there is a water outage, it would be very inconvenient. It's really scary to imagine." 
    CA: I used it without thinking, but I realized I should be prepared. 
    CU: That's right. It seems like it's better to always keep water in the bathtub as well. 
    CA: "There are various things you can devise, I'd like to start with those kinds of things." 
    CU: I thought I would also review various things! 
    CA: As for the measures we are taking now, it is just stocking canned food, but what kind of canned food do you like, <CU>? 
    CU: "The most convenient thing to use is probably canned mackerel." 
    CA: Saba can! It's nutritious, isn't it? 
    CU: That's right. And then there's the usual things like corn and tuna. 
    CA: Yeah, yeah. It's really great that both fish and vegetables can be preserved in cans. 
    CU: That's right. But the best thing is not having the opportunity to use emergency supplies! 
    CA: Really! If you are prepared, you have no worries, so I want to keep it as a charm. 
    CU: That's right. It seems like abnormal weather will continue to occur! 
    CA: Praying for safety and taking measures, right? 
    CU: Yes, let's both do our best to stay prepared. 
    CA: Let's talk again!
    """

    personality_traits = """
    CU is someone who enjoys some degree of novelty and creativity, though they balance this with a preference for routine and familiarity. 
    They are generally conscientious and reliable, often organized and mindful of details in their tasks and responsibilities. 
    CU is sociable and outgoing, finding energy and enjoyment in social interactions and activities. 
    They exhibit a good level of agreeableness, being cooperative and considerate in their interactions with others, though they still maintain their own perspective. 
    Finally, CU experiences a fair amount of emotional variability, often feeling anxious or stressed, but they manage to maintain overall functionality despite these fluctuations.
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
    Here, CU and CA are their respective designations. Now I will provide you with CU's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with CU playing the role of the Human and CA playing the role of the Computer. Specifically, you need to transform CU's utterances based on CU's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CA's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_2_dialogue_transformation_prompt = f"""
    Now I will provide you with a Human Human Dialogue as follows:  
    ## Human Human Dialogue:  
    {sample_2_human_human_dialogue}
    Here, CU and CA are their respective designations. Now I will provide you with CU's Big Five Personality Traits scores (7-point scale) and corresponding personality traits descriptions as follows:  
    ## Personality traits score & Personality traits description:  
    {personality_traits}
    Additionally, I will now provide you with Additional Knowledge (regarding differences between Human Human Dialogue and Human Computer Dialogue) as follows:  
    ## Additional Knowledge:  
    {additional_knowledge}
    Now, I need you to perform a Task where you transform this Human Human Dialogue into a Human Computer Dialogue, with CU playing the role of the Human and CA playing the role of the Computer. Specifically, you need to transform CU's utterances based on CU's Personality Traits & Personality Traits Description and Additional Knowledge, changing only the style while preserving the content and meaning. Likewise, you need to transform CA's utterances into a Computer style, also without altering the content and meaning.  

    **Important!!!** Your final output format must strictly follow the format of the provided Human Human Dialogue, and you must directly output the transformed new dialogue without including any additional title or text in your response!!!
    """

    sample_1_human_computer_dialogue = llm_response(sample_1_dialogue_transformation_prompt)

    sample_1_human_human_ct_count = count_ct_occurrences(sample_1_human_human_dialogue)
    sample_1_human_computer_ct_count = count_ct_occurrences(sample_1_human_computer_dialogue)

    sample_1_dialogue_transformation_human_feedback = """
    """

    sample_1_regenerated_human_computer_dialogue = evaluate_dialogue(sample_1_human_human_dialogue, sample_1_human_computer_dialogue, personality_traits, additional_knowledge, sample_1_dialogue_transformation_human_feedback)

    print('Final sample 1 HCD: ', sample_1_regenerated_human_computer_dialogue)

    sample_2_human_computer_dialogue = llm_response(sample_2_dialogue_transformation_prompt)

    sample_2_human_human_ct_count = count_ct_occurrences(sample_2_human_human_dialogue)
    sample_2_human_computer_ct_count = count_ct_occurrences(sample_2_human_computer_dialogue)

    sample_2_dialogue_transformation_human_feedback = """
    """

    sample_2_regenerated_human_computer_dialogue = evaluate_dialogue(sample_2_human_human_dialogue, sample_2_human_computer_dialogue, personality_traits, additional_knowledge, sample_2_dialogue_transformation_human_feedback)

    print('Final sample 2 HCD: ', sample_2_regenerated_human_computer_dialogue)

