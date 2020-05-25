<template>
    <div>
        <svg class="linechart" :id="id"></svg>
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
        data: Object,
        pieData: Object,
        radius: Number,
        id: Number
    },

    data() {
        return {
            testdata: {
                PBS: 500,
                PHS: 300,
                PLA: 350
            },
            height: 600,
            heightSVG: 0,
            widthSVG: 0,
            width: 600,
            margin: { top: 30, right: 30, bottom: 30, left: 70 },
            margin_top: 20,
            margin_left: 50,
            keys: Array,
            values: Array,
            color: Object,
            arc: Object,
            pie: Object,
            arcs: Object,
        };
    },
    watch: {
        pieData: function() {
                this.init();
                this.draw();
        }
    },
    computed: {},
    mounted() {
        this.init();
        this.draw();
    },
    methods: {
        init() {
            this.svg = d3.select(document.getElementById(this.id));
            this.svg
                .attr("preserveAspectRatio", "xMinYMin meet")
                .attr("viewBox", "0 0 " + this.width + " " + this.height);

            this.widthSVG = this.width - this.margin.left - this.margin.right;
            this.heightSVG = this.height - this.margin.top - this.margin.bottom;
            if (this.pieData === undefined) {
                this.keys = Object.keys(this.testdata);
                this.values = Object.values(this.testdata);
            }else {
                this.keys = Object.keys(this.pieData);
                this.values = Object.values(this.pieData);
            }

            // this.radius = Math.min(this.width, this.height) / 2 - 20;

            this.color = d3.scaleOrdinal(d3.schemeCategory10);

            this.arc = d3
                .arc()
                .outerRadius(this.radius)
                .innerRadius(0);
        },
        draw() {
            //clean the svg slate (https://stackoverflow.com/questions/14422198/how-do-i-remove-all-children-elements-from-a-node-and-then-apply-them-again-with/43661877#43661877)
            this.svg.selectAll("*").remove();
            let diagram = this; //done for function expressions
            this.container = this.svg
                .append("g")
                .attr("class", "svgcontainer")
                .attr("id", "c")
                .attr(
                    "transform",
                    "translate(" + this.width / 2 + "," + this.height / 2 + ")"
                );

            this.pie = d3
                .pie()
                .sort(null)
                .value(function(d) {
                    return d;
                });

            let color = this.color;
            let radius = this.radius;
            let keys = this.keys;

            this.arcs = this.container
                .selectAll(".arc")
                .data(this.pie(this.values));

            this.arcs
                .transition()
                .duration(1500)
                .attrTween("d", arcTween);

            var size = this.keys.length;

            let tooltip = diagram.svg
                .append("g")
                .attr("class", "tooltip")
                .attr("opacity", 0);

            tooltip
                .append("rect")
                .attr("width", 40)
                .attr("height", 20)
                .attr("rx",7)
                .attr("ry",7)
                .attr("fill", "#FFF")
                .style("stroke-width", 1)
                .style("stroke", "#000");
            let tooltext = tooltip.append("text").attr("class", "tooltext");

            var arcOver = d3.arc()
                .outerRadius(radius+10)
                .innerRadius(0);

            this.arcs
                .enter()
                .append("path")
                .attr("class", "arc")
                .attr("fill", function(d, i) {
                    return color(keys[i]);
                })
                .attr("d", this.arc)
                .on("mouseover", function(d, i) {
                    d3.select(this)
                        .attr("d", arcOver);
                })
                .on("mouseout", function(d, i) {
                    tooltip.attr("opacity", 0);
                    d3.select(this)
                        .attr("d", diagram.arc);
                })
                .on("click", function(d, i) {
                    let point = d3.mouse(this);
                    let x = point[0] + 300; // i dont know why but the d3 mouse xy position is WAY of
                    let y = point[1] + 280;
                    let text = diagram.keys[i] + ": " + d.value;
                    let width = 6 * text.length + 1;

                    // prevent drawing out of the svg box
                    // if (x > diagram.widthSVG / 2) {
                    //     x -= width;
                    // }
                    // if (y < diagram.heightSVG / 2) {
                    //     y += 20;
                    //     if (x < diagram.widthSVG / 2) {
                    //         x += 10; //move the tooltip out from under the mouse courser
                    //     }
                    // }

                    tooltip
                        .selectAll('rect')
                        .attr("width", width);

                    tooltip
                        .attr("transform", "translate(" + x + ", " + y + ")")
                        .attr("opacity", 1);
                    tooltext
                        .attr("x", 6)
                        .attr("y", 14)
                        .text(diagram.keys[i] + ": " + d.value);
                })
                .each(function(d) {
                    this._current = d;
                });

            function arcTween(a) {
                let i = d3.interpolate(this._current, a);
                this._current = i(0);
                return function(t) {
                    return arc(i(t));
                };
            }
        },
        update() {

        }
    }
};
</script>

<style scoped></style>
