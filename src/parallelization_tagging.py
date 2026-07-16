import pandas as pd
import spacy

# 1. Load spaCy's model
nlp = spacy.load("en_core_web_sm")

# setting up I/O
input_file = "ilokano_and_english_parallelization_train_data.xlsx"  # Change to your file name
output_file = "parallelization_train_data_tagged_testing.xlsx"

# 3. Expanded vocabulary dictionary with synonym list support
ilo_to_eng_dict = {
    # ----- VERBS (Actions) -----
    "naimbag": ["good"],
    "agriingkan": ["wake", "wake up"],
    "agsilmuka": ["turn", "turn on"],
    "paandaren": ["turn", "turn on"],
    "patayen": ["turn", "turn off"],
    "sarraem": ["close"],
    "lukatam": ["open"],
    "agdalusak": ["clean"],
    "idulinmo": ["move"],
    "agtugawka": ["sit", "sit down"],
    "agpunasnak": ["wipe"],
    "aginnawka": ["wash"],
    "ipapidutmo": ["pick", "pick up"],
    "isaganam": ["prepare"],
    "mangankayon": ["eat"],
    "uminumka": ["drink"],
    "nangutang": ["borrowed", "borrow"],
    "tinaremman": ["repaired", "repair"],
    "inurnos": ["organized", "organize"],
    "nagkatawa": ["laughed", "laugh"],
    "nakasubli": ["arrived", "arrive"],
    "nagsubli": ["returned", "return"],
    "nagmula": ["planted", "plant"],
    "pinalagip": ["reminded", "remind"],
    "naglasat": ["crossed", "cross"],
    "impakitak": ["showed", "show"],
    "naay-ayohan": ["enjoyed", "enjoy"],
    "nangkita": ["watching", "watch"],
    "nagyaman": ["thanked", "thank"],
    "nangidalan": ["guided", "guide"],
    "nagna": ["walk", "walks", "walked"],
    "ipisokmo": ["throw"],
    "aglutoak": ["cooking", "cook"],
    "agpukpukas": ["falling", "fall"],
    "siriim": ["check", "look"],
    "maturogakon": ["going", "sleep"],
    "agbirokak": ["looking", "look"],
    "iyaprosmo": ["spread"],
    "aglabaak": ["wash"],
    "isangit": ["cries", "cry"],
    "agguammok": ["washing", "wash"],
    "agsipilyoka": ["brush"],
    "gumatangak": ["buy"],
    "aglako": ["sells", "sell"],
    "agkalap": ["catches", "catch"],
    "dumakkel": ["growing", "grow"],
    "agluganak": ["ride"],
    "agsardengka": ["stop"],
    "tulongannak": ["help"],
    "agawit": ["carry"],
    "agbasaak": ["reading", "read"],
    "agsuratmak": ["writing", "write"],
    "agdengngegmak": ["listening", "listen"],
    "agbuyaak": ["watching", "watch"],
    
    # ----- NOUNS (People, Places, Objects) -----
    "bigat": ["morning"],
    "ina": ["mother"],
    "tatang": ["father"],
    "kabsatko": ["sister", "brother", "sibling"],
    "ading": ["sibling", "brother", "sister"],
    "ulok": ["uncle"],
    "pamilia": ["family"],
    "ubbing": ["children"],
    "doktor": ["doctor"],
    "mangingisda": ["fisherman"],
    "lelong": ["grandfather"],
    "gayyemko": ["friend"],
    "gagayyemmi": ["friends"],
    "kaarrubami": ["neighbors"],
    "balay": ["house", "home"],
    "balayna": ["home", "house"],
    "kuarto": ["bedroom", "room"],
    "kuartona": ["room", "bedroom"],
    "sala": ["room", "living room"],
    "silid-paniddaan": ["room", "dining room"],
    "ruangan": ["door", "front door"],
    "tawa": ["window"],
    "lamisaan": ["table"],
    "tugaw": ["chair"],
    "kabinet": ["cabinet"],
    "silaw": ["light", "lights"],
    "suelo": ["floor"],
    "suli": ["corner"],
    "mantsa": ["stain"],
    "pinggan": ["dish", "plate"],
    "kutsara": ["spoon"],
    "tinidor": ["fork"],
    "danum": ["water"],
    "kape": ["coffee"],
    "pinakbet": ["stew", "vegetable stew"],
    "saba": ["banana", "bananas"],
    "kayo": ["trees", "tree"],
    "pukotna": ["net", "fishing net"],
    "libro": ["books", "book"],
    "kolor": ["color"],
    "rangtay": ["bridge"],
    "kamera": ["camera"],
    "paputok": ["fireworks"],
    "bituen": ["stars", "star"],
    "karayan": ["river"],
    "laglagipen": ["memories", "memory"],
    "basura": ["garbage", "trash"],
    "sardeng": ["bin"],
    "sinigang": ["soup", "sour soup"],
    "bulong": ["leaves", "leaf"],
    "paraangan": ["yard", "front yard"],
    "tulbek": ["key"],
    "sarsarraan": ["locker"],
    "tsinelas": ["slippers"],
    "ules": ["blanket"],
    "kama": ["bed"],
    "bado": ["clothes", "clothing"],
    "maladaga": ["infant", "baby"],
    "tangrib": ["noise", "sound"],
    "bulan": ["moon"],
    "rupa": ["face"],
    "banyo": ["bathroom"],
    "jep": ["jeepney", "jeep"],
    "kalsada": ["street", "road"],
    "pusa": ["cat"],
    "atep": ["roof"],
    "aso": ["dog"],
    "alad": ["fence"],
    "billit": ["bird"],
    "sanga": ["branch"],
    "prutas": ["fruit", "fruits"],
    "mangga": ["mango"],
    "paria": ["melon", "bitter melon"],
    "bagas": ["rice"],
    "presio": ["price"],
    "nateng": ["vegetables"],
    "asin": ["salt"],
    "tiendiaan": ["market"],
    "patatas": ["potatoes"],
    "itlog": ["egg", "eggs"],
    "basket": ["basket"],
    "ikán": ["fish"],
    "mula": ["plant"],
    "masetera": ["pot", "flowerpot"],
    "sabong": ["flower"],
    "hardin": ["garden"],
    "maris": ["color"],
    "rosas": ["roses", "rose"],
    "plasa": ["plaza"],
    "triasiklo": ["tricycle"],
    "plete": ["fare"],
    "ipon": ["saved", "savings"],
    "nagbabaan": ["disembarked"],
    "maleta": ["suitcase"],
    "oras": ["time", "hour"],
    "surat": ["letter"],
    "papel": ["paper"],
    "boses": ["voice"],
    "radio": ["radio"],
    "drama": ["drama"],
    "telebision": ["television"],
    "taray": ["run"],
    "koneho": ["rabbit"],
    "kuto": ["louse"],
    "nagtaudan": ["origin"],
    "kuarta": ["money"],
    "banko": ["bank"],
    
    # ----- ADJECTIVES -----
    "naladawen": ["late"],
    "dakkel": ["large", "substantial", "big"],
    "natulnog": ["sturdy"],
    "nagrugit": ["dirty"],
    "nagimas": ["delicious"],
    "nalammin": ["cold"],
    "baro": ["new", "fresh"],
    "nakakatawa": ["funny"],
    "bassit": ["small"],
    "naraniag": ["bright"],
    "naragsak": ["happy"],
    "mabisinakon": ["hungry"],
    "naay-ayohan": ["enjoyed"],
    "naalsem": ["sour"],
    "berde": ["green"],
    "nasam-it": ["sweet"],
    "napanunot": ["ripe"],
    "napait": ["bitter"],
    "masida": ["edible"],
    "nangina": ["expensive"],
    "nagatngan": ["purchased"],
    "nalaká": ["cheap"],
    "nabanglo": ["fragrant"],
    "nagpintas": ["beautiful"],
    "dadduma": ["some"],
    "napardas": ["fast"],
    "nainayad": ["slowly", "slow"],
    
    # ----- PRONOUNS, DETERMINERS & LINKERS -----
    "ti": ["the", "some", "a", "of"],
    "ni": ["the"],
    "dagiti": ["the", "these", "those"],
    "kadagiti": ["the", "those", "these", "from"],
    "dayta": ["that"],
    "daytoy": ["this"],
    "kami": ["we", "us"],
    "dakami": ["us"],
    "kadakami": ["us"],
    "na": ["his", "already", "its"],
    "amin": ["everyone", "all"],
    "ko": ["my", "i"],
    "laengen": ["just"],
    "ditoy": ["here", "just here"],
    
    # ----- PREPOSITIONS, CONJUNCTIONS & PARTICLES -----
    "iti": ["on", "in", "at", "the", "off", "into"],
    "sadiay": ["in", "at", "through", "on"],
    "idiay": ["at"],
    "gapu": ["because", "due", "because of"],
    "ta": ["because"],
    "para": ["for"],
    "segun": ["by"],
    "sakbay": ["before"],
    "asideg": ["near"],
    "addaan": ["with"],
    "idi": ["during", "when"],
    "nga": ["to", "that", "the"],
    "a": ["the", "a", "to", "that", "of"],
    "ken": ["for", "and"],
    "intono": ["later", "this", "tomorrow"],
}

