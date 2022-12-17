if(getBrowser() === "Chrome") {
	chrome.extension.onRequest.addListener(parseMessage);
} else {
	browser.runtime.onMessage.addListener(parseMessage);
}

function parseMessage(request, sender) {
	course=request.getInfo
	rtab=sender.tab.id
	
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
	chrome.tabs.create({ url: chrome.extension.getURL('db.html') });
});

// From: https://stackoverflow.com/a/45985333/5257653
function getBrowser() {
  if (typeof chrome !== "undefined") {
	if (typeof browser !== "undefined") {
	  return "Firefox";
	} else {
	  return "Chrome";
	}
  } else {
	return "Edge";
  }
}
