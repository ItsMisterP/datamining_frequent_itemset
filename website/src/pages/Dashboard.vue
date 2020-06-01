<template>
    <div class="content">
        <div class="md-layout">
            <div class="md-layout-item md-size-large-50 md-size-small-100 md-size-xsmall-100 md-size-medium-100 ">
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Total crimes per district</h4>
                        <p class="category">
                            Shows the total number of crimes in each district as a heatmap.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <heatmap
                            id="1"
                            :districtCrimeCount="this.countsAll['District']"
                            @update-selectedDistrict="changeSelectedDistrict"
                        ></heatmap>
                    </md-card-content>
                </md-card>
            </div>

            <div class="md-layout-item md-size-large-50 md-size-small-100 md-size-xsmall-100 md-size-medium-100 " >
                <div class="md-layout-item" >
                    <md-card>
                        <md-card-header data-background-color="gray">
                            <h4 class="title">Crimes per {{currentAttribute}} in {{selectedDistrictLabel}}</h4>
                            <p class="category">
                                Shows the distribution of the total crime count for the selected attribute in the selected district.
                            </p>
                        </md-card-header>
                        <md-card-content >
                            <label> Displayed attribute:
                                <select @change="attributeChange($event.target.value)">
                                    <option v-for="attribute in this.districtAttributes" :key="attribute" :value="attribute">
                                        {{ attribute }}
                                    </option>
                                </select>
                            </label>
                            <piechart
                                    :id="2"
                                    :pieData="this.selectedDistrictData"
                                    @update-pieColor="updatePieColor"
                            ></piechart>
                            <md-table
                                    v-model="this.tableData"
                                    md-card
                                    md-fixed-header
                                    md-height="235px"
                                    >
                                <md-table-row
                                        slot="md-table-row"
                                        slot-scope="{ item }">
                                    <md-table-cell
                                            md-label="Key">
                                        {{ item[0] }}
                                    </md-table-cell>
                                    <md-table-cell
                                            md-label="Value">
                                        {{ item[1] }}
                                    </md-table-cell>
                                    <md-table-cell
                                            md-label="Color"
                                            :style="{ background: getCellColor(item[0])}">
                                    </md-table-cell>
                                </md-table-row>
                            </md-table>
                        </md-card-content>
                    </md-card>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import * as d3 from "d3";
import Chart from "../components/diagrams/Chart";
import ColumnChart from "../components/diagrams/ColumnChart";
import LineChart from "../components/diagrams/LineChart";
import GroupedBarChart from "../components/diagrams/GroupedBarChart";
import MultiLineChart from "../components/diagrams/MultiLineChart";
import PieChart from "../components/diagrams/PieChart";
import test from "../components/diagrams/ZoomableBarChart";

import { globalStore } from "@/main";
import HeatMap from "@/components/diagrams/HeatMap";

export default {
    components: {
        heatmap: HeatMap,
        piechart: PieChart
    },
    created() {
        this.fetchData();
    },
    data() {
        return {
            countsAll: {},
            selectedDistrict: String,
            selectedDistrictLabel: String,
            countsPerDistrict: {},
            selectedDistrictData: {},
            districtAttributes: {},
            currentAttribute: String,
            dataLoaded: false,
            pieColor: Array,
            tmpColor: String
        };
    },
    methods: {
        getURL: function(url) {
            return globalStore.prefix + url;
        },
        fetchData() {
            this.tmpColor = "#1f77b4" ;
            let dashboard = this;
            d3.json(this.getURL("json/CountsAll.json")).then(function(data) {
                dashboard.countsAll = data;
                dashboard.$emit("dataLoaded");
            });
            d3.json(this.getURL("json/countsPerDistrict.json")).then(function(data) {
                dashboard.countsPerDistrict = data;
                let defaultDistrict = Object.keys(dashboard.countsPerDistrict)[0];
                dashboard.districtAttributes = Object.keys(dashboard.countsPerDistrict[defaultDistrict]);
                dashboard.changeSelectedDistrict(defaultDistrict);
                dashboard.attributeChange(dashboard.districtAttributes[0]);
                dashboard.dataLoaded = true;
            });
        },
        changeSelectedDistrict(selectedDistrict) {
            this.selectedDistrict = selectedDistrict;
            this.selectedDistrictLabel = "district " + selectedDistrict.substr(3, selectedDistrict.length);
            this.selectedDistrictData = this.countsPerDistrict[this.selectedDistrict][this.currentAttribute];
        },
        attributeChange(attribute) {
            this.currentAttribute = attribute;
            this.selectedDistrictData = this.countsPerDistrict[this.selectedDistrict][this.currentAttribute];
        },
        updatePieColor(color) {
            this.pieColor = color;
        },
        getCellColor(index) {
            return this.pieColor(index);
        }
    },
    computed: {
        tableData: function () {
            return Object.entries(this.selectedDistrictData);
        }
    }
};
</script>

<style scoped>


</style>