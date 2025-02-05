import pandas as pd
import json

# persona_description = """
# 1. I am a student.
# 2. I am from Saitama Prefecture.
# 3. I don't eat breakfast every day.
# 4. I go for a walk every day.
# 5. I often go to the convenience store.
# 6. I type fast.
# 7. I have a poor memory.
# 8. I have a clear goal for my future.
# 9. I can find something fun every day.
# 10. I am very particular about the things I like.
# """

# personality_traits = """
# 'Openness': 5.25
# AH are a curious and imaginative individual who values creativity and new experiences. AH are likely to enjoy exploring different cultures, ideas, and unconventional ways of thinking. This trait makes AH open-minded and receptive to change, often leading AH to seek out diverse perspectives and innovative solutions in your personal and professional life.
#
# 'Conscientiousness': 3.1666667461395264
# AH are moderately organized and reliable, though AH may sometimes struggle with maintaining consistent levels of discipline and planning. While AH are capable of setting goals and working towards them, AH might occasionally procrastinate or find it challenging to stay focused. In AH's relationships and work, AH's balance spontaneity with responsibility, often adapting to the needs of the moment.
#
# 'Extraversion': 3.3333332538604736
# AH have a balanced level of extraversion, enjoying social interactions and activities while also valuing AH's alone time. AH can be outgoing and energetic in social settings, but AH also appreciate periods of solitude to recharge. This trait allows AH to be adaptable in various social environments, maintaining meaningful connections without feeling overwhelmed.
#
# 'Agreeableness': 4.166666507720947
# AH are generally kind, empathetic, and cooperative, often striving to maintain harmony in AH's relationships. AH value getting along with others and are usually willing to compromise to avoid conflicts. This trait helps AH build strong, supportive relationships, though AH might sometimes prioritize others' needs over AH's own.
#
# 'Neuroticism': 4.416666507720947
# AH are somewhat prone to experiencing stress and emotional fluctuations, often feeling worried or anxious about potential problems. While this can sometimes lead to moments of self-doubt or moodiness, it also means AH are highly aware of AH's emotions and can be very empathetic towards others. AH's sensitivity allows AH to navigate and respond to emotional situations thoughtfully.
# """

def construct_template(dialogue, dialogue_topic):
    system = (
        f"AH-Computer Dialogue Topic: {dialogue_topic}"
    )
    instruction = (
        f"You are an exceptional role player. Your designated character's name is AH. Your task is to engage in a dialogue with a computer based on a given topic. Your final output should be in the form of a complete dialogue, with two roles (User and Assistant). The User represents the character AH that you are playing, and the Assistant represents the computer. Avoid repetitive utterance for both User and Assistant side. Remember, your output should only contain the dialogue and no any other information."
    )
    label = (
        f"{dialogue}"
    )

    return system, instruction, label

def construct_template(dialogue, dialogue_topic):
    system = (
        f"AH's Personality Traits Score & Description: {personality_traits} \n"
        f"AH-Computer Dialogue Topic: {dialogue_topic}"
    )
    instruction = (
        f"You are an exceptional role player. Your designated character's name is AH. I will provide you with AH's Big Five Personality Traits scores (on a 7-point scale) along with descriptions for each trait. Your task is to engage in a dialogue with a computer based on a given topic. Your final output should be in the form of a complete dialogue, with two roles (User and Assistant). The User represents the character AH that you are playing, and the Assistant represents the computer. Remember, your output should only contain the dialogue and no any other information."
    )
    label = (
        f"{dialogue}"
    )

    return system, instruction, label

def load_my_dataset():

  df = pd.read_csv("adapted_dialogues_processed_cleaned.csv", skiprows=1, header=None)

  instructions = []
  inputs = []
  outputs = []

  for index, row in df.iterrows():
      dialogue = row[1]
      dialogue_topic = row[2]

      system, instruction, label = construct_template(dialogue, dialogue_topic)

      inputs.append(system)
      instructions.append(instruction)
      outputs.append(label)

      # 将数据打包成 JSONL 格式
      jsonl_data = []
      for inst, inp, out in zip(instructions, inputs, outputs):
          jsonl_data.append({
              "instruction": inst,
              "input": inp,
              "output": out
          })

      with open("training_dataset.jsonl", "w", encoding="utf-8") as file:
          for item in jsonl_data:
              file.write(json.dumps(item, ensure_ascii=False) + "\n")

# 调用加载数据集的函数并存储为 JSONL
load_my_dataset()