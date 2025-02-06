import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

output_path = r"C:\Users\Win\Desktop\6thsmart\result.pkl"
data=pd.read_pickle(output_path)


# Let's compute the average score for each presenter across all keys.
presenters = ["presenter-1", "presenter-2", "presenter-3", "presenter-4", "presenter-5"]
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
    print(f"{presenter}: {avg:.2f}")


sorted_averages = sorted(average_scores.items(), key=lambda x: x[1], reverse=True)

# Define ordinal labels for the top 5 presenters.
ordinals = ["1st", "2nd", "3rd", "4th", "5th"]

# Print each presenter's rank and score.
for i, (presenter, avg) in enumerate(sorted_averages):
    # Use the corresponding ordinal label for this rank.
    print(f"{ordinals[i]}: {presenter} with score {avg:.2f}")


# Create a new figure for the ranking image.
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')  # Turn off the axis

# Title for the image
ax.set_title("Presenter Ranking", fontsize=25, fontweight='bold', pad=20)

# Starting y-coordinate for text (using axis coordinates, where (0,0) is bottom-left)
y_start = 0.8
line_spacing = 0.12  # spacing between lines

# Print each rank line.
for i, (presenter, avg) in enumerate(sorted_averages):
    text_line = f"{ordinals[i]}: {presenter} with score {avg:.2f}"
    ax.text(0.1, y_start - i * line_spacing, text_line,
            fontsize=20, transform=ax.transAxes)

# Add a congratulatory message for the winner.
winner = sorted_averages[0][0]  # The best presenter.
winner_message = f"Winner: Congratulations {ordinals[0]}: {winner}!"
ax.text(0.1, y_start - len(sorted_averages) * line_spacing - 0.1, winner_message,
        fontsize=20, fontweight='bold', color='red', transform=ax.transAxes)

plt.rcParams['font.family'] = 'Arial'
plt.tight_layout()
plt.show()


def generate_winner_certificate(sorted_averages,grade):

    # Extract the top presenter
    top_presenter, top_score = sorted_averages[(grade-1)]


    # Create a figure for the winner announcement
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')  # Hide axes

    # Add a grand title
    if grade == 1:
        gradest= "1st"
    elif grade ==2:
        gradest = "2nd"
    elif grade ==3:
        gradest = "3rd"

    ax.set_title(f" Congratulations!\n\nthe 6th Smart Structal Maaterial Workshop\n {gradest} Prize", fontsize=24, fontweight='bold', color='black', pad=20)

    # Add a gold crown emoji and the winner's name in a luxurious font style
    winner_text = f"️ {top_presenter} ️"
    ax.text(0.5, 0.8, winner_text, fontsize=50, fontweight='bold', ha='center', va='center', color='darkblue', transform=ax.transAxes)

    # Add the score in an elegant way
    score_text = f"Achieved an Outstanding Score of {top_score:.4f}"
    ax.text(0.5, 0.4, score_text, fontsize=20, fontweight='bold', ha='center', va='center', color='black', transform=ax.transAxes)

    # Decorate with golden laurel leaves at the bottom

    # Show the final image
    plt.rcParams['font.family'] = 'Arial'
    plt.tight_layout()
    plt.show()


generate_winner_certificate(sorted_averages, 1)
generate_winner_certificate(sorted_averages, 2)
generate_winner_certificate(sorted_averages, 3)