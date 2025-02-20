import pandas as pd
import numpy as np
import pickle
import os

#1)엑셀 장소
####값 고정 test 파일
# file_path = r"C:/Users/Win/OneDrive/Lab_공유/2025 워크샵/python파일/6th_smartmaterial.xlsx"
####랜덤 test 파일
file_path = r"../6th_smartmaterial_Random.xlsx"
df = pd.read_excel(file_path,sheet_name=0, header=None)

#2)저장 장소
output_path =r"../pklfile/result.pkl"
output_path_sheet1 = r'../pklfile/schoolname.pkl'
output_path_sheet2 =r'../pklfile/gender.pkl'


# The key for each row is: "{1}_{2}_{3}"
##{1}= nickname {2}=university, {3}= Gender
#Save to Key ={신상정보}, dict={각평가정보}
result = {}


for index, row in df[1:].iterrows():
    # print(row)
    # Build the key using values in columns 1, 2, and 3.
    # Using .iloc to ensure we refer to columns by their integer index.
    key = f"{row.iloc[1]}_{row.iloc[2]}_{row.iloc[3]}"

    # Extract data
    presenter_1 = row.iloc[4:13].tolist()  # columns 4 ~ 12
    presenter_2 = row.iloc[13:22].tolist()  # columns 13 ~ 21
    presenter_3 = row.iloc[22:31].tolist()  # columns 14 ~ 22
    presenter_4 = row.iloc[31:40].tolist()  # columns 23 ~ 31
    presenter_5 = row.iloc[40:49].tolist()  # columns 32 ~ 40

    # Store the groups in a dictionary.
    result[key] = {
         "엄가현": presenter_1,
        "임동규": presenter_2,
        "김성종": presenter_3,
        "주수환": presenter_4,
        "김현수": presenter_5,
    }
    ##MAX num 5*9 = 45
    ###100/45=2
    ### 5(배점수)* (가중치 * 문제수) =100 이 되어야 함
    ## 발표태도  30 = 5 * (2*3 = 6)  (1,2,3) =(2,2,2,)
    ## 발표내용  50 = 5 * (2.5*4 = 10) (4,5,6,7)
    ## Q&A      20 = 5 * (2*2 = 4) (8,9)
    weights = np.array([2, 2, 2, 2.5, 2.5, 2.5, 2.5, 2, 2])

    # Convert lists to NumPy arrays (and cast to float) to allow numerical operations.
    p1 = np.array(presenter_1, dtype=float)
    p2 = np.array(presenter_2, dtype=float)
    p3 = np.array(presenter_3, dtype=float)
    p4 = np.array(presenter_4, dtype=float)
    p5 = np.array(presenter_5, dtype=float)

    # --- Step 3: Compute the weighted average for each presenter ---
    score1 = np.round(np.sum(p1 * weights),1)
    score2 = np.round(np.sum(p2 * weights),1)
    score3 = np.round(np.sum(p3 * weights),1)
    score4 = np.round(np.sum(p4 * weights),1)
    score5 = np.round(np.sum(p5 * weights),1)

    # Create a dictionary mapping each presenter to its computed score.
    scores = {
        "엄가현": score1,
        "임동규": score2,
        "김성종": score3,
        "주수환": score4,
        "김현수": score5,
    }

    result[key] = {
        "엄가현": presenter_1,
        "임동규": presenter_2,
        "김성종": presenter_3,
        "주수환": presenter_4,
        "김현수": presenter_5,
        "scores": scores  # The weighted average score for each presenter.
    }

df1 = pd.read_excel(file_path,sheet_name=1)
result_sheetschool = {}
for index, row in df1.iterrows():
    presenter = row['prensenter_name']
    print(presenter)
    school = row['school_name']
    result_sheetschool[presenter] = school

print(result)
print(result_sheetschool)

df1 = pd.read_excel(file_path,sheet_name=2)
print(df1)
result_gender = {}
for index, row in df1.iterrows():
    presenter = row['prensenter_name']
    gender = row['Gender']
    result_gender[presenter] = gender

def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)  # 파일의 디렉터리 경로 가져오기
    if not os.path.exists(directory):  # 폴더가 없으면
        os.makedirs(directory)  # 폴더 생성
        print(f"디렉터리 생성: {directory}")

# with open(output_path, "wb") as f:
#     pickle.dump(result, f)
#
# print(f"Result saved to {output_path}")
#
# with open(output_path_sheet1, "wb") as f:
#     pickle.dump(result_sheetschool, f)
# print(f"Sheet 1 결과가 {output_path_sheet1} 에 저장되었습니다.")
#
# with open(output_path_sheet2, "wb") as f:
#     pickle.dump(result_gender, f)
# print(f"Sheet 2 결과가 {output_path_sheet2} 에 저장되었습니다.")


for path, data, name in [(output_path, result, "Result"),
                         (output_path_sheet1, result_sheetschool, "Sheet 1"),
                         (output_path_sheet2, result_gender, "Sheet 2")]:
    ensure_directory_exists(path)  # 폴더 확인 및 생성
    with open(path, "wb") as f:
        pickle.dump(data, f)
    print(f"  {name} 결과가 {path} 에 저장되었습니다.")