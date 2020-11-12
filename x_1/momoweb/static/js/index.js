let data = [{
  "name": "name1",
  "count": 20,
},
  {
    "name": "name2",
    "count": 12,
  },
  {
    "name": "name3",
    "count": 19,
  },
  {
    "name": "name4",
    "count": 5,
  },
  {
    "name": "name5",
    "count": 16,
  },
  {
    "name": "name6",
    "count": 26,
  },
  {
    "name": "name7",
    "count": 30,
  }];

const width = 1000;
const height = 500;
const mySelection = document.getElementById("selectMe");
const selectItems = ["Alphabetically", "Ascending", "Descending"];

// Create a drop down
d3.select(mySelection)
  .append("span")
  .append("select")
  .attr("id", "selection")
  .attr("name", "tasks")
  .selectAll("option")
  .data(selectItems)
  .enter()
  .append("option")
  .attr("value", d => d)
  .text(d => d);

document.addEventListener("DOMContentLoaded", myChart());


// change chart by sort
d3.select("#selection").on("change", function () {
  const selectedOption = d3.select(this).node().value;
  if (selectedOption === "Ascending") {
    data.sort((a, b) => {
      return d3.ascending(a.count, b.count)
    })
  } else if (selectedOption === "Descending") {
    data.sort((a, b) => {
      return d3.descending(a.count, b.count)
    })
  } else if (selectedOption === "Alphabetically") {
    data.sort((a, b) => {
      return d3.ascending(a.name, b.name)
    })
  }
  myChart();
})

function myChart() {
  const chartDIV = document.createElement("div");
  const margin = ({top: 20, right: 0, bottom: 30, left: 40});

  const x = d3.scaleBand()
    .domain(data.map(d => d.name))
    .range([margin.left, width - margin.right])
    .padding(0.1);

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.count)]).nice()
    .range([height - margin.bottom, margin.top])

  const xAxis = g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickSizeOuter(0));

  const yAxis = g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y))
    .call(g => g.select(".domain").remove());

  const svg = d3.select(chartDIV)
    .append("svg")
    .attr("viewBox", [0, 0, width, height]);

  const bar = svg.append("g")
    .attr("fill", "steelblue")
    .selectAll("rect")
    .data(data)
    .join("rect")
    .style("mix-blend-mode", "multiply")
    .attr("x", d => x(d.name))
    .attr("y", d => y(d.count))
    .attr("height", d => y(0) - y(d.count))
    .attr("width", x.bandwidth());

  const gx = svg.append("g")
    .call(xAxis);

  const gy = svg.append("g")
    .call(yAxis);

  const t = svg.transition()
    .duration(750);

  bar.data(data, d => d.name)
    .order()
    .transition(t)
    .delay((d, i) => i * 20)
    .attr("x", d => x(d.name));

  gx.transition(t)
    .call(xAxis)
    .selectAll(".tick")
    .delay((d, i) => i * 20);

  const showChart = document.getElementById("duplicate-chart");
  while (showChart.firstChild) {
    showChart.firstChild.remove();
  }
  showChart.appendChild(chartDIV);
}
