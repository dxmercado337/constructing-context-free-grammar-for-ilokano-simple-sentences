import pandas as pd
import spacy

# 1. Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# 2. Define your file names and column name
input_file = 'english_translation-train-data.xlsx'     # Replace with your input file name
output_file = 'english_tagged_sentences.xlsx' # The file that will be saved
column_name = 'English Translation'          # Replace with the exact column header of your sentences

def tokenize_and_tag_spacy(text):
    """Function to process text, forcing punctuation to be tagged as 'PUNC'."""
    if pd.isna(text):
        return "", ""
    
    doc = nlp(str(text).strip())
    
    # Extract tokens
    tokens = [token.text for token in doc]
    
    # Extract POS tags, replacing punctuation tags with 'PUNC'
    pos_tags = []
    for token in doc:
        if token.is_punct:
            # Force punctuation to show "PUNC"
            pos_tags.append((token.text, "PUNC"))
        else:
            # Keep the standard POS tag (e.g., VB, NN, JJ)
            pos_tags.append((token.text, token.tag_))
    
    return str(tokens), str(pos_tags)

def process_excel():
    print(f"Reading '{input_file}'...")
    try:
        df = pd.read_excel(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find the file '{input_file}'.")
        return
    
    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found.")
        print(f"Available columns are: {list(df.columns)}")
        return

    print("Processing sentences (Tokenization & Custom PUNC tagging)...")
    
    # Apply the custom tagging function to your sentence column
    df[['Tokens', 'POS_Tags']] = df.apply(
        lambda row: pd.Series(tokenize_and_tag_spacy(row[column_name])), axis=1
    )

    # Save the updated DataFrame to a new Excel file
    df.to_excel(output_file, index=False)
    print(f"Success! Output saved to '{output_file}'")

if __name__ == "__main__":
    process_excel()
