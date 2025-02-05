import pandas as pd

# Load the dataset
df = pd.read_parquet('combined_data.parquet')

# Filter English language rows
df = df[df['language'] == 'English']

# Filter rows where turn equals 10
turn_6_dialogues = df[df['turn'] == 6]

# Randomly sample 300 rows
sampled_dialogues = turn_6_dialogues.sample(n=2000, random_state=95)  # random_state ensures reproducibility

# Save the sampled data to a new Parquet file
sampled_dialogues.to_parquet('sampled_turn_6_dialogues.parquet', index=False)