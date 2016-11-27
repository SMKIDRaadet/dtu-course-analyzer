//console.log($('.col-xs-8')[0].childNodes[0].innerHTML)
//avg, passpercent, lazy-score, course rating
function matchRuleShort(str, rule) {
  return new RegExp("^" + rule.split("*").join(".*") + "$").test(str);
}

function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

course = window.location.href.split("/course/")[1]

if(course[course.length -1] == "/"){
		course=course.slice(0,-1)
}

console.log(chrome.tabs)

chrome.tabs.executeScript(null, {file: "data.js"}, function(results){ alert("loaded"); });

if(course.length==5 && isNumeric(course)){
	if(matchRuleShort(window.location.href, "http*://kurser.dtu.dk/course/*")){
		coursedata=data[course]
		outputArr = [ ["Average grade", "avg", ""], ["Percent passed", "passpercent", "%"], ["Course rating percentile", "qualityscore", "%"], ["Lazy score", "lazyscore", ""], ["Workload percentile", "workscore", "%"]]
		output=""
		for(i = 0; i < outputArr.length; i++){
			output += outputArr[i][0] + ": " + coursedata[outputArr[i][1]] + outputArr[i][2] + ". "
		}

		$('.col-xs-8').prepend( "<h5>" + output + "</h5>")
	} else{
		console.log("Failed regex")
	}
} else{
	console.log("Wrong length of endStr or not isNumeric")
}
console.log("course=" + course)