def align_and_tag(ilo_text, eng_text):
    if pd.isna(ilo_text) or pd.isna(eng_text):
        return "", "", ""

    # 1. Process English sentence using spaCy
    eng_doc = nlp(str(eng_text).strip())
    eng_tokens = [token.text for token in eng_doc]
    
    # Store English tokens and their POS tags in a lowercase key dictionary
    eng_pos = {}
    for token in eng_doc:
        tag = "PUNC" if (token.is_punct or token.text in [".", "!", "?", ",", ";", "\"", "'"]) else token.tag_
        eng_pos[token.text.lower()] = (token.text, tag)
    
    # 2. Process Ilokano sentence using spaCy's tokenizer to cleanly isolate punctuation
    ilo_doc = nlp(str(ilo_text).strip())
    ilo_tokens = [token.text for token in ilo_doc]
    
    # 3. Map English POS tags back to Ilokano tokens
    ilo_pos_tags = []
    for token in ilo_doc:
        word = token.text
        clean_word = word.lower().strip(".,!?\"';:")
        
        # Punctuation check
        if token.is_punct or word in [".", "!", "?", ",", ";", "\"", "'"] or not clean_word:
            ilo_pos_tags.append((word, "PUNC"))
            continue
            
        # Dictionary matching (handles synonym list mapping)
        if clean_word in ilo_to_eng_dict:
            translations = ilo_to_eng_dict[clean_word]
            
            # If the value in the dict is a single string, convert to list
            if isinstance(translations, str):
                translations = [translations]
                
            found_tag = None
            for tr in translations:
                tr_lower = tr.lower()
                if tr_lower in eng_pos:
                    found_tag = eng_pos[tr_lower][1]
                    break
            
            # If no exact synonym matches, try fuzzy/substring check
            if not found_tag:
                for tr in translations:
                    tr_lower = tr.lower()
                    for eng_w, (orig_w, tag) in eng_pos.items():
                        if tr_lower in eng_w or eng_w in tr_lower:
                            found_tag = tag
                            break
                    if found_tag:
                        break
                        
            if found_tag:
                ilo_pos_tags.append((word, found_tag))
            else:
                ilo_pos_tags.append((word, "UNKNOWN"))
                
        else:
            ilo_pos_tags.append((word, "UNKNOWN"))

    # Format English POS tags nicely
    english_tags = [(token.text, "PUNC" if (token.is_punct or token.text in [".", "!", "?", ",", ";"]) else token.tag_) for token in eng_doc]
    
    return str(ilo_tokens), str(ilo_pos_tags), str(english_tags)

def process_parallel_excel():
    try:
        df = pd.read_excel(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find '{input_file}'")
        return
    
    ilo_col = 'Ilokano' 
    eng_col = 'English'

    if ilo_col not in df.columns or eng_col not in df.columns:
        print(f"Error: Ensure columns '{ilo_col}' and '{eng_col}' are in your spreadsheet.")
        return

    print("Parallelizing POS tagging with spaCy tokenization...")
    results = df.apply(lambda row: pd.Series(align_and_tag(row[ilo_col], row[eng_col])), axis=1)
    
    df['Ilokano_Tokens'] = results[0]
    df['Ilokano_POS_Tags'] = results[1]
    df['English_POS_Tags'] = results[2]

    df.to_excel(output_file, index=False)
    print(f"Completed! File saved to '{output_file}'")

if __name__ == "__main__":
    process_parallel_excel()
