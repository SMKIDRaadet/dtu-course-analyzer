// background.js
// In Manifest V3, we don't need to load data here anymore because 
// we inject it directly into the page via manifest.json.

// Update listener for the browser action button (top right icon)
chrome.action.onClicked.addListener((tab) => {
    // Open the dashboard when the icon is clicked
    chrome.tabs.create({ url: chrome.runtime.getURL('db.html') });
});