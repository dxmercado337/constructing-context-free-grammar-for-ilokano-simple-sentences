import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

# setting up I/O
input_file = "ilokano_and_english_parallelization_train_data.xlsx"  # Change to your file name
output_file = "parallelization_train_data_tagged.xlsx"

# dictionaries for the Ilokano POS Tagging to be based on context from English POS Tagging
# example -> <ilokano_word>:<english_word>
ilo_to_eng_dict = {
    # VERBS 
    "agriingkan": "wake",
    "agsilmuka": "turn", "paandaren": "turn",
    "sarraem": "close",
    "lukatam": "open",
    "agdalusak": "clean",
    "idulinmo": "move",
    "agtugawka": "sit",
    "agpunasnak": "wipe",
    "aginnawka": "wash",
    "ipapidutmo": "pick",
    "isaganam": "prepare",
    "mangankayon": "eat",
    "uminumka": "drink",
    "nangutang": "borrowed",
    "tinaremman": "repaired",
    "inurnos": "organized",
    "nagkatawa": "laughed",
    "nakasubli": "arrived", "nagsubli": "returned",
    "nagmula": "planted",
    "pinalagip": "reminded",
    "naglasat": "crossed",
    "impakitak": "showed",
    "naay-ayohan": "enjoyed", "nangkita": "watching",
    "nagyaman": "thanked",
    "nangidalan": "guided",
    "nagna": "walk",
    
    # NOUNS 
    "ina": "mother", "tatang": "father", "kabsatko": "sister", "ulok": "uncle",
    "pamilia": "family", "ubbing": "children", "doktor": "doctor", 
    "mangingisda": "fisherman", "gayyemko": "friend", "gagayyemmi": "friends", "kaarrubami": "neighbors",
    "balay": "house", "kuarto": "bedroom", "sala": "room", "silid-paniddaan": "room",
    "ruangan": "door", "tawa": "window", "lamisaan": "table", "tugaw": "chair", "kabinet": "cabinet",
    "silaw": "light", "suelo": "floor", "suli": "corner", "mantsa": "stain",
    "pinggan": "dish", "kutsara": "spoon", "tinidor": "fork",
    "danum": "water", "kape": "coffee", "pinakbet": "stew", "saba": "banana", "kayo": "trees",
    "pukotna": "net", "libro": "books", "kolor": "color", "rangtay": "bridge", "kamera": "camera",
    "paputok": "fireworks", "bituen": "stars", "karayan": "river", "bigat": "morning",
    
    # ADJECTIVES 
    "naimbag": "good",
    "naladawen": "late",
    "dakkel": "large",
    "natulnog": "sturdy",
    "nagrugit": "dirty",
    "nagimas": "delicious",
    "nalammin": "cold",
    "baro": "new", "fresh": "baro",
    "nakakatawa": "funny",
    "bassit": "small",
    "naraniag": "bright",
    "naragsak": "happy",
    "mabisinakon": "hungry",
    
    # PRONOUNS & DETERMINERS
    "ti": "the", "ni": "the", "dagiti": "the", # 'dagiti' is plural 'the'
    "dayta": "that",
    "daytoy": "this",
    "kami": "we", "dakami": "us", "kadakami": "us",
    "na": "his", 
    "amin": "everyone",
    
    # PREPOSITIONS, CONJUNCTIONS & PARTICLES
    "iti": "on", "sadiay": "in", "idiay": "at", 
    "gapu": "because", "ta": "because",
    "para": "for",
    "segun": "by",
    "sakbay": "before",
    "asideg": "near",
    "nga": "to", "a": "the" # 'nga' and 'a' act as linkers, sometimes aligning to 'to' or ignored
}

def align_and_tag(ilo_text, eng_text):
    if pd.isna(ilo_text) or pd.isna(eng_text):
        return "", "", ""

    # Process English sentence using spaCy
    eng_doc = nlp(str(eng_text).strip())
    
    # Store English tokens and their POS tags
    eng_tokens = [token.text for token in eng_doc]
    eng_pos = {token.text.lower(): (token.text, "PUNC" if token.is_punct else token.tag_) for token in eng_doc}
    
    # Create simple word tokenizer for Ilokano
    ilo_tokens = str(ilo_text).strip().split() # Simple whitespace split, or use spacy.blank("xx")
    
   # Map English POS tags back to Ilokano tokens
    ilo_pos_tags = []
    
    # Get a list of just the English tags for fallback positioning
    eng_tag_list = [token.tag_ for token in eng_doc if not token.is_punct]
    
    for i, token in enumerate(ilo_tokens):
        clean_token = token.lower().strip(".,!?\"'")
        
        # 1. Punctuation
        if token in [".", "!", "?", ",", ";", "\"", "'"]:
            ilo_pos_tags.append((token, "PUNC"))
            
        # 2. Dictionary Match (Highly Accurate)
        elif clean_token in ilo_to_eng_dict:
            translated_word = ilo_to_eng_dict[clean_token]
            if translated_word in eng_pos:
                ilo_pos_tags.append((token, eng_pos[translated_word][1]))
            else:
                ilo_pos_tags.append((token, "UNKNOWN"))
                
        # 3. Position Fallback (Guess based on order if dictionary fails)
        else:
            # If we don't know the word, but we have a tag at roughly the same position in the English sentence
            if i < len(eng_tag_list):
                 ilo_pos_tags.append((token, f"{eng_tag_list[i]}*")) # Added an asterisk * so you know it was guessed
            else:
                 ilo_pos_tags.append((token, "UNKNOWN"))

    # Return strings formatted for Excel
    english_tags = [(token.text, "PUNC" if token.is_punct else token.tag_) for token in eng_doc]
    return str(ilo_tokens), str(ilo_pos_tags), str(english_tags)

def process_parallel_excel():
    try:
        df = pd.read_excel(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find '{input_file}'")
        return
    
    # Ensure column names exist (Adjust headers as they appear in your Excel sheet)
    ilo_col = 'Ilokano' 
    eng_col = 'English'

    if ilo_col not in df.columns or eng_col not in df.columns:
        print(f"Error: Ensure columns '{ilo_col}' and '{eng_col}' are in your spreadsheet.")
        return

    print("Parallelizing POS tagging...")
    
    # Apply parallel mapping
    results = df.apply(lambda row: pd.Series(align_and_tag(row[ilo_col], row[eng_col])), axis=1)
    df['Ilokano_Tokens'] = results[0]
    df['Ilokano_POS_Tags'] = results[1]
    df['English_POS_Tags'] = results[2]

    df.to_excel(output_file, index=False)
    print(f"Completed! File saved to '{output_file}'")

if __name__ == "__main__":
    process_parallel_excel()
