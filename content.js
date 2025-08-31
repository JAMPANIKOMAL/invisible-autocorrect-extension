// content.js - The core logic for the Invisible Autocorrect extension.

// --- Main Function ---
// This function sets up the event listener for the entire document.
function setupAutocorrectListener() {
    // We are listening for the 'keyup' event on the whole body. This allows us
    // to capture typing in almost any text input field on any webpage.
    document.body.addEventListener('keyup', handleKeyUp);
}

// --- Event Handler ---
// This function is called every time a key is released.
function handleKeyUp(event) {
    // 1. Check if the key pressed was the spacebar.
    // The spacebar signals the end of a word, which is our cue to check it.
    if (event.key !== ' ') {
        return; // If it wasn't a space, do nothing.
    }

    // 2. Identify the active typing element.
    // 'event.target' is the HTML element where the typing is happening (e.g., a <textarea>).
    const activeElement = event.target;

    // We only want to run on textareas and specific input types.
    if (activeElement.tagName.toLowerCase() !== 'textarea' && activeElement.type !== 'text' && activeElement.type !== 'search' && !activeElement.isContentEditable) {
        return;
    }

    // 3. Get the word to check.
    const text = activeElement.value || activeElement.textContent;
    
    // Split the text into words. We use a regular expression to better handle multiple spaces.
    const words = text.trim().split(/\s+/);

    if (words.length < 1) {
        return;
    }

    // The word to check is the one right before the space was typed.
    const wordToCheck = words[words.length - 1];

    // 4. Perform the correction.
    // We check if our correctionMap (from dictionary.js) has an entry for this word.
    // The 'correctionMap' variable is available here because 'dictionary.js' was loaded first (as per manifest.json).
    if (correctionMap[wordToCheck.toLowerCase()]) {
        // Find the correct spelling. We handle potential capitalization by matching the case of the original word.
        const correctedWord = matchCase(wordToCheck, correctionMap[wordToCheck.toLowerCase()]);
        
        // Replace the misspelled word with the corrected one.
        words[words.length - 1] = correctedWord;

        // Reconstruct the text and update the input field's value.
        // We add a space at the end to preserve the user's typing flow.
        const newText = words.join(' ') + ' ';

        if (activeElement.value !== undefined) {
             activeElement.value = newText;
        } else {
            activeElement.textContent = newText;
            // For contentEditable divs, we need to move the cursor to the end.
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
