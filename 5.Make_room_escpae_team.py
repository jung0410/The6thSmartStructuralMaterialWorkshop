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



presenter = '김현수'
all_scores = []

# records라는 딕셔너리의 각 레코드에서 '엄가현'의 배열을 모읍니다.
for rec_key, rec_data in data.items():
    if presenter in rec_data:
        all_scores.append(np.array(rec_data[presenter]))

if all_scores:
    # element-wise 합산
    total = np.sum(all_scores, axis=0)
    # 레코드 수로 나누어 평균 계산 (여기서는 2로 나누는 것과 동일)
    average = total / len(all_scores)
    print(f"총합: {total}")
    print(f"평균: {average}")

    # 가중치를 곱해서 새로운 가중치 평균 계산
    weights = np.array([2, 2, 2, 2.5, 2.5, 2.5, 2.5, 2, 2])
    weighted_average = average * weights
    print(f"가중치 적용 후 평균: {weighted_average}")
else:
    print("해당 발표자의 데이터가 없습니다.")


# 전체 합계를 소수점 둘째 자리로 반올림
total_sum = np.sum(average)
total_sum_rounded = round(total_sum, 2)

weighted= np.sum(weighted_average)
total_weighted_average = round(weighted, 2)
# 항목 번호 (1~9)
items = np.arange(1, len(average) + 1)

# 항목 이름을 사용자 지정 (원하는 이름으로 수정 가능)
item_labels = ['Presentation Attire', 'Presentation Attitude', 'Presentation Effectiveness', 'Research Novelty', 'Research Logic', 'Research Advancement', 'Societal Impact Potential', 'Engagement Potential', 'Answer Precision']

# 각 그룹별 색상 지정:
# 1~3번 항목: 'red'
# 4~7번 항목: 'green'
# 8~9번 항목: 'blue'
group_colors = []
for i in range(len(average)):
    if i < 3:
        group_colors.append('tab:blue')
    elif i < 7:
        group_colors.append('tab:orange')
    else:
        group_colors.append('tab:red')

# 항목 번호 (1부터 9까지)
items = np.arange(1, len(average) + 1)

plt.figure(figsize=(8, 6))
# 각 항목별로 개별 막대를 그립니다.
for i, val in enumerate(average):
    plt.barh(items[i], val, color=group_colors[i], height=0.8)
    plt.text(val + 0.1, items[i], f"{val:.2f}", va="center", ha="left", fontsize=15, fontweight='bold')

# plt.xlabel("Each Grade", fontsize=14, fontweight='bold')
# plt.ylabel("항목", fontsize=14, fontweight='bold')
plt.title(f"Grade: {total_weighted_average:.2f}", fontsize=16, fontweight='bold')
plt.yticks(items, item_labels, fontsize=15,fontweight='bold')
plt.xticks(fontsize=22,fontweight='bold')
# X축 최대값을 7로 설정 (0부터 7까지)
plt.xlim(0, 5.5)

# X축 값이 5인 곳에 점선 그리기
ax = plt.gca()
ax.invert_yaxis()  # y축 순서를 뒤집음 (1번이 위쪽)
yticklabels = ax.get_yticklabels()
for i, label in enumerate(yticklabels):
    if i < 3:
        label.set_color('tab:blue')
    elif i < 7:
        label.set_color('tab:orange')
    else:
        label.set_color('tab:red')

# X축 값이 5인 곳에 점선 그리기
plt.axvline(x=5, color='black', linestyle='--', linewidth=1)


plt.tight_layout()
plt.savefig('../jpgfile/grade.jpg')
plt.show()


print(weighted_average)





# 그룹별로 합산:
# 첫 3개 항목: Appearance
appearance_sum = weighted_average[:3].sum()
# 항목 4~7: Research
research_sum = weighted_average[3:7].sum()
# 항목 8~9: Defence
defence_sum = weighted_average[7:9].sum()

group_sums = np.array([appearance_sum, research_sum, defence_sum])
group_labels = ["Appearance", "Research", "Defence"]
group_colors = ["tab:blue", "tab:orange", "tab:red"]

# 각 그룹의 합계를 슬라이스 내부에 소수점 둘째 자리까지 표시하는 함수
def make_autopct(values):
    def my_autopct(pct):
        total = np.sum(values)
        absolute = pct * total / 100.0
        return f"{absolute:.2f}"
    return my_autopct

plt.figure(figsize=(8, 8))
plt.pie(group_sums, labels=group_labels, colors=group_colors,
        autopct=make_autopct(group_sums), startangle=90,
        textprops={'fontsize': 20, 'fontweight': 'bold'})
# plt.title("2D Pie Chart of Groups", fontsize=20, fontweight='bold')
plt.axis('equal')  # 원형 유지
plt.tight_layout()
plt.savefig('../jpgfile/savefig_pie.jpg')
plt.show()