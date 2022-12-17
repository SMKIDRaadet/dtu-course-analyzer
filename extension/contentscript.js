course = window.location.href.match(
  /^http.:\/\/kurser.dtu.dk\/course\/(?:[0-9-]*\/)?([0-9]{5})/
)[1];

if (course.length == 5) {
  console.log("Course ID:", course);
  if(getBrowser() == "Chrome") {
	chrome.extension.sendRequest({ getInfo: course });
  } else {
	browser.runtime.sendMessage({ getInfo: course });
  }
}

if(getBrowser() == "Chrome") {
  chrome.runtime.onMessage.addListener(listen);
} else {
  browser.runtime.onMessage.addListener(listen);
}
									  
function listen(request, sender, sendResponse) {
  if (request[course]) {
    presentData(request[course]);
  }
}

outputArr = [
  ["Average grade", "avg", "", 12],
  ["Average grade percentile", "avgp", "%", 100],
  ["Percent passed", "passpercent", "%", 100],
  ["Course rating percentile", "qualityscore", "%", 100],
  ["Workscore percentile", "workload", "%", 100],
  ["Lazyscore percentile 🍺", "lazyscore", "%", 100],
];
function presentData(data) {
  $(".box.information > table")
    .first()
    .after($("<table/>").append($("<tbody/>", { id: "DTU-Course-Analyzer" })));
  addRow($("<span/>").text("—DTU Course Analyzer—"));

  if (data) {
    for (i = 0; i < outputArr.length; i++) {
      key = outputArr[i][1];
      val = data[key];

      val = Math.round(val * 10) / 10;
      if (typeof val != "undefined" && !isNaN(val)) {
        addRow(
          $("<span/>", { text: outputArr[i][0] }),
          val,
          outputArr[i][2],
          true,
          outputArr[i][3]
        );
      }
    }
  } else {
    addRow("No data found for this course");
  }
  addRow(
    $("<a/>", {
      href:
        "https://github.com/OskarNS/dtu-course-analyzer/blob/master/README.md",
      target: "_blank",
    }).append($("<label/>", { text: "What is this?" }))
  );
}

var tdIndex = 0;

function addRow(
  td1Elem,
  td2val = "",
  unitText = "",
  colored = false,
  maxValue = 1
) {
  id = "dca-td-" + tdIndex;

  $("#DTU-Course-Analyzer").append(
    $("<tr/>")
      .append($("<td/>").append($("<b/>").append(td1Elem)))
      .append(
        $("<td/>").append($("<span/>", { id: id, text: td2val + unitText }))
      )
  );

  if (colored) {
    elem = document.getElementById(id);
    elem.style.backgroundColor = getColor(1 - td2val / maxValue);
  }
  tdIndex++;
}

function getColor(value) {
  //value from 0 to 1
  if (value > 1) {
    value = 1;
  }
  var hue = ((1 - value) * 120).toString(10);
  return ["hsl(", hue, ",100%,50%)"].join("");
}

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
