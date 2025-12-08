// Import the data file. In Manifest V3, background is a Service Worker.
// 'data' variable is defined in db/data.js
try {
    importScripts('/db/data.js');
} catch (e) {
    console.error("Failed to load data.js:", e);
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    // Ensure we have a course ID request
    if (request.getInfo) {
        const courseId = request.getInfo;
        const responsePayload = {};

        // Check if data was loaded and course exists
        if (typeof data !== 'undefined' && courseId in data) {
            responsePayload[courseId] = data[courseId];
        } else {
            responsePayload[courseId] = false;
        }

        // Send the data back to the contentscript
        sendResponse(responsePayload);
    }
    
    // Return true to indicate we might respond asynchronously 
    // (though here we are synchronous, it's good practice in MV3)
    return true;
});

// Update listener for the browser action button (top right icon)
chrome.action.onClicked.addListener((tab) => {
    chrome.tabs.create({ url: chrome.runtime.getURL('db.html') });
});