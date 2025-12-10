// background.js - Chrome Version
// We don't handle data here anymore. The content script handles it via direct injection.

// Update listener for the browser action button (top right icon)
chrome.action.onClicked.addListener((tab) => {
    chrome.tabs.create({ url: chrome.runtime.getURL('db.html') });
});