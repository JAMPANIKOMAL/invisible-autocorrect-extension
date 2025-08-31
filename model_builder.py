import re
import json
import os

# --- Configuration ---
MASTER_DICTIONARY_FILE = 'assets/frequency_dictionary_en_82_765.txt'
OVERRIDE_JS_FILE = 'override.js'
OUTPUT_DICTIONARY_FILE = 'dictionary.js'
OUTPUT_VALIDWORDS_FILE = 'validWords.js'
MAX_EDIT_DISTANCE = 1
TOP_N_WORDS = 30000
MAX_TYPOS_PER_WORD = 20
SHORT_WORD_WHITELIST = set([
    "is", "by", "to", "in", "on", "at", "an", "it", "as", "be", "he", "we", "me", "my", "do", "go", "so", "no", "up", "us", "if", "or", "of", "am"
])

def generate_edits(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    adjacency = {
        'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wsdr', 'f': 'drtgvc',
        'g': 'ftyhbv', 'h': 'gyujnb', 'i': 'ujko', 'j': 'huikmn', 'k': 'jiolm', 'l': 'kop',
        'm': 'njk', 'n': 'bhjm', 'o': 'iklp', 'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'wedxz',
        't': 'rfgy', 'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu', 'z': 'asx'
    }
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in adjacency.get(R[0], '')]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def load_override_js(filepath):
    # Reads override.js and extracts the correctionMap as a Python dict
    with open(filepath, 'r', encoding='utf-8') as f:
        js = f.read()
    # Find the correctionMap object
    match = re.search(r'const\s+correctionMap\s*=\s*\{(.+?)\};', js, re.DOTALL)
    if not match:
        print('Could not find correctionMap in override.js')
        return {}
    obj_body = match.group(1)
    # Remove comments and trailing commas
    obj_body = re.sub(r'//.*', '', obj_body)
    obj_body = re.sub(r',\s*}', '}', obj_body)
    # Add quotes to keys and values if missing
    obj_body = re.sub(r'([\w-]+):', r'"\1":', obj_body)
    obj_body = re.sub(r':\s*([\w-]+)', r':"\1"', obj_body)
    # Wrap in braces
    json_str = '{' + obj_body + '}'
    try:
        correction_map = json.loads(json_str)
    except Exception as e:
        print('Error parsing override.js:', e)
        correction_map = {}
    return correction_map

def build_ai_dictionary():
    print("--- Starting AI Model Builder ---")
    master_word_freq = {}
    correction_map = {}
    # Step 1: Load master dictionary
    print(f"1. Loading master dictionary: '{MASTER_DICTIONARY_FILE}'...")
    try:
        with open(MASTER_DICTIONARY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    word = parts[0].lower()
                    if word.isalpha():
                        master_word_freq[word] = int(parts[1])
    except FileNotFoundError:
        print(f"\n--- ERROR ---")
        print(f"Master dictionary file not found: '{MASTER_DICTIONARY_FILE}'")
        return
    print(f"   Loaded {len(master_word_freq)} unique words.")
    sorted_words = sorted(master_word_freq.items(), key=lambda x: x[1], reverse=True)
    filtered_words = [(w, f) for w, f in sorted_words if len(w) > 2 or w in SHORT_WORD_WHITELIST]
    top_words = dict(filtered_words[:TOP_N_WORDS])
    print(f"   Using top {TOP_N_WORDS} words (length > 2 or whitelisted) for corrections.")
    # Step 2: Generate edits
    print(f"\n2. Generating misspellings (Edit Distance: {MAX_EDIT_DISTANCE})...")
    print("   This may take a few minutes...")
    total_words = len(top_words)
    for i, (correct_word, frequency) in enumerate(top_words.items()):
        if i % 1000 == 0:
            print(f"   Processed {i} / {total_words} words...")
        typos = list(generate_edits(correct_word))[:MAX_TYPOS_PER_WORD]
        for typo in typos:
            if typo in SHORT_WORD_WHITELIST:
                continue
            if typo not in top_words:
                if typo not in correction_map:
                    correction_map[typo] = correct_word
                else:
                    existing_correction = correction_map[typo]
                    if top_words.get(correct_word, 0) > top_words.get(existing_correction, 0):
                        correction_map[typo] = correct_word
    # Step 3: Load and apply manual overrides
    print(f"\n3. Loading manual overrides from '{OVERRIDE_JS_FILE}'...")
    if os.path.exists(OVERRIDE_JS_FILE):
        manual_overrides = load_override_js(OVERRIDE_JS_FILE)
        for typo, correction in manual_overrides.items():
            correction_map[typo] = correction
        print(f"   Applied {len(manual_overrides)} manual overrides.")
    else:
        print(f"   No override.js file found. Skipping manual overrides.")
    print(f"   Generated {len(correction_map)} unique corrections.")
    # Step 4: Write output files
    print(f"\n4. Writing output files...")
    try:
        with open(OUTPUT_DICTIONARY_FILE, 'w', encoding='utf-8') as outfile:
            outfile.write("const correctionMap={")
            first = True
            for misspelled, corrected in correction_map.items():
                misspelled_escaped = misspelled.replace('"', '\"')
                corrected_escaped = corrected.replace('"', '\"')
                if not first:
                    outfile.write(",")
                outfile.write(f'"{misspelled_escaped}":"{corrected_escaped}"')
                first = False
            outfile.write("};")
        with open(OUTPUT_VALIDWORDS_FILE, 'w', encoding='utf-8') as vfile:
            vfile.write("const validWords=new Set([")
            first = True
            for word in top_words.keys():
                word_escaped = word.replace('"', '\"')
                if not first:
                    vfile.write(",")
                vfile.write(f'"{word_escaped}"')
                first = False
            vfile.write("]);")
    except Exception as e:
        print(f"   Error writing files: {e}")
        return
    print("\n--- Success! ---")
    print(f"AI model building complete.\nYour new dictionary has been saved to '{OUTPUT_DICTIONARY_FILE}' and valid words to '{OUTPUT_VALIDWORDS_FILE}'.")

if __name__ == "__main__":
    build_ai_dictionary()
