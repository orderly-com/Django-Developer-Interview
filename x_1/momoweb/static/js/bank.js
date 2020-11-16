const mySelection = document.getElementById("selectDate");

d3.json('/api/bank-date-filter/').then(function (data) {
  data = data.map(d => d.split('-', 2).join('-'));
  d3.select(mySelection)
    .append("span")
    .append("select")
    .attr("id", "bank-discount-date-selection")
    .attr("name", "tasks")
    .selectAll("option")
    .data(data)
    .enter()
    .append("option")
    .attr("value", d => d)
    .text(d => d);

  document.addEventListener("DOMContentLoaded", bankChart());

  d3.select("#bank-discount-date-selection").on("change", function () {
    console.log(1);
    const selectedOption = d3.select(this).node().value;
    const year = selectedOption.split('-')[0];
    const month = selectedOption.split('-')[1];
    bankChart(year, month);
  });
})


function bankChart(year = null, month = null) {
  const chartDIV = document.createElement("div");
  const table = d3.select(chartDIV).append("table");

  let api = '/api/bank-discount/'
  if (year && month) {
    api = `/api/bank-discount/?year=${year}&month=${month}`
  }

  d3.json(api).then(function (data) {
    table.append("thead")
      .join("tr")
      .selectAll("th")
      .data(Object.keys(data[0]))
      .join("th")
      .text(d => d)
      .style("background-color", "#aaa")
      .style("color", "#fff") ;

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
  })
}
