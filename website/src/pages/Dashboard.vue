<template>
    <div class="content">
        <div class="md-layout">
            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
                layout="row"
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
                            :districtCrimeCount="loadedData['District']"
                            @update-selectedDistrict="changeSelectedDistrict"
                        ></heatmap>
                    </md-card-content>
                </md-card>
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Crime by District Heatmap</h4>
                        <p class="category">
                            Zeigt die absolute Anzahl nach Wochentag an.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <piechart
                            id="2"
                            :selectedDistrict="this.selectedDistrict"
                            @update-selectedDistrict="changeSelectedDistrict"
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

import { globalStore } from "../main";
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
            loadedData: {},
            selectedDistrict: Object
        };
    },
    methods: {
        getURL: function(url) {
            return globalStore.prefix + url;
        },
        fetchData() {
            let dashboard = this;
            d3.json(this.getURL("json/CountsAll.json")).then(function(data) {
                dashboard.loadedData = data;
                dashboard.$emit("dataLoaded");
                console.log("Dashboard event: CountsAll finished loading");
            });
        },
        changeSelectedDistrict(selectedDistrict) {
            console.log("dashboard data update");
            console.log(selectedDistrict);
        }
    }
};
</script>
