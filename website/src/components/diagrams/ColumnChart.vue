<template>
    <div>
        <h1>Säulendiagramm</h1>
        <svg :id="id" ></svg>
    </div>
</template>

<script>
import * as d3 from 'd3'
import { scaleLinear, scaleBand } from "d3-scale";
import { max, min } from "d3-array";
import { selectAll } from "d3-selection";

export default {
    name: "Column Chart",
    props:{
        data: Array
    },
    data(){
        return{
            testdata: {
                "AM" : 500000,
                "PM" :400000,
            },
            id: 6000,
            height: 600,
            heightSVG: 0,
            widthSVG: 0,
            width: 600,
            margin: {top: 20, right: 30, bottom: 30, left: 70},
            margin_top : 10,
            margin_left: 30,
            keys : [],
            values: [],
            x0: Object,
            y: Object,
            color: Object,
            svg: Object,
            container: Object,
            xAxis: Object,
            yAxis: Object,
            bars: Object
        }
    },
    mounted(){
        this.init();
        this.draw();
    },
    methods:{
        init(){
            this.svg = d3.select(document.getElementById(this.id));
            this.svg.attr("preserveAspectRatio", "xMinYMin meet")
                    .attr("viewBox", "0 0 " + this.width + " " + this.height);

            this.widthSVG = this.width - this.margin.left - this.margin.right;
            this.heightSVG = this.height - this.margin.top - this.margin.bottom;

            this.keys = Object.keys(this.testdata);
            this.values = Object.values(this.testdata);

            this.x0 = d3.scaleLinear().range([0, this.widthSVG]);
            this.x0.domain([0, d3.max(this.values)]);

            this.y = d3.scaleBand().range([this.heightSVG, 0]);
            this.y.domain(this.keys).padding(0.1);

            this.color = d3.scaleOrdinal(d3.schemeCategory10);
        },
        draw(){
            this.container = this.svg.append("g")
                                    .attr("class", "svgcontainer")
                                    .attr("id", "c")
                                    .attr("transform", "translate(" + this.margin_left + "," + this.margin_top + ")");

            this.xAxis = this.container.append("g")
                            .attr("class", "axis")
                            .attr("id", "xAxis")
                            .attr("transform", "translate(0," + this.heightSVG + ")")
                            .call(d3.axisBottom(this.x0));

            this.yAxis = this.container.append("g")
                                        .attr("class", "y axis")
                                        .call(d3.axisLeft(this.y));

            let color = this.color;
            let keys = this.keys;
            let y = this.y;
            let x = this.x0;

            this.bars = this.container.selectAll(".bar")
                                        .data(this.values)
                                        .enter().append("rect")
                                        .attr("class", "bar")
                                        .attr("x", 0)
                                        .attr("height", this.y.bandwidth())
                                        .attr("fill", function (d,i) {
                                            return color(i);
                                        })
                                        .attr("y", function(d,i) { return y(keys[i]); })
                                        .attr("width", function(d) { 
                                            return x(d);
                                        });
        },
        update(){

        }
    }
}
</script>

<style scoped>

</style>