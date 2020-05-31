<template>
    <div>
        <div class="md-layout">
            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Filter</h4>
                    </md-card-header>

                    <md-card-expand>
                        <md-card-actions
                            md-alignment="right"
                            id="expandableFilter"
                        >
                            <md-card-expand-trigger>
                                <md-button class="md-icon-button">
                                    <md-icon>keyboard_arrow_down</md-icon>
                                </md-button>
                            </md-card-expand-trigger>
                        </md-card-actions>
                        <md-card-expand-content>
                            <md-card-content>
                                <label for="networkminsup"
                                    >Min-Sup for Rules:</label
                                ><br />
                                <input
                                    id="networkminsup"
                                    @change="update"
                                    type="range"
                                    v-model.number="minsup"
                                    min="0.00001"
                                    max="0.3"
                                    step="0.00001"
                                />
                                {{ minsup }}
                                <br />
                                <label for="klucmin"
                                    >Minimum Kluc for Rules:</label
                                ><br />
                                <input
                                    id="klucmin"
                                    @change="update"
                                    type="range"
                                    v-model.number="klucMin"
                                    min="0.0"
                                    max="1"
                                    step="0.01"
                                />
                                {{ klucMin }}
                                <br />
                                <label for="klucmax"
                                    >Maximum Kluc for Rules:</label
                                ><br />
                                <input
                                    id="klucmax"
                                    @change="update"
                                    type="range"
                                    v-model.number="klucMax"
                                    min="0.0"
                                    max="1"
                                    step="0.01"
                                />
                                {{ klucMax }}
                                <br />
                                <label for="imbratio"
                                    >Imb-Ratio for Rules:</label
                                >
                                <br />
                                <input
                                    id="imbratio"
                                    @change="update"
                                    type="range"
                                    v-model.number="imb"
                                    min="0"
                                    max="1"
                                    step="0.01"
                                />
                                {{ imb }}
                                <br />
                                <md-checkbox
                                    :change="update"
                                    v-model="showItemsets"
                                    >Show Itemsets</md-checkbox
                                >
                            </md-card-content>
                        </md-card-expand-content>
                    </md-card-expand>
                </md-card>
            </div>

            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
            >
                <ForceGraph
                    ref="graph"
                    :graph="graph"
                    @nodeclicked="nodeclicked"
                ></ForceGraph>
            </div>

            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Association Rules</h4>
                    </md-card-header>
                    <md-card-content>
                        <md-table
                            v-model="tableRules"
                            md-sort="support"
                            md-sort-order="desc"
                            md-card
                            md-fixed-header
                        >
                            <md-table-empty-state
                                md-label="No Rules found"
                                :md-description="`No rules for the parameters`"
                            >
                            </md-table-empty-state>

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
                            </md-table-row>
                        </md-table>
                    </md-card-content>
                </md-card>
            </div>
        </div>
    </div>
</template>
<script>
import * as d3 from "d3";
import { scaleLinear, scaleBand } from "d3-scale";
import { max, min } from "d3-array";
import { selectAll } from "d3-selection";
import { globalStore } from "../main";
import ForceGraph from "../components/diagrams/ForceDirectedGraph";

