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

if(course.length==5){
	console.log(1);
	if(matchRuleShort(window.location.href, "http*://kurser.dtu.dk/*course/*")){
		browser.runtime.sendMessage({getInfo: course});
	}
}

browser.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if(request[course]){
		presentData(request[course])
	}
});

outputArr = [ ["Average grade", "avg", "", 12], ["Average grade percentile", "avgp", "%", 100], ["Percent passed", "passpercent", "%", 100], ["Course rating percentile", "qualityscore", "%", 100], ["Workscore percentile", "workload", "%", 100], ["Lazyscore percentile 🍺", "lazyscore", "%", 100]]
function presentData(data){
	addElement('<hr>',1);
	addElement('<table><tbody id="DTU-Course-Analyzer"></tbody></table>',2);
	addRow("—DTU Course Analyzer—");

	if(data){
		for(i = 0; i < outputArr.length; i++){
			key=outputArr[i][1]
			val=data[key]

			val=Math.round(val * 10) / 10
			if (typeof val != 'undefined' && !isNaN(val)){
				addRow(outputArr[i][0], val, outputArr[i][2], true, outputArr[i][3])
			}
		}
	} else {
		addRow("No data found for this course")
	}
	addRow("<a href='https://github.com/OskarNS/dtu-course-analyzer/blob/master/README.md' target='_blank'><label>What is this?</label</a>")
}

function addElement(html, index){
	$('.box.information').children(':eq(' + index + ')').after(html)
}

var tdIndex = 0;
function addRow(td1, td2="", unit="", colored = false, maxValue = 1){
	id = 'dca-td-' + tdIndex
	$('#DTU-Course-Analyzer')[0].insertRow(-1).innerHTML = '<tr><td><b>' + td1 + '</b></td><td><span id=' + id + '>' + td2 + unit + '</span></td></tr>';
	if(colored){
		elem=document.getElementById(id)
		elem.style.backgroundColor=getColor(1 - td2/maxValue);
	}
	tdIndex++;
}

function getColor(value){
    //value from 0 to 1
    if(value>1){
    	value=1;
    }
    var hue=((1-value)*120).toString(10);
    return ["hsl(",hue,",100%,50%)"].join("");
}
