// contentscript.js - Chrome Version 2.0.5

// 1. Configuration (Must be defined BEFORE running logic)
const outputArr = [
  ["Average grade", "avg", "", 12],
  ["Average grade percentile", "avgp", "%", 100],
  ["Percent passed", "passpercent", "%", 100],
  ["Course rating percentile", "qualityscore", "%", 100],
  ["Workscore percentile", "workload", "%", 100],
  ["Lazyscore percentile 🍺", "lazyscore", "%", 100],
];

// 2. Extract course ID from URL
const courseMatch = window.location.href.match(
  /^http.:\/\/kurser.dtu.dk\/course\/(?:[0-9-]*\/)?([0-9]{5})/
);
const courseId = courseMatch ? courseMatch[1] : null;

// 3. UI Generation Functions
function presentData(data) {
  // Vanilla JS selector: Find the table inside .box.information
  const infoBoxTable = document.querySelector(".box.information > table");
  
  // Guard clause if the page structure changes or element isn't found
  if (!infoBoxTable) return;

  // Create the container table
  const table = document.createElement("table");
  const tbody = document.createElement("tbody");
  tbody.id = "DTU-Course-Analyzer";
  table.appendChild(tbody);

  // Insert our table immediately after the existing info table
  infoBoxTable.insertAdjacentElement("afterend", table);

  // Add Header Row
  const headerText = document.createElement("span");
  headerText.textContent = "—DTU Course Analyzer—";
  addRow(tbody, headerText);

  if (data) {
    outputArr.forEach(([label, key, unit, maxVal]) => {
      let val = data[key];

      if (typeof val !== "undefined" && !isNaN(val)) {
        val = Math.round(val * 10) / 10;
        
        // Create label span
        const labelSpan = document.createElement("span");
        labelSpan.textContent = label;

        addRow(tbody, labelSpan, val, unit, true, maxVal);
      }
    });
  } else {
    addRow(tbody, "No data found for this course");
  }

  // Add Footer Link
  const link = document.createElement("a");
  link.href = "https://github.com/SMKIDRaadet/dtu-course-analyzer";
  link.target = "_blank";
  
  const linkLabel = document.createElement("label");
  linkLabel.textContent = "What is this?";
  linkLabel.style.cursor = "pointer"; // Make it look clickable
  
  link.appendChild(linkLabel);
  addRow(tbody, link);
}

function addRow(tbody, contentLeft, value = "", unit = "", colored = false, maxVal = 1) {
  const tr = document.createElement("tr");

  // Left Column (Label)
  const tdLeft = document.createElement("td");
  const b = document.createElement("b");
  if (typeof contentLeft === "string") {
    b.textContent = contentLeft;
  } else {
    b.appendChild(contentLeft);
  }
  tdLeft.appendChild(b);
  tr.appendChild(tdLeft);

  // Right Column (Value)
  const tdRight = document.createElement("td");
  const span = document.createElement("span");
  span.textContent = value + unit;

  if (colored) {
    span.style.backgroundColor = getColor(value / maxVal);
    // Add some padding/radius to make it look like the original chips
    span.style.padding = "2px 6px";
    span.style.borderRadius = "4px";
  }

  tdRight.appendChild(span);
  tr.appendChild(tdRight);

  tbody.appendChild(tr);
}

function getColor(value) {
  // Clamp value between 0 and 1
  const clamped = Math.max(0, Math.min(1, value));
  // Calculate Hue (Green=120 to Red=0)
  const hue = (clamped * 120).toString(10);
  return `hsl(${hue}, 100%, 50%)`;
}

// 4. Main Execution Logic (Must be at the BOTTOM)
if (courseId && courseId.length === 5) {
  // DIRECT INJECTION STRATEGY:
  // Manifest loads db/data.js BEFORE this script.
  // We read 'window.data' directly.
  const db = window.data; 

  if (db && db[courseId]) {
    presentData(db[courseId]);
  } else {
    console.error("DTU Analyzer: Course data not found. Ensure db/data.js starts with 'window.data = ...'");
    presentData(null);
  }
}