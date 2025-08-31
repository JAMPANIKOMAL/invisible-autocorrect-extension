// content.js - The core logic for the Invisible Autocorrect extension.

// --- Main Function ---
// This function sets up the event listener for the entire document.
function setupAutocorrectListener() {
    // We are listening for the 'keyup' event on the whole body. This allows us
    // to capture typing in almost any text input field on any webpage.
    document.body.addEventListener('keyup', handleKeyUp);
}


// --- Load validWords.js ---
// Make sure validWords.js is loaded before content.js in manifest.json

// --- Updated autocorrect logic ---
// Skip autocorrect if the word is valid
function handleKeyUp(event) {
    if (event.key !== ' ') {
        return;
    }
    const activeElement = event.target;
    if (activeElement.tagName.toLowerCase() !== 'textarea' && activeElement.type !== 'text' && activeElement.type !== 'search' && !activeElement.isContentEditable) {
        return;
    }
    const text = activeElement.value || activeElement.textContent;
    const words = text.trim().split(/\s+/);
    if (words.length < 1) {
        return;
    }
    const wordToCheck = words[words.length - 1];
    // Skip autocorrect if word is valid
    if (typeof validWords !== 'undefined' && validWords.has(wordToCheck.toLowerCase())) {
        return;
    }
    if (correctionMap[wordToCheck.toLowerCase()]) {
        const correctedWord = matchCase(wordToCheck, correctionMap[wordToCheck.toLowerCase()]);
        words[words.length - 1] = correctedWord;
        const newText = words.join(' ') + ' ';
        if (activeElement.value !== undefined) {
            activeElement.value = newText;
        } else {
            activeElement.textContent = newText;
            moveCursorToEnd(activeElement);
        }
    }
}

// --- Helper Function: Case Matching ---
// This ensures that if the user typed "Teh", it gets corrected to "The", not "the".
function matchCase(originalWord, correctedWord) {
    if (originalWord.length === 0 || correctedWord.length === 0) {
        return correctedWord;
    }

    // All caps
    if (originalWord === originalWord.toUpperCase()) {
        return correctedWord.toUpperCase();
    }
    
    // Title case (first letter capitalized)
    if (originalWord[0] === originalWord[0].toUpperCase()) {
        return correctedWord.charAt(0).toUpperCase() + correctedWord.slice(1);
    }

    // Default to lowercase
    return correctedWord;
}

// --- Helper Function: Move Cursor ---
// In 'contentEditable' elements, setting textContent moves the cursor to the start.
// This function moves it back to the end for a seamless experience.
function moveCursorToEnd(element) {
    const range = document.createRange();
    const selection = window.getSelection();
    range.selectNodeContents(element);

    // Collapse the range to the end point. 
    // false means collapse to the end, true would be to the start.
    range.collapse(false); 
    
    selection.removeAllRanges();
    selection.addRange(range);
}


// --- Start the Extension ---
// Run the setup function to activate the event listener.
setupAutocorrectListener();
