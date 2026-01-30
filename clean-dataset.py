# Clean politfact.csv such that it does not contain any spanish statements, only english ones
# We do this by checking if the tags column contains 'PolitiFact en Español' tag

import pandas as pd
# Load the dataset
data = pd.read_csv('datasets/politifact.csv')
# Filter out rows that contain 'PolitiFact en Español' in the 'tags' column
cleaned_data = data[~data['tags'].str.contains('PolitiFact en Español', na=False)]
# Filter out rows whose verdict is 'np-flip','half-flip','full-flop'
cleaned_data = cleaned_data[~cleaned_data['verdict'].isin(['np-flip', 'half-flip', 'full-flop'])]
# Save the cleaned dataset to a new CSV file    
cleaned_data.to_csv('datasets/politifact-english.csv', index=False)