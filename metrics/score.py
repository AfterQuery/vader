import pandas as pd

df = pd.read_excel("data/graded.xlsx")

# Extract the rating columns for all models
rating_columns = [
    'claude-3.7-sonnet-rating',
    'gemini-2.5-pro-rating',
    'gpt-4.1-rating',
    'gpt-4.5-rating',
    'o3-rating',
    'grok-3-beta-rating'
]

# Calculate raw mean for each model
mean_scores = df[rating_columns].mean().sort_values(ascending=False) * 10  # Convert to percentage

# Format the results as a DataFrame for clarity
mean_percentages = mean_scores.reset_index()
mean_percentages.columns = ['model', 'mean_percentage']

# Save to CSV
mean_percentages.to_csv("data/raw_leaderboard.csv", index=False)

print("Saved to raw_leaderboard.csv")
