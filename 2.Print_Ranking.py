import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import sys
sys.stdout.reconfigure(encoding='utf-8')  # 출력 인코딩 UTF-8 설정


output_path = r'../pklfile/result.pkl'
# 저장할 폴더 경로와 파일 이름을 별도로 정의합니다.
save_dir = r'../jpgfile'

data=pd.read_pickle(output_path)

plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False  # 마이너스(-) 기호 깨짐 방지


presenters = ["임동규", "주수환", "김현수", "김성종", "엄가현"]
total_scores = {presenter: 0 for presenter in presenters}
num_entries = len(data)

for key, data in data.items():
    scores = data["scores"]
    for presenter in presenters:
        total_scores[presenter] += scores[presenter]
        # print(scores[presenter])

# Compute averages
average_scores = {presenter: total_scores[presenter] / num_entries for presenter in presenters}

# print("Average scores across all keys:")
# print(average_scores)
for presenter, avg in average_scores.items():
    print(f"{presenter}: {avg:.2f}")


sorted_averages = sorted(average_scores.items(), key=lambda x: x[1], reverse=True)
ordinals = ["1st", "2nd", "3rd", "4th", "5th"]

for i, (presenter, avg) in enumerate(sorted_averages):
    print(f"{ordinals[i]}: {presenter} with score {avg:.2f}")


fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')  # Turn off the axis

# Title
ax.set_title("Presenter Ranking", fontsize=25, fontweight='bold', pad=20)

y_start = 0.8
line_spacing = 0.12

# Print each rank
for i, (presenter, avg) in enumerate(sorted_averages):
    text_line = f"{ordinals[i]}: {presenter} with score {avg:.2f}"
    ax.text(0.1, y_start - i * line_spacing, text_line,
            fontsize=20, transform=ax.transAxes)

# Add a congratulatory message
winner = sorted_averages[0][0]  # The best presenter.
winner_message = f"Winner: Congratulations {ordinals[0]}: {winner}!"
ax.text(0.1, y_start - len(sorted_averages) * line_spacing - 0.1, winner_message,
        fontsize=20, fontweight='bold', color='red', transform=ax.transAxes)

# plt.rcParams['font.family'] = 'Arial'
filename = f"Ranking_ALL.jpg"
save_path = os.path.join(save_dir, filename)

plt.tight_layout()
plt.savefig(save_path)
plt.show()


def generate_winner_certificate(sorted_averages,grade):
    top_presenter, top_score = sorted_averages[(grade-1)]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')  # Hide axes


    if grade == 1:
        gradest= "1st"
    elif grade ==2:
        gradest = "2nd"
    elif grade ==3:
        gradest = "3rd"

    ax.set_title(f" Congratulations!\n\nthe 6th Smart Structal Maaterial Workshop\n {gradest} Prize", fontsize=24, fontweight='bold', color='black', pad=20)

    winner_text = f"️ {top_presenter} ️"
    ax.text(0.5, 0.8, winner_text, fontsize=50, fontweight='bold', ha='center', va='center', color='darkblue', transform=ax.transAxes)


    score_text = f"Achieved an Outstanding Score of {top_score:.2f}"
    ax.text(0.5, 0.4, score_text, fontsize=20, fontweight='bold', ha='center', va='center', color='black', transform=ax.transAxes)

    # Show the final image
    # plt.rcParams['font.family'] = 'Arial'
    filename = f"Ranking{grade}.jpg"
    save_path = os.path.join(save_dir, filename)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()


generate_winner_certificate(sorted_averages, 1)
generate_winner_certificate(sorted_averages, 2)
generate_winner_certificate(sorted_averages, 3)