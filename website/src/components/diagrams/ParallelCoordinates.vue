<template>
    <div>
        <svg class="parallelcoordinates" :id="id"></svg>
    </div>
</template>

<script>
    import * as d3 from "d3";
    import { scaleLinear, scaleBand } from "d3-scale";
    import { max, min } from "d3-array";
    import { selectAll } from "d3-selection";

    export default {
        name: "Test-Chart",
        props: {
            dataString: String,
            id: String,
            data: Object
        },
        data() {
            return {
                testdata: {
                    AM1: 500000,
                    PM: 400000,
                    AM2: 43333,
                    PM2: 433333
                },
                height: 600,
                svgHeight: 0,
                svgWidth: 0,
                width: 600,
                margin: { top: 30, right: 30, bottom: 30, left: 70 },
                margin_top: 20,
                margin_left: 50,
                keys: [],
                values: [],
                x0: Object,
                y: Object,
                color: Object,
                svg: Object,
                container: Object,
                xAxis: Object,
                yAxis: Object,
                line: Object
            };
        },
        watch:{
            data: function(){
                if(this.data != undefined){
                    this.init();
                    this.draw();
                }
            }
        },
        mounted() {
            if(this.data != undefined){
                this.init();
                this.draw();
            }
        },
        created() {},
        methods: {
            fetchData() {
                let diagram = this;
                d3.json(this.dataString).then(function(data) {
                    diagram.data = data;
                    diagram.init();
                    diagram.draw();
                });
            },
            init() {
                this.testdata = this.data;

                this.svg = d3.select(document.getElementById(this.id));

                this.widthSVG = this.width - this.margin.left - this.margin.right;
                this.svgHeight = this.height - this.margin.top - this.margin.bottom;

                this.keys = Object.keys(this.testdata);
                this.values = Object.values(this.testdata);

                this.x0 = d3.scaleBand().range([0, this.widthSVG]);
                this.x0.domain(this.keys);

                this.y = d3
                    .scaleLinear()
                    .domain([0, d3.max(this.values)])
                    .nice()
                    .rangeRound([this.svgHeight, 0]);

                this.color = d3.scaleOrdinal(d3.schemeCategory10);
            },
            draw() {
                this.svg.attr("viewBox", "0 0 " + this.width + " " + this.height);

                this.container = this.svg
                    .append("g")
                    .attr("class", "svgcontainer")
                    .attr("id", "c")
                    .attr(
                        "transform",
                        "translate(" +
                        this.margin_left +
                        "," +
                        this.margin_top +
                        ")"
                    );

                this.xAxis = this.container
                    .append("g")
                    .attr("class", "axis")
                    .attr("id", "xAxis")
                    .attr("transform", "translate(0," + this.svgHeight + ")")
                    .call(d3.axisBottom(this.x0));

                this.yAxis = this.container
                    .append("g")
                    .attr("id", "yAxis")
                    .attr("class", "axis")
                    .call(d3.axisLeft(this.y))
                    .append("text")
                    .attr("x", 2)
                    .attr("y", this.y(this.y.ticks().pop()) + 0.5)
                    .attr("dy", "0.32em")
                    .attr("fill", "#000")
                    .attr("font-weight", "bold")
                    .attr("text-anchor", "start")
                    .text("k");

                let x0 = this.x0;
                let y = this.y;
                let keys = this.keys;
                let svgHeight = this.svgHeight;
                let color = this.color;
                let values = this.values;

                let line = d3
                    .line()
                    .x(function(d, i) {
                        return x0(keys[i]) + x0.bandwidth() / 2;
                    })
                    .y(function(d, i) {
                        return y(values[i]);
                    });

                this.container
                    .append("path")
                    .datum(keys)
                    .attr("stroke", function() {
                        return color(9);
                    })
                    .attr("class", "line Global")
                    .attr("d", line)
                    .attr("fill", "none");

                this.container
                    .selectAll(".dot")
                    .data(keys)
                    .enter()
                    .append("circle")
                    .attr("class", "dot Global")
                    .attr("cx", function(d) {
                        return x0(d) + x0.bandwidth() / 2;
                    })
                    .attr("cy", function(d, i) {
                        return y(values[i]);
                    })
                    .attr("r", 3);
            },
            update() {}
        }
    };
</script>

<style scoped></style>
