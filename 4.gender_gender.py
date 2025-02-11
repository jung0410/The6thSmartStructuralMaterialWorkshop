import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

result_path = r"C:\Users\Win\Desktop\6thsmart\result.pkl"
schoolname_path = r"C:\Users\Win\Desktop\6thsmart\gender.pkl"

data=pd.read_pickle(result_path)
presenter_school =pd.read_pickle(schoolname_path)

print(presenter_school)
presenters = ["presenter-1", "presenter-2", "presenter-3", "presenter-4", "presenter-5"]

gender_list = ["Male", "Female"]


gender_total_scores = {gender: {presenter: 0 for presenter in presenters} for gender in gender_list}
gender_counts = {gender: 0 for gender in gender_list}


for key, entry in data.items():
    # key에서 학교명을 추출
    gender = key.split('_')[2]
    if gender in gender_total_scores:
        scores = entry["scores"]
        for presenter in presenters:
            gender_total_scores[gender][presenter] += scores[presenter]
        gender_counts[gender] += 1

# 각 학교별로 평균 점수를 계산
gender_avg_scores = {}
for school in gender_total_scores:
    if gender_counts[school] > 0:
        gender_avg_scores[school] = {
            presenter: gender_total_scores[school][presenter] / gender_counts[gender]
            for presenter in presenters
        }
    else:

        gender_avg_scores[school] = {presenter: None for presenter in presenters}




# DataFrame으로 변환하여 보기 좋게 출력
df_gender_avg = pd.DataFrame(gender_avg_scores).T  # 전치해서 각 행이 학교, 각 열이 presenter가 되도록
print(df_gender_avg)
# df_gender_avg.rename(columns=gender, inplace=True)

df_gender_avg.index.name = "gender"
df_gender_avg.columns.name = "Presenter"

print(df_gender_avg)

# 소수점 두 자리로 포맷 (문자열로 변환)
df_gender_avg = df_gender_avg.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)


# 도와줘 gpt야
# #####예쁘게 좀 만들어봐
fig, ax = plt.subplots(figsize=(8, 4))  # 크기는 원하는 대로 조정하세요
# 한글 폰트 설정 한국말꺠져서 사용함
plt.rcParams["font.family"] = "Malgun Gothic"
# Axes의 테두리와 축을 제거
ax.axis('tight')
ax.axis('off')

# DataFrame 내용을 테이블로 그리기
# cellText: 각 셀의 텍스트, colLabels: 열 라벨, rowLabels: 행 라벨
table = ax.table(cellText=df_gender_avg.values,
                 colLabels=df_gender_avg.columns,
                 rowLabels=df_gender_avg.index,
                 loc='center')

# 폰트 크기와 테이블 크기를 조절 (원하는 대로 수정)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(0.88, 1.2)

# 실제 데이터 셀은 (i, j)에서 i>=1, j>=1 입니다.
cells = table.get_celld()
# df_school_avg의 행 수와 열 수

# 조건에 해당하는 셀 정보를 저장할 리스트 생성
red_cells = []

plt.show()

# 리스트를 DataFrame으로 변환
df_red_cells = pd.DataFrame(red_cells)

print(df_red_cells)
# 이미지(JPG)로 저장
output_jpg_path = r"C:\Users\Win\Desktop\6thsmart\school_avg_scores.jpg"
plt.savefig(output_jpg_path, bbox_inches='tight', dpi=300)  # dpi는 원하는 해상도에 맞게 조절


# print(f"DataFrame 테이블이 JPG 파일로 저장되었습니다: {output_jpg_path}")
