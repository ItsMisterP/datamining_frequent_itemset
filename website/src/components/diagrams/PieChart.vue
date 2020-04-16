<template>
    <div>
        <h1>Grouped Bar Chart</h1>
        <svg class="linechart"  :id="id">
        </svg>
    </div>
</template>

<script>
import * as d3 from 'd3'
import { scaleLinear, scaleBand } from "d3-scale";
import { max, min } from "d3-array";
import { selectAll } from "d3-selection";

export default {
    name: "Test-Chart",
    props: {
        data : Object,
    },
    data() {
        return{
            testdata:{
                "PBS": 500,
                "PHS": 300,
                "PLA": 350
            },
            id: 10000,
            height: 600,
            heightSVG: 0,
            widthSVG: 0,
            width: 600,
            margin: {top: 30, right: 30, bottom: 30, left: 70},
            margin_top : 20,
            margin_left: 50,
            keys: Array,
            values: Array,
            color: Object,
            radius: 0,
            arc: Object,
            pie: Object,
            arcs: Object
        }
    },
    computed: {
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

            this.radius = Math.min(this.width, this.height) / 2 - 20;


            console.log(this.keys);

            this.color = d3.scaleOrdinal(d3.schemeCategory10);

            this.arc = d3.arc()
                        .outerRadius(this.radius)
                        .innerRadius(0);
        },
        draw(){
            this.container = this.svg.append("g")
                                    .attr("class", "svgcontainer")
                                    .attr("id", "c")
                                    .attr('transform', 'translate(' + this.width / 2 + ',' + this.height / 2 + ')');
                                    
            this.pie = d3.pie()
                        .sort(null)
                        .value(function(d) { return d; });

            
            let color = this. color;
            let radius = this.radius;
            let keys = this.keys;

            this.arcs = this.container.selectAll(".arc")
                            .data(this.pie(this.values));

            this.arcs
                            .transition()
                            .duration(1500)
                            .attrTween("d", arcTween);

                        var size = this.keys.length;
            this.arcs.enter().append("path")
                            .attr("class", "arc")
                            .attr("fill", function(d, i) { return color(keys[i]); })
                            .attr("d", this.arc)
                            .each(function(d) { this._current = d; });

            function arcTween(a) {
                let i = d3.interpolate(this._current, a);
                this._current = i(0);
                return function(t) {
                    return arc(i(t));
                };
            }
        },
        update(){

        }
    }
}
</script>

<style scoped>

</style>