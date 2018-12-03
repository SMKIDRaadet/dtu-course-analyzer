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

	
chrome.browserAction.onClicked.addListener(function(tab) {
	chrome.tabs.create({ url: chrome.extension.getURL('db.html') });
});
function getColor(value){
    //value from 0 to 1
    var hue=((1-value)*120).toString(10);
    return ["hsl(",hue,",100%,50%)"].join("");
}