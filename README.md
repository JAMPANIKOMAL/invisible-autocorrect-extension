# Invisible Autocorrect - Chrome Extension

## About The Project

Invisible Autocorrect is a Chrome extension that brings seamless, phone-like autocorrect to your browser. Unlike traditional spell checkers that underline errors and require manual correction, this extension instantly and invisibly fixes thousands of common typing mistakes as soon as you press the spacebar.

The correction engine uses an AI model to intelligently predict intended words from typos, leveraging a comprehensive analysis of the English language.

## Getting Started

Follow these steps to set up the extension locally.

### Prerequisites

- Google Chrome browser

### Installation

#### Download the Project

1. Click the green **Code** button on this GitHub page.
2. Select **Download ZIP**.
3. Unzip the downloaded folder to a memorable location on your computer.

#### Load the Extension in Chrome

1. Open Chrome and go to `chrome://extensions`.
2. Enable **Developer mode** (toggle in the top-right corner).
3. Click **Load unpacked** (top-left).
4. Select the unzipped project folder.

The extension is now installed and active! Test it by typing a common misspelling (e.g., `teh` or `wierd`) in any text box and pressing the spacebar.

## Manual Overrides

The autocorrect engine also supports a large set of manual corrections via `override.js`. This file contains thousands of curated typo-to-correction mappings, ensuring that even rare or tricky misspellings are fixed instantly. The Python builder script (`model_builder.py`) automatically loads and applies these overrides when generating the dictionary.

## Output Files

- `dictionary.js`: The main autocorrect correction map, including both AI-generated and manual overrides.
- `validWords.js`: A JavaScript Set containing all valid words used for autocorrect whitelisting and validation.

## Acknowledgements

- Developed with assistance from Google's Gemini.
- The AI model leverages word frequency data from the [SymSpell project](https://github.com/wolfgarbe/SymSpell).

# Note on Dictionary Coverage

The current autocorrect dictionary (`dictionary.js`) is a minimal, optimized 12 MB file. It covers the most common English words and typos for fast performance, but may not autocorrect every possible misspelling.

If you want a more comprehensive autocorrect experience, you can generate a full dictionary by running the commented code block at the end of `model_builder.py`. This will create a much larger dictionary covering nearly all possible corrections, but may impact extension performance and load time.