export default {
    components: {
        ForceGraph
    },
    watch: {
        showItemsets: function() {
            this.update();
        }
    },
    data() {
        return {
            graph: {
                nodes: [],
                links: []
            },
            minsup: 0.001,
            klucMin: 0.0,
            klucMax: 1,
            imb: 0,
            showItemsets: false,
            filteredRules: [],
            tableRules: []
        };
    },
    mounted() {
        this.fetchData();
    },
    methods: {
        nodeclicked($event) {
            let d = $event;
            this.tableRules = this.filteredRules;
            this.tableRules = this.filteredRules.filter(item => {
                return (
                    item.antecedents.includes(d.id) ||
                    item.consequents.includes(d.id) ||
                    (
                        "{" +
                        item.antecedents.join(",") +
                        "}->{" +
                        item.consequents.join(",") +
                        "}"
                    ).includes(d.id)
                );
            });
        },
        fetchData() {
            let graph = this;
            d3.json(this.getURL("json/association_rules.json")).then(function(
                data
            ) {
                graph.rules = data;
                graph.prepareData();
                graph.$refs.graph.init();
            });
        },
        update() {
            this.graph.nodes = [];
            this.graph.links = [];
            this.prepareData();
            this.$refs.graph.update();
        },
        prepareData() {
            let rules = this.rules;
            this.filteredRules = rules.filter(item => {
                return (
                    item.support > this.minsup &&
                    item.kluc >= this.klucMin &&
                    item.kluc < this.klucMax &&
                    item.imbratio >= this.imb
                );
            });
            this.tableRules = this.filteredRules;
            if (!this.showItemsets) {
                this.filteredRules.forEach(element => {
                    let value = 1;
                    this.graph.nodes.push({
                        id:
                            "{" +
                            element.antecedents.join(",") +
                            "}->{" +
                            element.consequents.join(",") +
                            "}",
                        type: "rule",
                        col: "#FF6B66",
                        radius: this.radius + value,
                        support: element.support
                    });
                    let inputs = element.antecedents;
                    inputs.forEach(input => {
                        if (
                            this.graph.nodes.filter(node => node.id == input)
                                .length == 0
                        ) {
                            this.graph.nodes.push({
                                id: input,
                                col: "green",
                                radius: this.radius
                            });
                        }
                        this.graph.links.push({
                            source: input,
                            target:
                                "{" +
                                element.antecedents.join(",") +
                                "}->{" +
                                element.consequents.join(",") +
                                "}",
                            col: "blue"
                        });
                    });
                    let outputs = element.consequents;
                    outputs.forEach(output => {
                        if (
                            this.graph.nodes.filter(node => node.id == output)
                                .length == 0
                        ) {
                            this.graph.nodes.push({
                                id: output,
                                col: "green",
                                val: 2,
                                radius: this.radius
                            });
                        }
                        this.graph.links.push({
                            source:
                                "{" +
                                element.antecedents.join(",") +
                                "}->{" +
                                element.consequents.join(",") +
                                "}",
                            target: output,
                            col: "black"
                        });
                    });
                });
            } else {
                this.filteredRules.forEach(element => {
                    let value = 1000.0 * parseFloat(element.support);
                    this.graph.nodes.push({
                        id:
                            "{" +
                            element.antecedents.join(",") +
                            "}->{" +
                            element.consequents.join(",") +
                            "}",
                        type: "rule",
                        col: "#FF6B66",
                        radius: value
                    });
                    if (
                        this.graph.nodes.filter(
                            node =>
                                node.id ==
                                "{" + element.antecedents.join(",") + "}"
                        ).length == 0
                    ) {
                        let value2 = 1000.0 * parseFloat(element.as);
                        this.graph.nodes.push({
                            id: "{" + element.antecedents.join(",") + "}",
                            col: "green",
                            val: 2,
                            radius: value2
                        });
                    }
                    this.graph.links.push({
                        source: "{" + element.antecedents.join(",") + "}",
                        target:
                            "{" +
                            element.antecedents.join(",") +
                            "}->{" +
                            element.consequents.join(",") +
                            "}",
                        col: "blue"
                    });
                    if (
                        this.graph.nodes.filter(
                            node =>
                                node.id ==
                                "{" + element.consequents.join(",") + "}"
                        ).length == 0
                    ) {
                        let value3 = 1000.0 * parseFloat(element.as);
                        this.graph.nodes.push({
                            id: "{" + element.consequents.join(",") + "}",
                            col: "green",
                            val: 2,
                            radius: value3
                        });
                    }
                    this.graph.links.push({
                        source: "{" + element.consequents.join(",") + "}",
                        target:
                            "{" +
                            element.antecedents.join(",") +
                            "}->{" +
                            element.consequents.join(",") +
                            "}",
                        col: "black"
                    });
                });
            }
        },
        getURL: function(url) {
            return globalStore.prefix + url;
        }
    }
};
</script>
<style scoped>
.md-card-actions {
    margin: 1.75rem 1rem 0.75rem !important;
    background-color: #fff !important;
    border-top: 0 !important;
}
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
