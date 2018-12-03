browser.runtime.onMessage.addListener(function(request, sender) {
	course=request.getInfo
	rtab=sender.tab.id
	
	var resp={};
	if(course in data){
		resp[course]=data[course]
	} else{
		resp[course]=false
	}
	
	browser.tabs.query({active: true, currentWindow: true}, function(tabs) {
		browser.tabs.sendMessage(rtab, resp);
	});
});
	
browser.browserAction.onClicked.addListener(function(tab) {
	browser.tabs.create({ url: browser.extension.getURL('db.html') });
});