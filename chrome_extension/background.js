chrome.extension.onRequest.addListener(function(request, sender) {
	course=request.getInfo
	rtab=sender.tab.id
	
	var resp={};
	if(course in data){
		console.log(data[course]);
		resp[course]=data[course];
	} else{
		console.log("No data for this course");
		resp[course]=false;
	}
	
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		chrome.tabs.sendMessage(rtab, resp);
	});
});

	
chrome.browserAction.onClicked.addListener(function(tab) {
	chrome.tabs.create({ url: chrome.extension.getURL('db.html') });
});
