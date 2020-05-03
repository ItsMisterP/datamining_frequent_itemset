<template>
    <div>
        <h1>Multi Line Chart</h1>
        <svg class="linechart" :id="id"></svg>
        Noch buggy, warte bis wir den richtigen Datensatz haben
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
        data: Object
    },
    data() {
        return {
            testdata: {
                PLA: {
                    A: 1,
                    B: 2
                },
                PBS: {
                    A: 1,
                    B: 4
                }
            },
            id: 9000,
            height: 600,
            heightSVG: 0,
            widthSVG: 0,
            width: 600,
            margin: { top: 30, right: 30, bottom: 30, left: 70 },
            margin_top: 20,
            margin_left: 50,
            keysX0: [],
            keysX1: [],
            values: [],
            maxX1: 0,
            x0: Object,
            x1: Object,
            y: Object,
            color: Object,
            svg: Object,
            container: Object,
            xAxis: Object,
            yAxis: Object,
            groups: Object,
            lines: Object,
            points: Object
        };
    },
    computed: {},
    mounted() {
        this.init();
        this.draw();
    },
    created() {
    },
    methods: {
        init() {
            this.svg = d3.select(document.getElementById(this.id));
            this.svg
                .attr("preserveAspectRatio", "xMinYMin meet")
                .attr("viewBox", "0 0 " + this.width + " " + this.height);

            this.widthSVG = this.width - this.margin.left - this.margin.right;
            this.heightSVG = this.height - this.margin.top - this.margin.bottom;

            this.keysX0 = Object.keys(this.testdata);
            this.values = Object.values(this.testdata);
            this.keysX1 = Object.keys(this.values[0]);

            this.color = d3.scaleOrdinal(d3.schemeCategory10);

            this.maxX1 = this.findMax(this.values, this.keysX1);

            this.x0 = d3
                .scaleBand()
                .range([0, this.widthSVG])
                .padding(0.1);
            this.x0.domain(this.keysX1);

            this.y = d3
                .scaleLinear()
                .domain([0, this.maxX1])
                .nice()
                .rangeRound([this.heightSVG, 0]);

            this.generator = d3
                .line()
                .x(function(d, i) {
                    return x0(this.keysX0[i]) + x0.bandwidth() / 2;
                })
                .y(function(d) {
                    return y(d);
                });
        },
        draw() {
            this.container = this.svg
                .append("g")
                .attr("class", "svgcontainer")
                .attr("id", "containerid")
                .attr(
                    "transform",
                    "translate(" +
                        this.margin.left +
                        "," +
                        this.margin.top +
                        ")"
                );

            this.xAxis = this.container
                .append("g")
                .attr("class", "axis")
                .attr("id", "xAxis")
                .attr("transform", "translate(0," + this.heightSVG + ")")
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
            let x1 = this.x1;
            let values = this.values;
            let y = this.y;
            let keysX0 = this.keysX0;
            let keysX1 = this.keysX1;
            let heightSVG = this.heightSVG;
            let widthSVG = this.widthSVG;
            let margin = this.margin;
            let color = this.color;

            let generator = d3
                .line()
                .x(function(d, i) {
                    return x0(keysX1[i]) + x0.bandwidth() / 2;
                })
                .y(function(d) {
                    return y(d);
                });

            this.groups = this.container
                .selectAll(".line-group")
                .data(keysX1)
                .enter()
                .append("g")
                .attr("fill", function(d, i) {
                    return color(i);
                })
                .attr("class", function(d) {
                    return "line-group " + d;
                });

            this.lines = this.groups
                .append("path")
                .attr("stroke", function(d, i) {
                    return color(i);
                })
                .datum(function(d) {
                    let dat = [];
                    for (let k = 0; k < keysX0.length; k++) {
                        dat.push(values[k][d]);
                    }
                    return dat;
                })
                .attr("class", "line Global")
                .attr("d", generator)
                .attr("fill", "none");

            this.points = this.groups
                .selectAll(".dot")
                .data(function(d) {
                    let dat = [];
                    for (let k = 0; k < keysX1.length; k++) {
                        dat.push(values[k][d]);
                    }
                    return dat;
                })
                .enter()
                .append("circle") // Uses the enter().append() method
                .attr("class", "dot") // Assign a class for styling
                .attr("cx", function(d, i) {
                    return x0(keysX1[i]) + x0.bandwidth() / 2;
                })
                .attr("cy", function(d) {
                    return y(d);
                })
                .attr("r", 3);
        },
        update() {},
        createX1Keys(values) {
            let arr = [];

            for (let i in value) {
                for (let j in value[i]) {
                    if (!arr.includes(j)) {
                        arr.push(j);
                    }
                }
            }
            return arr;
        },
        findMax(values, keysX1) {
            let max = 0;

            for (let i = 0; i < values.length; i++) {
                for (let j = 0; j < keysX1.length; j++) {
                    let tmp = values[i];

                    if (parseFloat(tmp[keysX1[j]]) > parseFloat(max))
                        max = tmp[keysX1[j]];
                }
            }

            return max;
        }
    }
};
</script>

<style scoped></style>
