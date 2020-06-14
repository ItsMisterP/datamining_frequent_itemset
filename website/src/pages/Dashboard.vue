<template>
    <div class="content">
        <div class="md-layout md-alignment-center">
            <div
                class="md-layout-item md-size-60 md-medium-size-33 md-small-size-50 md-xsmall-size-100"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <div>
                            <h4 class="title">Total crimes per district</h4>
                            <p class="category">
                                Shows the total number of crimes in each
                                district as a heatmap.
                            </p>
                        </div>
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

            <div
                class="md-layout-item md-size-40 md-medium-size-33 md-small-size-50 md-xsmall-size-100"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <div>
                            <h4 class="title">
                                Crimes per {{ currentAttribute }} in
                                {{ selectedDistrictLabel }}
                            </h4>
                            <p class="category">
                                Shows the distribution of the total crime count
                                for the selected attribute in the selected
                                district.
                            </p>
                        </div>
                    </md-card-header>
                    <md-card-content>
                        <label>
                            Displayed attribute:
                            <select
                                @change="attributeChange($event.target.value)"
                            >
                                <option
                                    v-for="attribute in this.districtAttributes"
                                    :key="attribute"
                                    :value="attribute"
                                >
                                    {{ attribute }}
                                </option>
                            </select>
                        </label>
                        <piechart
                            :id="2"
                            :pieData="this.selectedDistrictData"
                            @update-pieColor="updatePieColor"
                            @update-selectedTableRow="updateSelectedTableRow"
                        ></piechart>
                        <md-table
                            v-model="this.tableData"
                            md-card
                            md-fixed-header
                            md-height="267px"
                            id="pieDataTable"
                        >
                            <md-table-row
                                slot="md-table-row"
                                slot-scope="{ item }"
                                md-selectable="single"
                                :id="item[0]"
                            >
                                <md-table-cell md-label="Key">
                                    {{ item[0] }}
                                </md-table-cell>
                                <md-table-cell md-label="Value">
                                    {{ item[1] }}
                                </md-table-cell>
                                <md-table-cell
                                    md-label="Color"
                                    :style="{
                                        background:
                                            getCellColor(item[0]) + '!important'
                                    }"
                                >
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
import PieChart from "../components/diagrams/PieChart";
import { globalStore } from "@/main";
import HeatMap from "@/components/diagrams/HeatMap";

export default {
    components: {
        heatmap: HeatMap,
        piechart: PieChart
    },
    created() {
        this.fetchData();
        this.currentSelectedRowIndex = -1;
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
            tmpColor: String,
            currentSelectedRowIndex: Number
        };
    },
    methods: {
        getURL: function(url) {
            return globalStore.prefix + url;
        },
        fetchData() {
            this.tmpColor = "#1f77b4";
            let dashboard = this;
            d3.json(this.getURL("json/CountsAll.json")).then(function(data) {
                dashboard.countsAll = data;
                dashboard.$emit("dataLoaded");
            });
            d3.json(this.getURL("json/countsPerDistrict.json")).then(function(
                data
            ) {
                dashboard.countsPerDistrict = data;
                let defaultDistrict = Object.keys(
                    dashboard.countsPerDistrict
                )[0];
                dashboard.districtAttributes = Object.keys(
                    dashboard.countsPerDistrict[defaultDistrict]
                );
                dashboard.changeSelectedDistrict(defaultDistrict);
                dashboard.attributeChange(dashboard.districtAttributes[0]);
                dashboard.dataLoaded = true;
            });
        },
        changeSelectedDistrict(selectedDistrict) {
            this.selectedDistrict = selectedDistrict;
            this.selectedDistrictLabel =
                "district " +
                selectedDistrict.substr(3, selectedDistrict.length);
            this.selectedDistrictData = this.countsPerDistrict[
                this.selectedDistrict
            ][this.currentAttribute];
        },
        attributeChange(attribute) {
            this.currentAttribute = attribute;
            this.selectedDistrictData = this.countsPerDistrict[
                this.selectedDistrict
            ][this.currentAttribute];
        },
        updatePieColor(color) {
            this.pieColor = color;
        },
        getCellColor(index) {
            return this.pieColor(index);
        },
        updateSelectedTableRow(index) {
            if (this.currentSelectedRowIndex > 0) {
                d3.select(
                    document.getElementById("" + this.currentSelectedRowIndex)
                ).classed("md-selected-single", false);
            }
            this.currentSelectedRowIndex = index;
            let row = document.getElementById(
                "" + Object.keys(this.selectedDistrictData)[this.currentSelectedRowIndex]
            );
            d3.select(row).classed("md-selected-single", true);
            document.getElementsByClassName("md-table-content")[0].scrollTop =
                row.offsetTop;
        }
    },
    computed: {
        tableData: function() {
            return Object.entries(this.selectedDistrictData);
        }
    }
};
</script>

<style scoped>
</style>