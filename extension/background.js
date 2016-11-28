chrome.extension.onRequest.addListener(function(request, sender) {
	course=request.getInfo
	rtab=sender.tab.id
	//console.log(rtab + ":'" + course + "'");
	
	var resp={};
	if(course in data){
		resp[course]=data[course]
	} else{
		//console.log("No data for this course")
		resp[course]=false
	}
	
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		chrome.tabs.sendMessage(rtab, resp);
	});
});

