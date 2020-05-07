<template>
    <div>
        <svg class="barchart" :id="id"></svg>
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
        data: {},
    },
    data() {
        return {
            height: 600,
            svgHeight: 0,
            svgWidth: 0,
            width: 600,
            margin: { top: 30, right: 30, bottom: 30, left: 70 },
            margin_top: 20,
            margin_left: 70,
            keys: [],
            values: [],
            x0: Object,
            y: Object,
            color: Object,
            svg: Object,
            container: Object,
            xAxis: Object,
            yAxis: Object,
            bars: Object,
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

            this.x0 = d3
                .scaleBand()
                .range([0, this.widthSVG])
                .padding(0.1);
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

            this.bars = this.container
                .selectAll(".bar")
                .data(this.values)
                .enter()
                .append("g")
                .attr("class", "bar");

            let x0 = this.x0;
            let y = this.y;
            let keys = this.keys;
            let svgHeight = this.svgHeight;
            let color = this.color;

            this.bars
                .append("rect")
                .attr("x", function(d, i) {
                    return x0(keys[i]);
                })
                .attr("y", function(d) {
                    return y(d);
                })
                .attr("width", x0.bandwidth())
                .attr("height", function(d) {
                    return svgHeight - y(d);
                })
                .attr("fill", function(d, i) {
                    return color(i);
                });
            /*
            //Die Labels über den Balken erstellen
            this.bars.append("text").text(function(d){ return d3.format(",")(d)})
                .attr("x", function(d,i) { return x0(keys[i])+x0.bandwidth()/2; })
                .attr("y", function(d) { return y(d)-5; })
                .attr("text-anchor", "middle");
*/
        },
        update() {}
    }
};
</script>

<style scoped></style>
