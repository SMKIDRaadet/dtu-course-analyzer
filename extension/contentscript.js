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

//console.log("Checking")
if(course.length==5){
	if(matchRuleShort(window.location.href, "http*://kurser.dtu.dk/*course/*")){
		chrome.extension.sendRequest({getInfo: course});
		//console.log("Passed regex")

	} else{
		//console.log("Failed regex")
	}
} else{
	//console.log("Wrong length")
	//console.log("Wrong length of endStr or not numeric")
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	/*if(request.ping) {
	sendResponse({pong: true}); return; 
	}*/
	if(request[course]){
		//console.log(request[course])

		//console.log(getHTML(request[course]))
	} else if(request[course]==false){
		console.log("DTU COURSE ANALYZER: Wrong or no information received from db")
	}
	presentData(request[course])

});

outputArr = [ ["Average grade", "avg", ""], ["Average grade percentile", "avgp", "%"], ["Percent passed", "passpercent", "%"], ["Course rating percentile", "qualityscore", "%"], ["Workload percentile", "workload", "%"], ["Lazyscore percentile 🍺", "lazyscore", "%"]]
function presentData(data){
	addElement('<hr>',1);
	addElement('<table><tbody id="DTU-Course-Analyzer"></tbody></table>',2);
	console.log(data)
	addRow("—DTU Course Analyzer—", "");

	if(data){
		for(i = 0; i < outputArr.length; i++){
			key=outputArr[i][1]
			val=data[key]
			if (key=="workscore"){
				val=100-val
			}
			val=Math.round(val * 10) / 10
			if (typeof val != 'undefined' && !isNaN(val)){
				console.log(val)
				addRow(outputArr[i][0], val + outputArr[i][2])
			}
		}
	} else {
		addRow("No data found for this course", "")
	}
	addRow("<a href='https://github.com/OskarNS/dtu-course-analyzer/blob/master/README.md' target='_blank'><label>What is this?</label</a>", "")
}

function addElement(html, index){
	$('.box.information').children(':eq(' + index + ')').after(html)
}

function addRow(td1, td2){
	$('#DTU-Course-Analyzer')[0].insertRow(-1).innerHTML = '<tr><td><b>' + td1 + '</b></td><td>' + td2 + '</td></tr>';
}