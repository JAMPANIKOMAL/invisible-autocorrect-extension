# Project Version History

This document outlines the development journey and versions of the Invisible Autocorrect extension.

## Version 1.0: Proof of Concept

- **Dictionary:** Small, manually curated JavaScript object (`correctionMap`) with 20–50 common English misspellings.
- **Logic:** `content.js` checks the last typed word against the map and replaces it if a match is found.
- **Goal:** Demonstrate seamless autocorrection in a browser environment.

## Version 2.0: AI-Powered Model

- **Data Source:** Uses `frequency_dictionary_en_82_765.txt` from the SymSpell project (82,000+ correctly spelled English words with frequency).
- **Model Building:** A Python script (`model_builder.py`) acts as an offline AI model builder:
    - Reads the master dictionary.
    - Generates all possible misspellings one edit distance away (insertions, deletions, substitutions, transpositions).
    - Builds a reverse-lookup map: each typo maps to its correct word.
    - Resolves conflicts by selecting the word with higher frequency.
- **Result:** Produces `dictionary.js` with a correction map containing hundreds of thousands of entries, enabling robust real-world autocorrection.

## Version 2.1: Manual Overrides and Valid Words

- **Manual Overrides:** Added support for a large curated set of typo corrections via `override.js`. These are loaded and merged into the correction map during dictionary generation.
- **Valid Words Output:** The builder now generates `validWords.js`, a JavaScript Set of all valid words for use in the extension.
