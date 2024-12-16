import pandas as pd

# Load your Excel file
file_path = 'company.xlsx'  # Replace with the path to your file
df = pd.read_excel(file_path)

# Assuming the email column is named 'Email' (adjust if needed)
df_cleaned = df.dropna(subset=['Email'])

# Save the cleaned DataFrame back to an Excel file
df_cleaned.to_excel('cleaned_file.xlsx', index=False)

print("Rows with 'NA' in the Email column have been removed and saved to 'cleaned_file.xlsx'.")
