
var data = [
    { aa: 77, bb: 20, 'url': '1url' },
    { aa: 40, bb: 90, 'url': '2url' },
    { aa: 80, bb: 50, 'url': '3123' },
]
var margin = { top: 10, right: 40, bottom: 30, left: 30 },
    width = 450 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;
var x = d3.scaleLinear()
    .domain([0, 100])
    .range([0, width]);
var y = d3.scaleLinear()
    .domain([0, 100])
    .range([height, 0]);
var svg01 = d3.select("#scatter_area")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");
svg01
    .append('g')
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));
svg01
    .append('g')
    .call(d3.axisLeft(y));
svg01
    .selectAll("whatever")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", function (d) { return x(d.aa) })
    .attr("cy", function (d) { return y(d.bb) })
    .attr("r", 3)
svg01
    .selectAll("whatever")
    .data(data)
    .enter()
    .append("text")
    .attr('x', function (d) { return x(d.aa) })
    .attr('y', function (d) { return y(d.bb) })
    .append("a")
    .attr('href', function (d) { return (d.url) })
    .text(function (d) { return (d.url) })
