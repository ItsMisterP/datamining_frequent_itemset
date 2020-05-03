<template>
    <div class="content">
        <div class="md-layout">
            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Verbrechen nach den Wochentagen</h4>
                        <p class="category">
                            Zeigt die absolute Anzahl nach Wochentag an.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <chart
                            :dataString="
                                getURL('json/DataframeValueCountsWEEKDAY.json')
                            "
                            id="9"
                        ></chart>
                    </md-card-content>
                </md-card>
            </div>

            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Vebrechen nach der Uhrzeit</h4>
                        <p class="category">
                            Zeigt die absolute Anzahl nach der Uhrzeit an.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <column
                            :dataString="
                                getURL('json/DataframeValueCountsTIME.json')
                            "
                            id="8"
                        ></column>
                    </md-card-content>
                </md-card>
            </div>

            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Verbrechen pro Block (Top 30)</h4>
                        <p class="category">
                            Zeigt die absolute Anzahl pro Block an.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <column
                            :dataString="
                                getURL('json/DataframeValueCountsBLOCK.json')
                            "
                            id="7"
                        ></column>
                    </md-card-content>
                </md-card>
            </div>

            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Verbechen pro Location (Top 30)</h4>
                        <p class="category">
                            Zeigt die absolute Anzahl nach der Location an.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <column
                            :dataString="
                                getURL(
                                    'json/DataframeValueCountsLOCATIONDESCRIPTION.json'
                                )
                            "
                            id="6"
                        ></column>
                    </md-card-content>
                </md-card>
            </div>

            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">
                            Verbrechen pro "Primary Description"
                        </h4>
                        <p class="category">
                            Zeigt die absolute Anzahl der "Primary Description"
                            an.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <column
                            :dataString="
                                getURL(
                                    'json/DataframeValueCountsPRIMARYTYPE.json'
                                )
                            "
                            id="5"
                        ></column>
                    </md-card-content>
                </md-card>
            </div>

            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">
                            Verbrechen pro "Secondary Description"
                        </h4>
                        <p class="category">
                            Zeigt die absolute Anzahl der "Secondary
                            Description" an.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <column
                            :dataString="
                                getURL(
                                    'json/DataframeValueCountsDESCRIPTION.json'
                                )
                            "
                            id="3"
                        ></column>
                    </md-card-content>
                </md-card>
            </div>

            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">
                            Verbrechen je nach Tageszeit (grob)
                        </h4>
                        <p class="category">
                            Zeigt die absolute Anzahl nach AM und PM an.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <chart
                            :dataString="
                                getURL('json/DataframeValueCountsT.json')
                            "
                            id="1"
                        ></chart>
                    </md-card-content>
                </md-card>
            </div>

            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Vebrechen pro Monat</h4>
                        <p class="category">
                            Zeigt die absolute Anzahl der Verbrachen pro Monat
                            an.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <column
                            :dataString="
                                getURL('json/DataframeValueCountsMONTH.json')
                            "
                            id="2"
                        ></column>
                    </md-card-content>
                </md-card>
            </div>

            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">
                            Zeitliche Entwicklung der Verbrechen
                        </h4>
                        <p class="category">
                            Zeigt die zeitliche Entwicklung der absoluten Anzahl
                            der Verbrachen.
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <linechart
                            :dataString="
                                getURL('json/DataframeValueCountsYEAR.json')
                            "
                            id="4"
                        ></linechart>
                    </md-card-content>
                </md-card>
            </div>
            <!--
            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">
                            Items und ihre relative/absolute Anzahl
                        </h4>
                        <p class="category">Gibt das Aufkommen der Items an.</p>
                    </md-card-header>
                    <md-card-content>
                        <piechart></piechart>
                    </md-card-content>
                </md-card>
            </div>
            -->
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

export default {
    components: {
        chart: Chart,
        column: ColumnChart,
        linechart: LineChart
        //piechart: PieChart
    },
    created() {},
    data() {
        return {
            loadedData: {}
        };
    },
    methods: {
        getURL: function(url) {
            return globalStore.prefix + url;
        }
    }
};
</script>
