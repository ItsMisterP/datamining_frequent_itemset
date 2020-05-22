<template>
    <div>
        <div id="example" class="parcoords" style="width:1000px;height:300px"></div>
        <div id="grid"></div>
    </div>
</template>
<script>
import * as d3 from "d3";
import { scaleLinear, scaleBand } from "d3-scale";
import { max, min } from "d3-array";
import { selectAll } from "d3-selection";
import { globalStore } from "../main";
import ParCoords from 'parcoord-es';



export default {
    watch: {},

    data() {
        return {};
    },
    mounted() {
        this.init();
    },
    methods: {
        init() {


            // var green_to_blue = d3.scaleLinear()
            //     .domain([9, 50])
            //     .range(["#7AC143", "#00B0DD"])
            //     .interpolate(d3.interpolateLab);
            //
            // var color = function(d) { return green_to_blue(d['Length of Day (hours)']); };
            //
            // var parcoords = ParCoords()("#example")
            //     .color(color)
            //     .alpha(0.4);
            //
            // d3.csv('http://localhost:8000/csv/planet.csv').then(function (data) {
            //     parcoords
            //         .data(data)
            //         .render()
            //         .brushMode("1D-axes");  // enable brushing
            // })

            //interact with this variable from a javascript console
            var pc0 = undefined;

            var parcoords = ParCoords()("#example")
                .alpha(0.4);
            d3.csv('http://localhost:8000/csv/cars.csv').then(function(data) {
                parcoords
                    .data(data)
                    .bundlingStrength(0) // set bundling strength
                    .smoothness(0)
                    .bundleDimension("cylinders")
                    .showControlPoints(false)
                    .hideAxis(["name"])
                    .render()
                    .brushMode("1D-axes")
                    .reorderable()
                    .interactive();

                // smoothness
                d3.select("#smoothness").on("change", function() {
                    d3.select("#smooth").text(this.value);
                    pc0.smoothness(this.value).render();
                });

                // bundling strength slider
                d3.select("#bundling").on("change", function() {
                    d3.select("#strength").text(this.value);
                    pc0.bundlingStrength(this.value).render();
                });

                var select = d3.select("#bundleDimension").append("select").on("change", changeBundle);

                var options = select.selectAll('option')
                    .data(d3.keys(pc0.dimensions()));

                options
                    .enter()
                    .append("option")
                    .attr("value", function(d) {return d;})
                    .text(function(d) {return d;});

                function changeBundle() {
                    pc0.bundleDimension(this.value);
                }
            });
        }
    }
};
</script>
<style scoped>
    @import 'parallelcoords/style.css';
.edge {
    stroke: white;
    stroke-width: 1;
}
.graphSVG {
    background-color: black;
}

div.container {
    width: 100%;
    border: 1px solid gray;
}
div.tooltip {
    position: absolute;
    text-align: center;
    width: 180px;
    padding: 2px;
    font: 12px sans-serif;
    background: lightsteelblue;
    border: 0px;
    border-radius: 8px;
    pointer-events: none;
}
input {
    width: 50%;
}
</style>
