import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# 어느 컴에서든 작동하도록 상대위치로 폴더경로를 정하면 좋다.
result_path = r'..\pklfile\result.pkl'
schoolname_path = r'..\pklfile\schoolname.pkl'


output_jpg_path = r"..\jpgfile\school_avg_scores.jpg"


data=pd.read_pickle(result_path)
presenter_school =pd.read_pickle(schoolname_path)

print(presenter_school)
# presenters = ["presenter-1", "presenter-2", "presenter-3", "presenter-4", "presenter-5"]

presenters = ["엄가현", "임동규", "김성종", "주수환", "김현수"]

# school_list = ["중앙대학교", "단국대학교", "한양대 에리카", "가천대학교", "유니스트"]
school_list = ["한양대 에리카", "단국대학교", "중앙대학교", "유니스트", "가천대학교"]

school_total_scores = {school: {presenter: 0 for presenter in presenters} for school in school_list}
school_counts = {school: 0 for school in school_list}


for key, entry in data.items():
    # key에서 학교명을 추출
    school = key.split('_')[0]
    if school in school_total_scores:
        scores = entry["scores"]
        for presenter in presenters:
            school_total_scores[school][presenter] += scores[presenter]
        school_counts[school] += 1

# 각 학교별로 평균 점수를 계산
school_avg_scores = {}
for school in school_total_scores:
    if school_counts[school] > 0:
        school_avg_scores[school] = {
            presenter: school_total_scores[school][presenter] / school_counts[school]
            for presenter in presenters
        }
    else:

        school_avg_scores[school] = {presenter: None for presenter in presenters}




# DataFrame으로 변환하여 보기 좋게 출력
df_school_avg = pd.DataFrame(school_avg_scores).T  # 전치해서 각 행이 학교, 각 열이 presenter가 되도록
df_school_avg.rename(columns=presenter_school, inplace=True)

df_school_avg.index.name = "School"
df_school_avg.columns.name = "Presenter"

print(df_school_avg)

# 소수점 두 자리로 포맷 (문자열로 변환)
# df_school_avg = df_school_avg.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
print(df_school_avg)

#  숫자로 변환 (문자열로 변환된 숫자가 있다면)
###전체 상대 변화
# df_school_avg = df_school_avg.applymap(lambda x: float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else x)
### Row별 상대 변화

# 데이터프레임 전체에서 Min-Max 정규화 수행 (컬럼별이 아니라 전체 기준
# global_min = df_school_avg.min().min()  # 데이터프레임 전체에서 최소값 찾기
# global_max = df_school_avg.max().max()  # 데이터프레임 전체에서 최대값 찾기
#
# # 학교 to 학교에서 가장 점수를 잘 준 점수  : Max :1.0
# # 학교 to 학교에서 가장 점수를 낮게 준 점수: Min :0.0
# df_school_avg = df_school_avg.applymap(lambda x: (x - global_min) / (global_max - global_min) if isinstance(x, (int, float)) else x)
#
# # 소수점 2자리로 변환
# df_school_avg = df_school_avg.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)

df_school_avg = df_school_avg.apply(lambda row: (row - row.min()) / (row.max() - row.min()) if row.max() != row.min() else row, axis=1)
df_school_avg = df_school_avg.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)

print(df_school_avg)



# 도와줘 gpt야
#####예쁘게 좀 만들어봐
fig, ax = plt.subplots(figsize=(8, 4))  # 크기는 원하는 대로 조정하세요
# 한글 폰트 설정 한국말꺠져서 사용함
plt.rcParams["font.family"] = "Malgun Gothic"
# Axes의 테두리와 축을 제거
ax.axis('tight')
ax.axis('off')

# DataFrame 내용을 테이블로 그리기
# cellText: 각 셀의 텍스트, colLabels: 열 라벨, rowLabels: 행 라벨
table = ax.table(cellText=df_school_avg.values,
                 colLabels=df_school_avg.columns,
                 rowLabels=df_school_avg.index,
                 loc='center')

# 실제 데이터 셀은 (i, j)에서 i>=1, j>=1 입니다.
cells = table.get_celld()
# df_school_avg의 행 수와 열 수

#대각선 값
diag_indices = list(zip(range(len(df_school_avg)), range(len(df_school_avg.columns))))
diag_values = [df_school_avg.iloc[i, j] for i, j in diag_indices]

# 학교별 자신의 학교에게 준 최댓값, 최솟값 찾기
max_value = max(diag_values)
min_value = min(diag_values)


# 색상 설정 GPT야 부탁해
highlight_color = "#FFD700"  # 대각선 기본 색상 (골드)
max_color = "#FF6347"  # 최댓값 색상 (토마토색)
min_color = "#4682B4"  # 최솟값 색상 (스틸블루)

# 대각선 값(본인 학교몇 점으로 처리했는지 색상 설정)
for (i, j) in diag_indices:
    cell = cells[(i + 1, j)]
    value = df_school_avg.iloc[i, j]
    ###가운데 값만 금색으로 처리
    cell.set_facecolor(highlight_color)
    # if value == max_value:
    #     # cell.set_facecolor(max_color)  # 최댓값
    # elif value == min_value:
    #     # cell.set_facecolor(min_color)  # 최솟값
    # else:
    #     cell.set_facecolor(highlight_color)  # 일반 대각선 값



# ✅ **각 Row별 최대값을 빨간색으로 설정**
df_school_avg_numeric = df_school_avg.astype(float)  # 문자열을 숫자로 변환
for row_idx in range(len(df_school_avg_numeric)):
    max_val = df_school_avg_numeric.iloc[row_idx].max()  # 해당 Row의 최대값 찾기
    for col_idx in range(len(df_school_avg_numeric.columns)):
        cell_val = df_school_avg_numeric.iloc[row_idx, col_idx]
        if cell_val == max_val:
            table[(row_idx + 1, col_idx)].set_facecolor("red")  # 빨간색 배경 적용
            table[(row_idx + 1, col_idx)].set_text_props(color="white", weight="bold")  # 폰트 색상 변경

# 폰트 크기와 테이블 크기를 조절 (원하는 대로 수정)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(0.88, 1.2)



plt.savefig(output_jpg_path, bbox_inches='tight', dpi=300)  # dpi는 원하는 해상도에 맞게 조절
plt.show()

# # 리스트를 DataFrame으로 변환
# df_red_cells = pd.DataFrame(red_cells)

# 이미지(JPG)로 저장
#
#
# plt.close(fig)

# print(f"DataFrame 테이블이 JPG 파일로 저장되었습니다: {output_jpg_path}")
