# Whitelist of common short words that should never be autocorrected
SHORT_WORD_WHITELIST = set([
    "is", "by", "to", "in", "on", "at", "an", "it", "as", "be", "he", "we", "me", "my", "do", "go", "so", "no", "up", "us", "if", "or", "of", "am"
])
# --- For advanced users: Generate a complete dictionary ---
# Uncomment and run the following code block to build a full dictionary covering all words and typos.
# WARNING: The resulting file may be 1 GB+ and is not recommended for regular use!
#
# def build_full_dictionary():
#     print("--- Starting Full Dictionary Build ---")
#     master_word_freq = {}
#     correction_map = {}
#     try:
#         with open(MASTER_DICTIONARY_FILE, 'r', encoding='utf-8') as f:
#             for line in f:
#                 parts = line.strip().split()
#                 if len(parts) == 2:
#                     word = parts[0].lower()
#                     if word.isalpha():
#                         master_word_freq[word] = int(parts[1])
#     except FileNotFoundError:
#         print(f"\n--- ERROR ---")
#         print(f"Master dictionary file not found: '{MASTER_DICTIONARY_FILE}'")
#         print("Please make sure it's in the same folder as this script.")
#         return
#     print(f"   Loaded {len(master_word_freq)} unique words.")
#     total_words = len(master_word_freq)
#     for i, (correct_word, frequency) in enumerate(master_word_freq.items()):
#         if i % 5000 == 0:
#             print(f"   Processed {i} / {total_words} words...")
#         typos = generate_edits(correct_word)
#         for typo in typos:
#             if typo not in master_word_freq:
#                 if typo not in correction_map:
#                     correction_map[typo] = correct_word
#                 else:
#                     existing_correction = correction_map[typo]
#                     if master_word_freq.get(correct_word, 0) > master_word_freq.get(existing_correction, 0):
#                         correction_map[typo] = correct_word
#     print(f"   Generated {len(correction_map)} unique corrections.")
#     try:
#         with open('dictionary_full.js', 'w', encoding='utf-8') as outfile:
#             outfile.write("const correctionMap={")
#             first = True
#             for misspelled, corrected in correction_map.items():
#                 misspelled_escaped = misspelled.replace('"', '\"')
#                 corrected_escaped = corrected.replace('"', '\"')
#                 if not first:
#                     outfile.write(",")
#                 outfile.write(f'"{misspelled_escaped}":"{corrected_escaped}"')
#                 first = False
#             outfile.write("};")
#     except Exception as e:
#         print(f"   Error writing file: {e}")
#         return
#     print("\n--- Success! ---")
#     print("Full dictionary has been saved to 'dictionary_full.js'.")
# model_builder.py
# This script builds an advanced correction dictionary using a frequency list
# and an edit distance algorithm to generate potential misspellings.

import re

# --- Configuration ---

# --- Configuration ---
MASTER_DICTIONARY_FILE = 'assets/frequency_dictionary_en_82_765.txt'
OUTPUT_FILE = 'dictionary.js'
MAX_EDIT_DISTANCE = 1
# Only include corrections for the top N most frequent words
TOP_N_WORDS = 30000  # Adjust this value to approach 12 MB output size
# Limit the number of typos per word (most likely typos)
MAX_TYPOS_PER_WORD = 20

def generate_edits(word):
    """
    Generates likely typos for a word, prioritizing common keyboard mistakes.
    Includes deletions, transpositions, substitutions (adjacent keys), and insertions.
    """
    letters = 'abcdefghijklmnopqrstuvwxyz'
    # QWERTY keyboard adjacency map (simplified)
    adjacency = {
        'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wsdr', 'f': 'drtgvc',
        'g': 'ftyhbv', 'h': 'gyujnb', 'i': 'ujko', 'j': 'huikmn', 'k': 'jiolm', 'l': 'kop',
        'm': 'njk', 'n': 'bhjm', 'o': 'iklp', 'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'wedxz',
        't': 'rfgy', 'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu', 'z': 'asx'
    }
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    # Substitutions: only adjacent keys
    replaces = [L + c + R[1:] for L, R in splits if R for c in adjacency.get(R[0], '')]
    inserts = [L + c + R for L, R in splits for c in letters]
    # Only keep unique typos
    return set(deletes + transposes + replaces + inserts)

def build_ai_dictionary():
    """
    Main function to build the dictionary.
    """
    print("--- Starting AI Model Builder ---")
    
    master_word_freq = {}
    correction_map = {}

    # --- Step 1: Load the Master Dictionary ---
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
        print("Please make sure it's in the same folder as this script.")
        return
    print(f"   Loaded {len(master_word_freq)} unique words.")

    # Sort and keep only the top N most frequent words, skipping short words
    sorted_words = sorted(master_word_freq.items(), key=lambda x: x[1], reverse=True)
    filtered_words = [(w, f) for w, f in sorted_words if len(w) > 2 or w in SHORT_WORD_WHITELIST]
    top_words = dict(filtered_words[:TOP_N_WORDS])
    print(f"   Using top {TOP_N_WORDS} words (length > 2 or whitelisted) for corrections.")

    # --- Step 2: Generate Edits and Build Correction Map ---
    print(f"\n2. Generating misspellings (Edit Distance: {MAX_EDIT_DISTANCE})...")
    print("   This may take a few minutes...")
    
    total_words = len(top_words)
    for i, (correct_word, frequency) in enumerate(top_words.items()):
        if i % 1000 == 0:
            print(f"   Processed {i} / {total_words} words...")

        typos = list(generate_edits(correct_word))
        # Limit the number of typos per word
        typos = typos[:MAX_TYPOS_PER_WORD]

        for typo in typos:
            # Exclude autocorrect for whitelisted short words
            if typo in SHORT_WORD_WHITELIST:
                continue
            if typo not in top_words:
                if typo not in correction_map:
                    correction_map[typo] = correct_word
                else:
                    existing_correction = correction_map[typo]
                    if top_words.get(correct_word, 0) > top_words.get(existing_correction, 0):
                        correction_map[typo] = correct_word
    
    print(f"   Generated {len(correction_map)} unique corrections.")

    # --- Step 3: Write the Output File ---
    print(f"\n3. Writing output file: '{OUTPUT_FILE}'...")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
            # Minified output: no comments, no extra whitespace
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
        # Also write validWords.js
        with open('validWords.js', 'w', encoding='utf-8') as vfile:
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
        print(f"   Error writing file: {e}")
        return

    print("\n--- Success! ---")
    print("AI model building complete.")
    print(f"Your new dictionary has been saved to '{OUTPUT_FILE}'.")

# --- Run the script ---
if __name__ == "__main__":
    build_ai_dictionary()
