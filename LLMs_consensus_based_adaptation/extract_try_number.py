import os
import pandas as pd
from statistics import mean

folder_path = 'average_+1_std_aggregation_output_adapted_dialogues'

final_list = []

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)

        df = pd.read_csv(file_path)

        try_numbers = df['Try_Number'].tolist()

        final_list.extend(try_numbers)

average_value = mean(final_list)

output_file = 'average_+1_std_aggregation_try_number.txt'
with open(output_file, 'w') as file:
    file.write("Final List:\n")
    file.write(str(final_list) + "\n\n")
    file.write(f"Average of try_number values: {average_value}\n")