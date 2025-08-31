# Invisible Autocorrect for Chrome

A lightweight, privacy-focused Chrome extension that provides seamless, phone-like autocorrect. It automatically corrects spelling mistakes as you type—no pop-ups, no underlines.

![Demo GIF showing the extension in action]

## About The Project

This project aims to deliver a simple, "invisible" autocorrect experience in Chrome, similar to smartphones. Unlike other writing assistants, it avoids visual distractions and manual suggestion acceptance.

**How is it different?**  
It works silently: spelling errors are corrected instantly when you press the spacebar, keeping your workflow uninterrupted.

## Acknowledgements

Developed with help from Google's Gemini for code generation, project structure, and documentation.

## Key Features

- **Truly Invisible:** No underlines, pop-ups, or suggestion boxes.
- **Instant Correction:** Typos fixed automatically after each word.
- **Privacy First:** Works offline; no data leaves your device.
- **Lightweight & Fast:** Pure JavaScript for minimal impact.
- **Open Source:** Inspect, modify, and contribute freely.

## How It Works

A content script is injected into web pages, listening for keyup events in text areas and editable fields.

1. Detects the word typed before the spacebar.
2. Checks an internal offline dictionary for common misspellings.
3. Instantly replaces misspelled words if found.

All corrections happen instantly for a smooth typing experience.

## Installation & Usage (from GitHub)

Since it's not on the Chrome Web Store, install manually:

**Download:**
- Click the green `Code` button on GitHub.
- Select `Download ZIP`.
- Unzip the folder.

**Load in Chrome:**
- Go to `chrome://extensions`.
- Enable Developer mode (top-right).
- Click `Load unpacked` (top-left).
- Select the unzipped project folder.

**Start Typing!**  
The extension is now active. Visit any site with a text box and type—autocorrect works automatically.

## Future Improvements

This project is evolving. Planned features:

- [ ] Expand the dictionary for more misspellings.
- [ ] Add UI to enable/disable on specific sites.
- [ ] Allow custom words in the dictionary.

Feel free to fork and contribute!
