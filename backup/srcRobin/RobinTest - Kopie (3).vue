<style>
    /* data table styles */
    #grid { height: 100%; }
    .row, .header { clear: left; font-size: 0.75rem; line-height: 1.125rem; height: 1.125rem; }
    .row:nth-child(odd) { background: rgba(0,0,0,0.05); }
    .header { font-weight: bold; }
    .cell { float: left;  white-space: nowrap; width: 6.25rem; margin-right: 0.625rem; height: 1.125rem; }
    .col-0 { width: 15.625rem; }
    .col-1 { width: 15.625rem; }
</style>
<template>
    <div class="md-layout">
        <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
        >
            <md-card>
                <md-card-header data-background-color="gray">
                    <h4 class="title">Filter</h4>
                </md-card-header>
                <md-card-content>
                    <div id="example" class="parcoords" style="width:100%;height:30rem;margin-bottom: 3rem"></div>
                    <div id="grid"></div>
                </md-card-content>

            </md-card>


        </div>
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

            var dimensions = ["cs", "confidence", "imbratio", "kluc", "support"];


            // load csv file and create the chart
            d3.json(("http://localhost:8000/json/association_rules.json")).then(function(data) {
                console.log(data);
                pc0 = ParCoords()('#example')
                    .data(data)
                    .dimensions(dimensions)
                    .bundlingStrength(.5) // set bundling strength
                    .smoothness(0)
                    .showControlPoints(false)
                    .render()
                    .brushMode("1D-axes")
                    .reorderable()
                    .interactive();

                // create data table, row hover highlighting
                var grid = d3.divgrid();
                d3.select("#grid")
                    .datum(data.slice(0,500))
                    .call(grid)
                    .selectAll(".row")
                    .on({
                        "mouseover": function(d) { pc0.highlight([d]) },
                        "mouseout": pc0.unhighlight
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
                pc0.on("brush", function(d) {
                    d3.select("#grid")
                        .datum(d.slice(0,500))
                        .call(grid)
                        .selectAll(".row")
                        .on({
                            "mouseover": function(d) { pc0.highlight([d]) },
                            "mouseout": pc0.unhighlight
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
