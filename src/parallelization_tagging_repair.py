import pandas as pd
import ast
import tkinter as tk
from tkinter import filedialog

# 1. Open a pop-up window to let you select your EXCEL (.xlsx) file
root = tk.Tk()
root.withdraw()  # Hide the main empty Tkinter window

print("Select your broken Excel (.xlsx) file in the pop-up window...")
file_path = filedialog.askopenfilename(
    title="Select the broken Ilokano-English Excel file",
    filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
)

if not file_path:
    print("No file was selected. Exiting script.")
    exit()

# Load the selected Excel file
# (pandas will use the openpyxl engine automatically for .xlsx)
df = pd.read_excel(file_path)

# 2. Build a dictionary of known correct tags from the file itself
known_tags = {}
for col in ['Ilokano_POS_Tags', 'English_POS_Tags']:
    if col in df.columns:
        for row in df[col].dropna():
            try:
                tokens_list = ast.literal_eval(row)
                for word, tag in tokens_list:
                    if tag != 'UNKNOWN':
                        known_tags[word.lower()] = tag
            except (ValueError, SyntaxError):
                continue

# 3. Add manual fallback fixes for the root words missing from your database
manual_fallbacks = {
    'adda': 'VB',
    'uneg': 'NN',
    'rabaw': 'NN',
    'madamdama': 'RB',
    'panagtrabaho': 'NN',
    'panagpasiar': 'NN',
    'sabado': 'NNP',
    'ania': 'WP',
    'mano': 'WP',
    'ayanna': 'WP',
    'nasam': 'JJ',
    'it': 'JJ', 
    'alas': 'NN',
    'dies': 'CD',
    'agas': 'VB',
    'asog': 'NN',
    'silid': 'NN',
    'paniddaan': 'NN'
}
known_tags.update(manual_fallbacks)

# 4. Function to repair individual rows
def repair_tags(tags_str):
    if pd.isna(tags_str):
        return tags_str
    try:
        tokens_list = ast.literal_eval(tags_str)
        repaired_list = []
        for word, tag in tokens_list:
            if tag == 'UNKNOWN':
                lookup_word = word.lower()
                fixed_tag = known_tags.get(lookup_word, 'UNKNOWN')
                
                if fixed_tag == 'UNKNOWN':
                    if lookup_word.startswith('ag') or lookup_word.startswith('ma'):
                        fixed_tag = 'VB'
                    elif lookup_word.startswith('na'):
                        fixed_tag = 'JJ'
                    else:
                        fixed_tag = 'NN'
                        
                repaired_list.append((word, fixed_tag))
            else:
                repaired_list.append((word, tag))
        return str(repaired_list)
    except (ValueError, SyntaxError):
        return tags_str

# Apply the repair functions to the tag columns if they exist
if 'Ilokano_POS_Tags' in df.columns:
    df['Ilokano_POS_Tags'] = df['Ilokano_POS_Tags'].apply(repair_tags)
if 'English_POS_Tags' in df.columns:
    df['English_POS_Tags'] = df['English_POS_Tags'].apply(repair_tags)

# 5. Export directly back to an Excel file (.xlsx)
output_path = "Fixed_Ilokano_English_Parallel_Data.xlsx"
df.to_excel(output_path, index=False)

print(f"\n🎉 Success! The repaired Excel file has been saved to: {output_path}")
