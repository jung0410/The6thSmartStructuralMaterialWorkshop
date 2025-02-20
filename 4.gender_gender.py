import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import os
from PIL import Image
import cv2
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

result_path = r'..\pklfile\result.pkl'
schoolname_path = r'..\pklfile\gender.pkl'

###발표자 사진
#### 발표자 이름과 맞춰 jpg파일로 넣어놔야됨
image_folder = r'../presenter_image_file'
data=pd.read_pickle(result_path)
presenter_school =pd.read_pickle(schoolname_path)

print(presenter_school)
presenters =  ["엄가현", "임동규", "김성종", "주수환", "김현수"]
gender_list = ["Male", "Female"]


presenter_images = {}
for presenter in presenters:
    image_path = os.path.join(image_folder, f"{presenter}.jpg")
    if os.path.exists(image_path):
        presenter_images[presenter] = cv2.imread(image_path)  # 이미지 로드
        # cv2.imshow('gray_image', presenter_images[presenter])
        # cv2.waitKey(0)
    else:
        print(f"⚠ 이미지 파일 없음: {image_path}")  # 없는 파일 알림


for presenter in presenters:
    image_path = os.path.join(image_folder, f"{presenter}.jpg")

    if os.path.exists(image_path):
        # ✅ 한글 파일명을 바이너리로 읽고 OpenCV에서 디코딩 처리
        with open(image_path, "rb") as file:
            file_bytes = bytearray(file.read())  # 파일을 바이너리로 읽기
            np_array = np.asarray(file_bytes, dtype=np.uint8)  # NumPy 배열 변환
            presenter_images[presenter] = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # OpenCV에서 이미지 디코딩

        # ✅ 이미지 확인 (테스트 시 주석 해제 가능)
        # cv2.imshow(f"Image - {presenter}", presenter_images[presenter])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    else:
        print(f"⚠ 이미지 파일 없음: {image_path}")  # 없는 파일 알림



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


gender_avg_scores = {}
for gender in gender_total_scores:
    if gender_counts[gender] > 0:
        gender_avg_scores[gender] = {
            presenter: gender_total_scores[gender][presenter] / gender_counts[gender]
            for presenter in presenters
        }
    else:

        gender_avg_scores[gender] = {presenter: None for presenter in presenters}




# DataFrame으로 변환하여 보기 좋게 출력
df_gender_avg = pd.DataFrame(gender_avg_scores).T  # 전치해서 각 행이 학교, 각 열이 presenter가 되도록

#  숫자로 변환 (문자열로 변환된 숫자가 있다면)
df_gender_avg = df_gender_avg.applymap(lambda x: float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else x)

# 데이터프레임 전체에서 Min-Max 정규화 수행 (컬럼별이 아니라 전체 기준)
###여기서 RoW 별로 해야됨!!!
# global_min = df_gender_avg.min().min()  # 데이터프레임 전체에서 최소값 찾기
# global_max = df_gender_avg.max().max()  # 데이터프레임 전체에서 최대값 찾기

# Gender to 발표자에서 가장 점수를 잘 준 점수  : Max :1.0
# Gender to 발표자에서 가장 점수를 낮게 준 점수: Min :0.0
# df_gender_avg = df_gender_avg.applymap(lambda x: (x - global_min) / (global_max - global_min) if isinstance(x, (int, float)) else x)
# ✅ Row별 Min-Max 정규화 적용
df_gender_avg = df_gender_avg.apply(lambda row: (row - row.min()) / (row.max() - row.min()) if row.max() != row.min() else row, axis=1)


# print(df_gender_avg)
# df_gender_avg.rename(columns=gender, inplace=True)

df_gender_avg.index.name = "gender"
df_gender_avg.columns.name = "Presenter"

# print(df_gender_avg)

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
                 loc='center',
                 cellLoc='center',
                 rowLoc='center')


# ✅ **각 Row별 최대값을 빨간색으로 설정**
df_gender_avg_numeric = df_gender_avg.astype(float)  # 문자열을 숫자로 변환
for row_idx in range(len(df_gender_avg_numeric)):
    max_val = df_gender_avg_numeric.iloc[row_idx].max()  # 해당 Row의 최대값 찾기
    for col_idx in range(len(df_gender_avg_numeric.columns)):
        cell_val = df_gender_avg_numeric.iloc[row_idx, col_idx]
        if cell_val == max_val:
            table[(row_idx + 1, col_idx)].set_facecolor("red")  # 빨간색 배경 적용
            table[(row_idx + 1, col_idx)].set_text_props(color="white", weight="bold")  # 폰트 색상 변경



# ✅ 폰트 및 크기 조절
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.00, 1.2)


rows = 3
cols = 5
i = 1

# ✅ 테이블 배경색 스타일 적용




for idx, presenter in enumerate(presenters):
    if presenter in presenter_images:  # 인덱스 초과 방지
        img = presenter_images[presenter]
        ax = fig.add_subplot(rows, cols, i)
        plt.axis("off")
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        i+=1


# 이미지가 테이블 위에 표시되도록 설정
ax.set_zorder(2)
fig.canvas.draw()  # 렌더링 강제 업데이트

output_jpg_path = r'..\jpgfile\gender_avg_scores.jpg'
plt.savefig(output_jpg_path, bbox_inches='tight', dpi=600)  # dpi는 원하는 해상도에 맞게 조절


plt.show()

# 이미지(JPG)로 저장


# print(f"DataFrame 테이블이 JPG 파일로 저장되었습니다: {output_jpg_path}")
