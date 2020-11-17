const width = 1000;
const height = 500;
d3.json("/api/duplicate-limit-time-sale/").then(function (data) {
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
    const margin = ({top: 20, right: 40, bottom: 100, left: 40});

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
      .attr("width", x.bandwidth())
      .attr("data", (d) => d.name)
      .attr("data-toggle", "tooltip")
      .attr("data-placement", "bottom")
      .attr("title", d => d.name)
      .on("mouseover", function () {
        d3.select(this).style("fill", "lightsteelblue");
        $(function () {
          $("[data-toggle='tooltip']").tooltip();
        });
      })
      .on("mouseout", function () {
        d3.select(this).style("fill", "steelblue");
      });


    const gx = svg.append("g")
      .call(xAxis);

    const gy = svg.append("g")
      .call(yAxis)
      .attr("font-size", 18);

    const t = svg.transition()
      .duration(750);

    bar.data(data, d => d.name)
      .order()
      .transition(t)
      .delay((d, i) => i * 20)
      .attr("x", d => x(d.name));

    gx.transition(t)
      .call(xAxis)
      .selectAll("text")
      .attr("x", 10)
      .attr("font-size", 18)
      .attr("text-anchor", "start")
      .text(function (d) {
        return d.slice(0, 5) + "...";
      })
      .attr("transform", "rotate(45)")
      .delay((d, i) => i * 20);


    const showChart = document.getElementById("duplicate-chart");
    while (showChart.firstChild) {
      showChart.firstChild.remove();
    }
    showChart.appendChild(chartDIV);
  }
});
