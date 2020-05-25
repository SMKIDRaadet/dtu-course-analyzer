console.log('running!')

function matchRuleShort(str, rule) {
 	return new RegExp("^" + rule.split("*").join(".*") + "$").test(str);
}

function isNumeric(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}

course = window.location.href.split("/course/")[1]
if( !(isNumeric(course[course.length -1])) ){
		course=course.slice(0,-1);
}

if(course.length==5){
	console.log(1);
	if(matchRuleShort(window.location.href, "http*://kurser.dtu.dk/*course/*")){
		browser.runtime.sendMessage({getInfo: course});
	}
}

browser.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if(request[course]){
		presentData(request[course]);
	}
});

const defaultColorRange = {minHue: 0, maxHue: 120, startRangeAt: 0};

outputArr = [
	["Average grade", "avg", "", 12, {minHue: 0, maxHue: 120, startRangeAt: 0.2}],
	["Average grade percentile", "avgp", "%", 100, defaultColorRange],
	["Percent passed", "passpercent", "%", 100, {minHue: 0, maxHue: 120, startRangeAt: 0.5}],
	["Course rating percentile", "qualityscore", "%", 100, defaultColorRange],
	["Workscore percentile", "workload", "%", 100, defaultColorRange],
	["Lazyscore percentile 🍺", "lazyscore", "%", 100, defaultColorRange]]

function presentData(data){
	$('.box.information > table').first().after($('<table/>').append($('<tbody/>', {'id': 'DTU-Course-Analyzer'})));
	addRow($('<span/>').text('—DTU Course Analyzer—'));

	if(data){
		for(i = 0; i < outputArr.length; i++){
			key=outputArr[i][1];
			val=data[key];

			val=Math.round(val * 10) / 10;
			if (typeof val != 'undefined' && !isNaN(val)){
				addRow($('<span/>', {'text': outputArr[i][0]}), val, outputArr[i][2], true, outputArr[i][3], outputArr[i][4]);
			}
		}
	} else {
		addRow("No data found for this course");
	}
	addRow($('<a/>', {'href': 'https://github.com/OskarNS/dtu-course-analyzer/blob/master/README.md', 'target': '_blank'}).append($('<label/>', {'text': 'What is this?'})));
}

var tdIndex = 0;

function addRow(td1Elem, td2val="", unitText="", colored = false, maxValue = 1, colorRange = defaultColorRange){
	id = 'dca-td-' + tdIndex;

	$('#DTU-Course-Analyzer').append(
		$('<tr/>').append(
			$('<td/>').append(
				$('<b/>').append(td1Elem)
				)
			)
		.append($('<td/>').append(
			$('<span/>', {'id': id, 'text': td2val + unitText})
			)
		)
	);

	if(colored){
		elem = document.getElementById(id);
		elem.style.backgroundColor = colorRangeToString(td2val/maxValue, colorRange);
	}
	tdIndex++;
}

/**
 * Returns the hsl color string for the value using the specified color range.
 */
function colorRangeToString(value, colorRange) {
	const range = colorRange.maxHue - colorRange.minHue;

	// The processed value is the value after it is adjusted so that is offset by colorRange.startRangeAt
	let processedValue = clamp(value, 0, 1);

	if(colorRange.startRangeAt !== 0) {
		processedValue = (value - colorRange.startRangeAt) / colorRange.startRangeAt;
	}

	// The processed value is then scaled by the range, and added to the minimum hue to achieve the final hue value
	const hueOffset = processedValue * range;
	const hue = clamp(hueOffset + colorRange.minHue, colorRange.minHue, colorRange.maxHue);

	return `hsl(${hue}, 100%, 50%)`;
}

function clamp(value, min, max) {
	return Math.max(min, Math.min(value, max));
}
