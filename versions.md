Project Version History
This document outlines the development journey and different versions of the Invisible Autocorrect extension.

Version 1.0: The Proof of Concept
The initial version was a proof-of-concept built to test the core functionality of instant, invisible autocorrection.

Dictionary: Used a small, manually curated JavaScript object (correctionMap) containing about 20-50 common English misspellings.

Logic: The content.js script would check the last typed word against this small map and perform a replacement if a match was found.

Goal: To prove that the user experience of seamless correction was possible in a browser environment.

Version 2.0: The AI-Powered Model
This version represents a significant leap forward, moving from a manual list to a comprehensive, programmatically generated dictionary.

Data Source: It uses a master frequency dictionary (specifically, frequency_dictionary_en_82_765.txt from the SymSpell project) which contains over 82,000 correctly spelled English words and their usage frequency.

Model Building: A Python script (model_builder.py) was created to act as an offline "AI model builder." This script:

Reads the master dictionary.

For each correct word, it generates all possible misspellings that are one "edit distance" away (e.g., insertions, deletions, substitutions, and transpositions).

It then builds a massive reverse-lookup map, where each potential typo maps back to its correct word.

It intelligently resolves conflicts (where a typo could map to multiple words) by choosing the word with the higher frequency in the master dictionary.

Result: This process generates a final dictionary.js file with a correction map containing hundreds of thousands of entries, making the extension far more powerful and capable of correcting a vast range of real-world typing errors.