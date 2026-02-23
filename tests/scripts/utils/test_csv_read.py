import pandas as pd

df = pd.read_csv("data/games.csv", nrows=5, index_col=False)

print("Columns in DataFrame:")
print(df.columns.tolist())
print("\nFirst row - Developers and Genres:")
print(df[["Developers", "Genres"]].head(1))
