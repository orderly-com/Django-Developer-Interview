const dataSet1 = [
  {
    "bank_name": "bankA",
    "discount_date": "10/1-10/5",
    "condition": "滿100",
    "discount": "送3萬"
  },
  {
    "bank_name": "bankB",
    "discount_date": "10/1-10/5",
    "condition": "滿100",
    "discount": "送3萬"
  }
];

const dataSet2 = [
  {
    "bank_name": "bankA",
    "discount_date": "11/1-11/5",
    "condition": "滿100",
    "discount": "送3萬"
  },
  {
    "bank_name": "bankB",
    "discount_date": "11/1-11/5",
    "condition": "滿100",
    "discount": "送3萬"
  }
];

const mySelection = document.getElementById("selectDate");
const selectItems = ["dataSet1", "dataSet2"];
let data = dataSet1;

d3.select(mySelection)
  .append("span")
  .append("select")
  .attr("id", "bank-discount-date-selection")
  .attr("name", "tasks")
  .selectAll("option")
  .data(selectItems)
  .enter()
  .append("option")
  .attr("value", d => d)
  .text(d => d);

document.addEventListener("DOMContentLoaded", bankChart());

d3.select("#bank-discount-date-selection").on("change", function () {
  const selectedOption = d3.select(this).node().value;
  if (selectedOption === "dataSet1") {
    data = dataSet1
  } else if (selectedOption === "dataSet2") {
    data = dataSet2
  }
  bankChart()
});

function bankChart() {
  const chartDIV = document.createElement("div");
  const margin = ({top: 20, right: 40, bottom: 100, left: 40});
  const table = d3.select(chartDIV).append("table");

  table.append("thead")
    .join("tr")
    .selectAll("th")
    .data(Object.keys(data[0]))
    .join("th")
    .text(d => d)
    .style("background-color", "#aaa")
    .style("color", "#fff");

  table.append("tbody")
    .selectAll("tr")
    .data(data)
    .join("tr")
    .selectAll("td")
    .data(row => Object.entries(row))
    .join("td")
    .text(d => d[1]);
  const showChart = document.getElementById("bank-chart");
  while (showChart.firstChild) {
    showChart.firstChild.remove();
  }
  showChart.appendChild(chartDIV);
}

