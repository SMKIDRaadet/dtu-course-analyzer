chrome.runtime.onMessage.addListener(parseMessage);

function parseMessage(request, sender, sendResponse) {
	let course=request.getInfo
	let rtab=sender.tab.id
	
	var resp={};
	if(course in data){
		resp[course]=data[course]
	} else{
		resp[course]=false
	}
	
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		chrome.tabs.sendMessage(rtab, resp);
	});
}
chrome.browserAction.onClicked.addListener(function(tab) {
	chrome.tabs.create({ url: chrome.runtime.getURL('db.html') });
});
