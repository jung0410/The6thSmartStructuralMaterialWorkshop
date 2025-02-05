import pandas as pd
import numpy as np
import pickle

output_path = r"C:\Users\Win\Desktop\6thsmart\result.pkl"
data=pd.read_pickle(output_path)


# Let's compute the average score for each presenter across all keys.
presenters = ["presenter_1", "presenter_2", "presenter_3", "presenter_4", "presenter_5"]
total_scores = {presenter: 0 for presenter in presenters}
num_entries = len(data)

# Iterate over each key in result
for key, data in data.items():
    scores = data["scores"]
    for presenter in presenters:
        total_scores[presenter] += scores[presenter]
        print(scores[presenter])

# Compute averages
average_scores = {presenter: total_scores[presenter] / num_entries for presenter in presenters}

print("Average scores across all keys:")
print(average_scores)
for presenter, avg in average_scores.items():
    print(f"{presenter}: {avg:.4f}")


sorted_averages = sorted(average_scores.items(), key=lambda x: x[1], reverse=True)

# Define ordinal labels for the top 5 presenters.
ordinals = ["1st", "2nd", "3rd", "4th", "5th"]

# Print each presenter's rank and score.
for i, (presenter, avg) in enumerate(sorted_averages):
    # Use the corresponding ordinal label for this rank.
    print(f"{ordinals[i]}: {presenter} with score {avg:.4f}")