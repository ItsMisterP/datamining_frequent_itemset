<template>
    <div class="content">
        <div class="md-layout" layout="row">
            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Crime by District Heatmap</h4>
                        <p class="category">
                            Total crime count per district.
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
            <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-49" >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Crime by District Heatmap</h4>
                        <p class="category">
                            Zeigt die absolute Anzahl nach Wochentag an.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <label> Displayed attribute:
                            <select @change="attributeChange($event.target.value)">
                                <option v-for="attribute in this.districtAttributes" :key="attribute" :value="attribute">
                                    {{ attribute }}
                                </option>
                            </select>
                        </label>
                        <piechart
                                id="2"
                                :pieData="this.selectedDistrictData"
                                :radius=200
                        ></piechart>
                    </md-card-content>
                </md-card>
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
        //chart: Chart,
        heatmap: HeatMap,
        //column: ColumnChart,
        //linechart: LineChart
        piechart: PieChart
    },
    created() {
        this.fetchData();
    },
    data() {
        return {
            countsAll: {},
            selectedDistrict: Object,
            countsPerDistrict: {},
            selectedDistrictData: {},
            districtAttributes: {},
            currentAttribute: String
        };
    },
    methods: {
        getURL: function(url) {
            return globalStore.prefix + url;
        },
        fetchData() {
            let dashboard = this;
            d3.json(this.getURL("json/CountsAll.json")).then(function(data) {
                dashboard.countsAll = data;
                dashboard.$emit("dataLoaded");
                console.log("Dashboard event: CountsAll finished loading");
            });
            d3.json(this.getURL("json/countsPerDistrict.json")).then(function(data) {
                dashboard.countsPerDistrict = data;
                console.log("Dashboard event: countsPerDistrict finished loading");
                dashboard.districtAttributes = Object.keys(dashboard.countsPerDistrict[Object.keys(dashboard.countsPerDistrict)[0]]);
                dashboard.currentAttribute = dashboard.districtAttributes[0];
            });
        },
        changeSelectedDistrict(selectedDistrict) {
            this.selectedDistrict = selectedDistrict;
            this.selectedDistrictData = this.countsPerDistrict[this.selectedDistrict][this.currentAttribute];
        },
        attributeChange(attribute) {
            this.currentAttribute = attribute;
            this.selectedDistrictData = this.countsPerDistrict[this.selectedDistrict][this.currentAttribute];
        }
    }
};
</script>
