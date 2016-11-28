function matchRuleShort(str, rule) {
 	return new RegExp("^" + rule.split("*").join(".*") + "$").test(str);
}

function isNumeric(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}

course = window.location.href.split("/course/")[1]
if( !(isNumeric(course[course.length -1])) ){
		course=course.slice(0,-1)
}
//console.log("course=" + course)


if(course.length==5 && isNumeric(course)){
	if(matchRuleShort(window.location.href, "http*://kurser.dtu.dk/course/*")){
		chrome.extension.sendRequest({getInfo: course});

	} else{
		//console.log("Failed regex")
	}
} else{
	//console.log("Wrong length of endStr or not numeric")
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	/*if(request.ping) {
	sendResponse({pong: true}); return; 
	}*/
	if(request[course]){
		//console.log(request[course])

		//console.log(getHTML(request[course]))
		presentData(request[course])
	}
});

outputArr = [ ["Average grade", "avg", ""], ["Percent passed", "passpercent", "%"], ["Course rating percentile", "qualityscore", "%"], ["Workload percentile", "workscore", "%"], ["Lazy score", "lazyscore", ""]]
function presentData(data){
	addElement('<hr>',1);
	addElement('<table><tbody id="DTU-Course-Analyzer"></tbody></table>',2);
	
	addRow("—DTU Course Analyzer—", "");
	for(i = 0; i < outputArr.length; i++){
		addRow(outputArr[i][0], data[outputArr[i][1]] + outputArr[i][2])
	}
	addRow("<a href='#'><label>What is this?</label</a>", "")
}

function addElement(html, index){
	$('.box.information').children(':eq(' + index + ')').after(html)
}

function addRow(td1, td2){
	$('#DTU-Course-Analyzer')[0].insertRow(-1).innerHTML = '<tr><td><b>' + td1 + '</b></td><td>' + td2 + '</td></tr>';
}