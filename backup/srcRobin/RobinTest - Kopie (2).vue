<style>
    /* data table styles */
    #grid { height: 198px; }
    .row, .header { clear: left; font-size: 12px; line-height: 18px; height: 18px; }
    .row:nth-child(odd) { background: rgba(0,0,0,0.05); }
    .header { font-weight: bold; }
    .cell { float: left; overflow: hidden; white-space: nowrap; width: 100px; height: 18px; }
    .col-0 { width: 180px; }
</style>
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
import * as divgrid from './parallelcoords/divgrid';



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
            var pc0;

            var blue_to_brown = d3.scaleLinear()
                .domain([9, 50])
                .range(["steelblue", "brown"])
                .interpolate(d3.interpolateLab);

            var color = function(d) { return blue_to_brown(d['economy (mpg)']); };

            var parcoords = ParCoords()("#example")
                .color(color)
                .alpha(0.4);

            // load csv file and create the chart
            d3.csv('http://localhost:8000/csv/cars.csv').then(function (data) {
                parcoords
                    .data(data)
                    .hideAxis(["name"])
                    .render()
                    .brushMode("1D-axes") // enable brushing
                    .bundlingStrength(0) // set bundling strength
                    .smoothness(0)
                    .bundleDimension("cylinders")
                    .showControlPoints(false)
                    .hideAxis(["name"])
                    .render()
                    .brushMode("1D-axes")
                    .reorderable()
                    .interactive();

                // create data table, row hover highlighting
                var grid = d3.divgrid();
                d3.select("#grid")
                    .datum(data.slice(0,10))
                    .call(grid)
                    .selectAll(".row")
                    .on({
                        "mouseover": function(d) { parcoords.highlight([d]) },
                        "mouseout": parcoords.unhighlight
                    });


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


                // update data table on brush event
                parcoords.on("brush", function(d) {
                    d3.select("#grid")
                        .datum(d.slice(0,10))
                        .call(grid)
                        .selectAll(".row")
                        .on({
                            "mouseover": function(d) { parcoords.highlight([d]) },
                            "mouseout": parcoords.unhighlight
                        });
                });



            });
        }
    }
};
</script>
<style scoped>

    @import 'parallelcoords/style.css';
    @import 'parallelcoords/parcoordsPage.css';


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
