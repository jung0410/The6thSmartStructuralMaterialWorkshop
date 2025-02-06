import pandas as pd
import numpy as np
import pickle

# 1) Read the Excel file (no header assumed)
file_path = r"C:\Users\Win\Desktop\6thsmart\6th_smartmaterial.xlsx"
df = pd.read_excel(file_path, header=None)

# 2) Build a dictionary for each row.
# The key for each row is: "{1}_{2}_{3}"
##{1}= nickname {2}=university, {3}= Gender
#Save to Key ={신상정보}, dict={각평가정보}
result = {}

for index, row in df[1:].iterrows():
    # print(row)
    # Build the key using values in columns 1, 2, and 3.
    # Using .iloc to ensure we refer to columns by their integer index.
    key = f"{row.iloc[1]}_{row.iloc[2]}_{row.iloc[3]}"

    # Extract data from specific column ranges.
    presenter_1 = row.iloc[4:13].tolist()  # columns 4 ~ 12
    presenter_2 = row.iloc[13:22].tolist()  # columns 13 ~ 21
    presenter_3 = row.iloc[22:31].tolist()  # columns 14 ~ 22
    presenter_4 = row.iloc[31:40].tolist()  # columns 23 ~ 31
    presenter_5 = row.iloc[40:49].tolist()  # columns 32 ~ 40

    # Store the groups in a dictionary.
    result[key] = {
        "presenter_1":  presenter_1,
        "presenter_2": presenter_2,
        "presenter_3": presenter_3,
        "presenter_4": presenter_4,
        "presenter_5": presenter_5
    }
    ##MAX num 5*9 = 45
    ###100/45=2
    weights = np.array([2, 2, 2, 2, 2, 2, 2, 2, 4])

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
        "presenter-1": score1,
        "presenter-2": score2,
        "presenter-3": score3,
        "presenter-4": score4,
        "presenter-5": score5,
    }

    # --- Step 4: Rank the presenters based on their scores ---
    # Sorted in descending order (best score first).
    # ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Store everything in the result dictionary.
    result[key] = {
        "presenter-1": presenter_1,
        "presenter-2": presenter_2,
        "presenter-3": presenter_3,
        "presenter-4": presenter_4,
        "presenter-5": presenter_5,
        "scores": scores  # The weighted average score for each presenter.
    }



# Optionally, print the resulting dictionary to check its structure.
print(result)

output_path = r"C:\Users\Win\Desktop\6thsmart\result.pkl"  # Change the path and file name as needed

with open(output_path, "wb") as f:
    pickle.dump(result, f)

print(f"Result saved to {output_path}")


