
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
                    <!-- http://bl.ocks.org/sc28/afa69162dc61833dc19fec7f0094f01a -->
                    <md-button id="btnReset">Reset Selection</md-button>
                    <div id="example" class="parcoords" style="width:100%;height:30rem;margin-bottom: 3rem"></div>

                    <md-table
                            v-model="tableRules"
                            md-sort="support"
                            md-sort-order="desc"
                            md-card
                            md-fixed-header
                    >
                        <md-table-row
                                slot="md-table-row"
                                slot-scope="{ item }"
                        >
                            <md-table-cell
                                    md-label="Support"
                                    md-sort-by="support"
                                    md-numeric
                            >
                                {{ item.support }}
                            </md-table-cell>
                            <md-table-cell
                                    md-label="Antecedents"
                                    md-sort-by="antecedents"
                            >
                                {{ item.antecedents }}
                            </md-table-cell>
                            <md-table-cell
                                    md-label="Consequents"
                                    md-sort-by="consequents"
                            >
                                {{ item.consequents }}
                            </md-table-cell>
                            <md-table-cell
                                    md-label="Confidence"
                                    md-sort-by="confidence"
                            >
                                {{ item.confidence }}
                            </md-table-cell>
                            <md-table-cell
                                    md-label="Kluc"
                                    md-sort-by="kluc"
                            >
                                {{ item.kluc }}
                            </md-table-cell>
                            <md-table-cell
                                    md-label="Imbalance Ratio"
                                    md-sort-by="imbratio"
                            >
                                {{ item.imbratio }}
                            </md-table-cell>
                            <md-table-cell
                                    md-label="cs"
                                    md-sort-by="cs"
                            >
                                {{ item.cs }}
                            </md-table-cell>
                        </md-table-row>
                    </md-table>



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


    export default {
        watch: {
            showItemsets: function() {
                this.update();
            }
        },

        data() {
            return {
                tableRules: [],
            };
        },
        mounted() {
            this.init();
        },
        methods: {
            getURL: function(url) {
                return globalStore.prefix + url;
            },
            update() {
                init();
            },

            init() {
                var blue_to_brown = d3.scaleLinear()
                    .domain([0.3, 0.5])
                    .range(["steelblue", "brown"])
                    .interpolate(d3.interpolateLab);

                var color = function(d) { return blue_to_brown(d["kluc"]) };

                var parcoords = ParCoords()("#example")
                    .color(color)
                    .alpha(0.4);

                var dimensions = ["cs", "confidence", "imbratio", "kluc", "support"];

                let graph = this;
                // load csv file and create the chart


                d3.json(this.getURL("json/association_rules.json")).then(function(data) {
                    graph.tableRules = data;
                    console.log(data);
                    parcoords
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


                    // smoothness
                    d3.select("#smoothness").on("change", function() {
                        d3.select("#smooth").text(this.value);
                        parcoords .smoothness(this.value).render();
                    });

                    // bundling strength slider
                    d3.select("#bundling").on("change", function() {
                        d3.select("#strength").text(this.value);
                        parcoords .bundlingStrength(this.value).render();
                    });

                    var select = d3.select("#bundleDimension").append("select").on("change", changeBundle);

                    var options = select.selectAll('option')
                        .data(d3.keys(parcoords .dimensions()));

                    options
                        .enter()
                        .append("option")
                        .attr("value", function(d) {return d;})
                        .text(function(d) {return d;});

                    function changeBundle() {
                        parcoords .bundleDimension(this.value);
                    }


                    parcoords .on("brush", function(d) {
                        graph.tableRules = d
                    });
                });

                //Neue funktionalität

                var sltBrushMode = d3.select('#sltBrushMode')
                sltBrushMode.selectAll('option')
                    .data(parcoords.brushModes())
                    .enter()
                    .append('option')
                    .text(function(d) { return d; });

                sltBrushMode.on('change', function() {
                    parcoords.brushMode(this.value);
                    switch(this.value) {
                        case 'None':
                            d3.select("#pStrums").style("visibility", "hidden");
                            d3.select("#lblPredicate").style("visibility", "hidden");
                            d3.select("#sltPredicate").style("visibility", "hidden");
                            d3.select("#btnReset").style("visibility", "hidden");
                            break;
                        case '2D-strums':
                            d3.select("#pStrums").style("visibility", "visible");
                            break;
                        default:
                            d3.select("#pStrums").style("visibility", "hidden");
                            d3.select("#lblPredicate").style("visibility", "visible");
                            d3.select("#sltPredicate").style("visibility", "visible");
                            d3.select("#btnReset").style("visibility", "visible");
                            break;
                    }
                });

                sltBrushMode.property('value', '1D-axes');

                d3.select('#btnReset').on('click', function() {parcoords.brushReset();})
                d3.select('#sltPredicate').on('change', function() {
                    parcoords.brushPredicate(this.value);
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
