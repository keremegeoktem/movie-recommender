import pandas as pd

# Load both files
numeric = pd.read_csv("user_movie_matrix.csv", index_col=0)
titled = pd.read_csv("user_movie_matrix_with_titles.csv", index_col=0)

# Step 1: Confirm shape
print("Shape match:", numeric.shape == titled.shape)

# Step 2: Confirm user IDs (index)
print("Row index match:", numeric.index.equals(titled.index))

# Step 3: Confirm all values are the same
# Sort columns to align if needed
values_match = numeric.values.round(6).tolist() == titled.values.round(6).tolist()
print("All rating values match:", values_match)

# Step 4: Optional — show first 5 column name differences
print("\nColumn names in original:")
print(numeric.columns[:5])

print("\nColumn names in titled version:")
print(titled.columns[:5])